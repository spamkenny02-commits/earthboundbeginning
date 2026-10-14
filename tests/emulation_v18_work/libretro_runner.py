#!/usr/bin/env python3
"""Minimal headless libretro frontend: full core emulation, controller events,
framebuffer capture, save states and WRAM inspection. No ROM patches or cheats.
Commands on stdin are JSON objects; responses are one-line JSON.
"""
import argparse,ctypes as C,hashlib,json,sys,time
from pathlib import Path
import numpy as np
from PIL import Image

class Variable(C.Structure):_fields_=[('key',C.c_char_p),('value',C.c_char_p)]
class Game(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
class System(C.Structure):_fields_=[('library_name',C.c_char_p),('library_version',C.c_char_p),('valid_extensions',C.c_char_p),('need_fullpath',C.c_bool),('block_extract',C.c_bool)]
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
VIDEO=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUDIO=C.CFUNCTYPE(None,C.c_int16,C.c_int16)
BATCH=C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
POLL=C.CFUNCTYPE(None)
INPUT=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
BUTTONS={'B':0,'Y':1,'Select':2,'Start':3,'Up':4,'Down':5,'Left':6,'Right':7,'A':8,'X':9,'L':10,'R':11}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--core',type=Path,required=True);ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    lib=C.CDLL(str(a.core.resolve()));latest={};frame=0;pressed=set();options={};pixel=2;audio_frames=0;history=[]
    directory=str(a.out.resolve()).encode()
    @ENV
    def env(cmd,data):
        nonlocal pixel
        if cmd in (9,31):C.cast(data,C.POINTER(C.c_char_p))[0]=directory;return True
        if cmd==10:pixel=C.cast(data,C.POINTER(C.c_int))[0];return pixel in (0,1,2)
        if cmd==3:C.cast(data,C.POINTER(C.c_bool))[0]=True;return True
        if cmd==52:C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
        if cmd==16:
            values=C.cast(data,C.POINTER(Variable));i=0
            while values[i].key:
                value=values[i].value.split(b';',1)[-1].strip().split(b'|')[0];options[values[i].key]=value;i+=1
            return True
        if cmd==15:
            v=C.cast(data,C.POINTER(Variable));key=v[0].key
            if key in options:v[0].value=options[key];return True
            return False
        if cmd==17:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
        if cmd==39:C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
        if cmd==0x1002f:C.cast(data,C.POINTER(C.c_int))[0]=3;return True
        if cmd in (1,6,8,11,18,35,37,55):return True
        return False
    @VIDEO
    def video(data,w,h,pitch):
        if data:latest.update(raw=C.string_at(data,pitch*h),width=w,height=h,pitch=pitch,pixel=pixel)
    @AUDIO
    def audio(l,r):pass
    @BATCH
    def batch(data,n):
        nonlocal audio_frames
        audio_frames+=n;return n
    @POLL
    def poll():pass
    @INPUT
    def input_state(port,device,index,ident):return int(port==0 and device==1 and ident in pressed)
    for name,cb,typ in [('environment',env,ENV),('video_refresh',video,VIDEO),('audio_sample',audio,AUDIO),('audio_sample_batch',batch,BATCH),('input_poll',poll,POLL),('input_state',input_state,INPUT)]:
        f=getattr(lib,'retro_set_'+name);f.argtypes=[typ];f(cb)
    lib.retro_load_game.argtypes=[C.POINTER(Game)];lib.retro_load_game.restype=C.c_bool
    lib.retro_get_system_info.argtypes=[C.POINTER(System)]
    lib.retro_get_memory_data.argtypes=[C.c_uint];lib.retro_get_memory_data.restype=C.c_void_p
    lib.retro_get_memory_size.argtypes=[C.c_uint];lib.retro_get_memory_size.restype=C.c_size_t
    lib.retro_serialize_size.restype=C.c_size_t
    lib.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];lib.retro_serialize.restype=C.c_bool
    lib.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];lib.retro_unserialize.restype=C.c_bool
    system=System();lib.retro_get_system_info(C.byref(system));lib.retro_init()
    data=a.rom.read_bytes();buffer=C.create_string_buffer(data);game=Game(str(a.rom.resolve()).encode(),C.cast(buffer,C.c_void_p),len(data),None)
    if not lib.retro_load_game(C.byref(game)):raise RuntimeError('Core failed to load ROM')
    libc=C.CDLL(None)
    def send(value):libc.fflush(None);print(json.dumps(value),flush=True)
    def snapshot(name):
        if not latest:raise RuntimeError('No video frame yet')
        w=latest['width'];h=latest['height'];pitch=latest['pitch'];fmt=latest['pixel'];raw=latest['raw']
        if fmt in (0,2):
            v=np.frombuffer(raw,dtype='<u2').reshape(h,pitch//2)[:,:w].astype(np.uint32)
            if fmt==2:r=((v>>11)&31)*255//31;g=((v>>5)&63)*255//63;b=(v&31)*255//31
            else:r=((v>>10)&31)*255//31;g=((v>>5)&31)*255//31;b=(v&31)*255//31
        else:
            v=np.frombuffer(raw,dtype='<u4').reshape(h,pitch//4)[:,:w];r=(v>>16)&255;g=(v>>8)&255;b=v&255
        img=Image.fromarray(np.stack([r,g,b],axis=-1).astype('uint8'));p=a.out/(name+'.png');img.save(p)
        return {'path':str(p.resolve()),'width':w,'height':h,'sha256_rgb':hashlib.sha256(img.tobytes()).hexdigest()}
    send({'ready':True,'core':system.library_name.decode(),'version':system.library_version.decode(),'source_sha256':hashlib.sha256(data).hexdigest(),'save_ram_size':lib.retro_get_memory_size(0)})
    try:
        for line in sys.stdin:
            command=json.loads(line);t=time.monotonic();response={}
            if 'load' in command:
                state=Path(command['load']).read_bytes();buf=C.create_string_buffer(state)
                if not lib.retro_unserialize(buf,len(state)):raise RuntimeError('State load failed')
                frame=command.get('frame',0)
            if command.get('reset'):lib.retro_reset()
            pressed={BUTTONS[x] for x in command.get('buttons',[])}
            for _ in range(command.get('frames',0)):lib.retro_run();frame+=1
            pressed=set()
            if 'screenshot' in command:response['image']=snapshot(command['screenshot'])
            if 'save' in command:
                n=lib.retro_serialize_size();buf=C.create_string_buffer(n)
                if not lib.retro_serialize(buf,n):raise RuntimeError('State save failed')
                p=a.out/(command['save']+'.state');p.write_bytes(buf.raw);response['state']=str(p.resolve())
            if 'ram' in command:
                off=int(str(command['ram']['offset']),0);size=command['ram'].get('length',32);ptr=lib.retro_get_memory_data(2)
                if off<0 or off+size>lib.retro_get_memory_size(2):raise ValueError('RAM range invalid')
                response['ram_hex']=C.string_at(ptr+off,size).hex(' ')
            if command.get('dump_ram'):
                ptr=lib.retro_get_memory_data(2);p=a.out/(command['dump_ram']+'.wram');p.write_bytes(C.string_at(ptr,lib.retro_get_memory_size(2)));response['ram_file']=str(p.resolve())
            response.update(frame=frame,audio_samples=audio_frames,elapsed=round(time.monotonic()-t,3));history.append({'command':command,'response':response});(a.out/'history.json').write_text(json.dumps(history,indent=2));send(response)
            if command.get('quit'):break
    finally:lib.retro_unload_game();lib.retro_deinit()
if __name__=='__main__':main()
