"""Exercise original 1A 21 in a synthetic text script; only read WRAM.
Uses V61 IPS unchanged. Does not execute the natural inventory routines.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'));import runtime as b
from opcode_proof import prove
SLOT,WRAPPER=0x368B51,0x330FC0
LEFT_HELPER,RIGHT_HELPER=0x330E00,0x330E20
CASES={'equal_byte':(5,5,False),'different_byte':(5,7,False),'equal_32bit':(0x12345678,0x12345678,False),'different_high_word':(1,0x10001,False),'different_low_word':(0x10002,0x10001,False),'equal_zero':(1,2,True)}
def constant_callback(value):
 # Return a 32-bit value in the engine's normal virtual return registers.
 return b'\xc2\x30\xa9'+(value&65535).to_bytes(2,'little')+b'\x85\x06\xa9'+(value>>16).to_bytes(2,'little')+b'\x85\x08\x6b'
def script(left,right,zero,profile):
 def set_work(address):return b'\x1a\x0c'+b.pointer(address)[:3]+b'\x81'
 return b'\x01'+b.encode('@Résultat: ',profile)+set_work(LEFT_HELPER)+b'\x0d\x00'+set_work(RIGHT_HELPER)+b'\x1a\x21\x0d\x00\x1c\x0a\x00\x00\x00\x00'+b.encode(' ; suite lue.',profile)+b'\x13\x02'

def read_registers(raw,start=0x8500):
 def word(a):return int.from_bytes(raw[a-start:a-start+2],'little')
 head,focus=word(0x88E0),word(0x8958)
 if head==0xFFFF:base=0x85FE;index=None
 else:
  index=raw[0x88E4+focus-start];index=index if index<128 else index-256;base=0x8650+index*0x52
 if not start<=base+0x17<base+0x1F<=start+len(raw):raise ValueError('Active window outside captured memory')
 return {'window_head':head,'window_focus':focus,'window_index':index,'window_base':f'{base:04X}','working_memory':int.from_bytes(raw[base+0x17-start:base+0x1B-start],'little'),'argument_memory':int.from_bytes(raw[base+0x1B-start:base+0x1F-start],'little')}
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);args=ap.parse_args();p=args.profile;source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA
 ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes();plan=json.loads((ROOT/'tools/v61/validation_v61.json').read_text());assert b.sha(ips)==plan['profiles'][p]['sha256'];base=b.apply(source,b.records(ips));prove(base)
 summary={'profile':p,'patch_version':'v61','base_rom_sha256':b.sha(base),'method':'synthetic_script_original_equality_handler_and_read_only_wram','wram_written_directly_by_tester':False,'register_initialization':'Two temporary callbacks return constants through the original 1A 0C engine; no natural inventory scene is claimed','core_sha256':b.sha(args.core.read_bytes()),'cases':{}}
 for name,(left,right,zero) in CASES.items():
  expected=int(left==right or zero);payload=script(left,right,zero,p);assert len(payload)<=64 and base[WRAPPER:WRAPPER+len(payload)]==bytes(len(payload));changes=[(SLOT,b.pointer(WRAPPER)),(WRAPPER,payload),(LEFT_HELPER,constant_callback(0 if zero else left)),(RIGHT_HELPER,constant_callback(0 if zero else right))]
  for address,code in changes[2:]:assert base[address:address+len(code)]==bytes(len(code));fixture=bytearray(base);mask=bytearray(len(base))
  for a,v in changes:fixture[a:a+len(v)]=v;mask[a:a+len(v)]=b'\1'*len(v)
  assert all(x==y or m for x,y,m in zip(base,fixture,mask));prove(fixture);out=(args.out/p/name).resolve();out.mkdir(exist_ok=True,parents=True);rom=out/'fixture.sfc';rom.write_bytes(fixture)
  with (out/'stderr.log').open('w') as err:
   proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(rom),'--core',str(args.core.resolve()),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
   def read():
    while True:
     line=proc.stdout.readline()
     if not line:raise RuntimeError('Emulator exited')
     try:return json.loads(line)
     except json.JSONDecodeError:pass
   def send(c):proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();return read()
   def tap(key):send({'frames':2,'buttons':[key]});send({'frames':12})
   read();send({'load':str((args.states_dir/p/'after_combat.state').resolve()),'frames':60})
   for key in ('A','Right','A','A','A'):tap(key)
   capture=send({'frames':300,'screenshot':'result','ram':{'offset':'0x8500','length':0x500}});registers=read_registers(bytes.fromhex(capture.pop('ram_hex')));assert registers['working_memory']==registers['argument_memory']==expected,(name,registers,expected)
   send({'quit':True});proc.wait(timeout=10);assert proc.returncode==0
  rom.unlink();summary['cases'][name]={'left':0 if zero else left,'right':0 if zero else right,'expected_result':expected,'registers_read':registers,'result_verified':True,'returncode':0,'payload_hex':payload.hex(),'constant_return_callbacks':[{'offset':f'{a:06X}','hex':code.hex()} for a,code in changes[2:]],'fixture_sha256':b.sha(fixture),'capture':capture};print(p,name,expected,'verified',flush=True)
 args.out.mkdir(exist_ok=True,parents=True);(args.out/f'results_{p}.json').write_text(json.dumps(summary,indent=2)+'\n')
