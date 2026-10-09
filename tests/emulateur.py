#!/usr/bin/env python3
"""Frontend libretro sans écran. Aucun cœur ni ROM distribué.
Usage: emulateur.py CORE ROM OUT [--state état] [--actions actions.json]
Actions: [{"frames":120,"buttons":[8],"capture":"nom","save":"état"}]
Boutons joypad: B=0,Start=3,haut=4,bas=5,gauche=6,droite=7,A=8.
Dépendances: numpy, Pillow; cœur libretro Snes9x 2010 compilé séparément.
"""
import argparse,ctypes as C,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('core');p.add_argument('rom');p.add_argument('out');p.add_argument('--state');p.add_argument('--actions');p.add_argument('--sram',type=Path,help='Charger puis conserver la RAM de sauvegarde native (.srm)');a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
lib=C.CDLL(a.core);fmt=0;last=None;buttons=set();frame=0;refs=[]
class Variable(C.Structure):_fields_=[('key',C.c_char_p),('value',C.c_char_p)]
class Game(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
options={};directory=str(out.resolve()).encode();refs.append(directory)
@C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
def env(cmd,data):
 global fmt
 if cmd==10:fmt=C.cast(data,C.POINTER(C.c_int))[0];return fmt in (0,1,2)
 if cmd in (9,30,31):C.cast(data,C.POINTER(C.c_char_p))[0]=directory;return True
 if cmd==16:
  v=C.cast(data,C.POINTER(Variable));i=0
  while v[i].key:
   options[v[i].key]=v[i].value.split(b'; ')[-1].split(b'|')[0];i+=1
  return True
 if cmd==15:
  v=C.cast(data,C.POINTER(Variable));v[0].value=options.get(v[0].key);return bool(v[0].value)
 if cmd==17:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
 if cmd==3:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
 if cmd==39:C.cast(data,C.POINTER(C.c_int))[0]=3;return True
 return False
@C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
def video(data,w,h,pitch):
 global last
 if not data:return
 dtype=np.uint32 if fmt==1 else np.uint16
 n=4 if fmt==1 else 2
 arr=np.frombuffer(C.string_at(data,pitch*h),dtype=dtype).reshape(h,pitch//n)[:,:w].copy()
 if fmt==1:r=(arr>>16)&255;g=(arr>>8)&255;b=arr&255
 else:
  r=((arr>>(11 if fmt==2 else 10))&31)*255//31;g=((arr>>5)&(63 if fmt==2 else 31))*255//(63 if fmt==2 else 31);b=(arr&31)*255//31
 last=Image.fromarray(np.stack([r,g,b],axis=2).astype('uint8'))
@C.CFUNCTYPE(None,C.c_int16,C.c_int16)
def audio(l,r):pass
@C.CFUNCTYPE(C.c_size_t,C.c_void_p,C.c_size_t)
def batch(data,n):return n
@C.CFUNCTYPE(None)
def poll():pass
@C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
def input_state(port,device,index,id):return int(port==0 and id in buttons)
for name,cb in [('environment',env),('video_refresh',video),('audio_sample',audio),('audio_sample_batch',batch),('input_poll',poll),('input_state',input_state)]:
 getattr(lib,'retro_set_'+name).argtypes=[type(cb)];getattr(lib,'retro_set_'+name)(cb)
lib.retro_init();lib.retro_load_game.argtypes=[C.POINTER(Game)];lib.retro_load_game.restype=C.c_bool
raw=Path(a.rom).read_bytes();buffer=C.create_string_buffer(raw);game=Game(str(Path(a.rom).resolve()).encode(),C.cast(buffer,C.c_void_p),len(raw),None)
assert lib.retro_load_game(C.byref(game)),'Échec chargement ROM'
lib.retro_get_memory_size.argtypes=[C.c_uint];lib.retro_get_memory_size.restype=C.c_size_t
lib.retro_get_memory_data.argtypes=[C.c_uint];lib.retro_get_memory_data.restype=C.c_void_p
sram_size=lib.retro_get_memory_size(0);sram_ptr=lib.retro_get_memory_data(0);sram_loaded_sha256=None;state_sha256=None
if a.sram:
 assert sram_size and sram_ptr,'RAM de sauvegarde absente'
 if a.sram.exists():
  saved=a.sram.read_bytes();assert len(saved)==sram_size,'Taille SRAM différente'
  sram_loaded_sha256=hashlib.sha256(saved).hexdigest();C.memmove(sram_ptr,saved,sram_size)
lib.retro_serialize_size.restype=C.c_size_t
lib.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];lib.retro_serialize.restype=C.c_bool
lib.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];lib.retro_unserialize.restype=C.c_bool
if a.state:
 st=Path(a.state).read_bytes();state_sha256=hashlib.sha256(st).hexdigest();buf=C.create_string_buffer(st);assert lib.retro_unserialize(buf,len(st))
lib.retro_set_controller_port_device(0,1)
actions=json.loads(Path(a.actions).read_text()) if a.actions else [{'frames':600,'capture':'boot','save':'boot.state'}]
for action in actions:
 buttons=set(action.get('buttons',[]))
 for _ in range(action['frames']):lib.retro_run();frame+=1
 if action.get('capture'):
  assert last is not None;last.save(out/(action['capture']+'.png'))
 if action.get('save'):
  size=lib.retro_serialize_size();buf=C.create_string_buffer(size);assert lib.retro_serialize(buf,size);(out/action['save']).write_bytes(buf.raw)
result={'frames':frame,'rom_sha256':hashlib.sha256(raw).hexdigest(),'pixel_format':fmt,'size':last.size,'actions':actions,'initial_state_sha256':state_sha256,'loaded_sram_sha256':sram_loaded_sha256}
if a.sram:
 saved=C.string_at(sram_ptr,sram_size);a.sram.parent.mkdir(parents=True,exist_ok=True);a.sram.write_bytes(saved)
 result['sram']={'size':sram_size,'sha256':hashlib.sha256(saved).hexdigest()}
(out/'session.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result))
lib.retro_unload_game();lib.retro_deinit()
