"""Render controlled item scripts and normal inventory operations in Snes9x."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v57'));import build_v57 as b
SLOT=0x368B51
CONTEXTS={'07C6F1':1,'07D958':1,'07D967':1,'07D9AE':1,'097B8C':2,'097BD3':3,'097C07':2,'097C39':2,'097C60':1,'097F8B':2,'09FA30':2,'09FA75':2,'09FAB9':5,'09FD60':1,'2F9F9F':2,'2F9FE2':1,'2FA002':1,'2FA029':2,'2FA07E':2,'2FA0B7':1,'38E79A':1,'07E400':3,'07E4F6':3}
OPERATIONS={'eat_card':['Down','A'],'give_card_to_self':['Down','Down','A','A'],'drop_card':['Down','Down','Down','A'],'help_card':['Down','Down','Down','Down','A'],'use_card':['A']}
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
ap.add_argument('--mode',choices=['controlled','natural'],required=True);args=ap.parse_args();source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA
summary={'method':args.mode,'rom_modified_for_probe':args.mode=='controlled','wram_modified_for_probe':False,'core_sha256':b.sha(args.core.read_bytes()),'versions':{}}
for version in ((57,) if args.mode=='controlled' else (56,57)):
 plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());profiles={}
 for profile in ('accents','ascii'):
  base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes()));assert b.sha(base)==plan['profiles'][profile]['target_rom_sha256'];cases={}
  for name,value in (CONTEXTS if args.mode=='controlled' else OPERATIONS).items():
   out=(args.out/f'v{version}'/profile/name).resolve();out.mkdir(parents=True,exist_ok=True);fixture=bytearray(base)
   if args.mode=='controlled':fixture[SLOT:SLOT+4]=b.pointer(int(name,16))
   assert all(x==y for i,(x,y) in enumerate(zip(base,fixture)) if not (args.mode=='controlled' and SLOT<=i<SLOT+4))
   rom=out/'fixture.sfc';rom.write_bytes(fixture)
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
    read();send({'load':str((args.states_dir/profile/'after_combat.state').resolve()),'frames':60});captures=[]
    for key in ('A','Right','A','A'):tap(key)
    if args.mode=='natural':
     for i,key in enumerate(value):tap(key);captures.append(send({'frames':60,'screenshot':f'step_{i}'}))
     captures.append(send({'frames':150,'screenshot':'response'}))
    else:
     tap('A')
     for frame in (30,60,90):captures.append(send({'frames':30,'screenshot':f'early_{frame:03d}'}))
     for page in range(1,value+1):
      if page>1:
       for frame in (30,60,90):captures.append(send({'frames':30,'screenshot':f'page_{page:02d}_early_{frame:03d}'}))
      captures.append(send({'frames':210,'screenshot':f'page_{page:02d}'}))
      if page<value:tap('A')
    send({'quit':True});proc.wait(timeout=10);assert proc.returncode==0
   rom.unlink();cases[name]={'base_rom_sha256':b.sha(base),'fixture_rom_sha256':b.sha(fixture),'only_declared_routing_changed':True,'returncode':proc.returncode,'captures':captures};print(version,profile,name,'completed',flush=True)
  profiles[profile]=cases
 summary['versions'][str(version)]=profiles
(args.out/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
