"""Compare five short-text paths in V60/V61 with controlled ROM routing.
No WRAM is edited. This does not prove access from their natural NPC scenes.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v61'));import build_v61 as b
SLOT,WRAPPER=0x368B51,0x330FC0
CASES={'article':(0x34FADF,'',False),'recipient':(0x37BE28,"@Donner l'objet (",False),'boo_one':(0x35041F,'',True),'boo_two':(0x3504A9,'',True),'boo_three':(0x3505D4,'',True)}
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
ap.add_argument('--profile',choices=('accents','ascii'),required=True);args=ap.parse_args();p=args.profile
source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA
summary={'profile':p,'wram_modified_by_tester':False,'method':'controlled_card_action_routing_with_call_wrapper','core_sha256':b.sha(args.core.read_bytes()),'versions':{}}
for version in (60,61):
 base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{p}.ips').read_bytes()));plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());assert b.sha(base)==plan['profiles'][p]['target_rom_sha256'];cases={}
 for name,(target,prefix,advance) in CASES.items():
  out=(args.out/f'v{version}'/p/name).resolve();out.mkdir(parents=True,exist_ok=True);wrapper=b'\x01'+b.encode(prefix,p)+b'\x08'+b.pointer(target)+b'\x13\x02';assert base[WRAPPER:WRAPPER+len(wrapper)]==bytes(len(wrapper));changes=[(SLOT,b.pointer(WRAPPER)),(WRAPPER,wrapper)];fixture=bytearray(base);mask=bytearray(len(base))
  for q,v in changes:fixture[q:q+len(v)]=v;mask[q:q+len(v)]=b'\1'*len(v)
  assert all(x==y or m for x,y,m in zip(base,fixture,mask));rom=out/'fixture.sfc';rom.write_bytes(fixture)
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
   ready=read();send({'load':str((args.states_dir/p/'after_combat.state').resolve()),'frames':60})
   for key in ('A','Right','A','A','A'):tap(key)
   send({'frames':90})
   if advance:tap('A')
   capture=send({'frames':180,'screenshot':'response'});send({'quit':True});proc.wait(timeout=10);assert proc.returncode==0
  rom.unlink();cases[name]={'returncode':0,'base_rom_sha256':b.sha(base),'fixture_sha256':b.sha(fixture),'original_text_and_commands_preserved_from_patch':True,'temporary_writes':[{'offset':f'{q:06X}','hex':v.hex()} for q,v in changes],'capture':capture};print(version,p,name,'completed',flush=True)
 summary['versions'][str(version)]=cases
args.out.mkdir(exist_ok=True,parents=True);(args.out/f'results_{p}.json').write_text(json.dumps(summary,indent=2)+'\n')
