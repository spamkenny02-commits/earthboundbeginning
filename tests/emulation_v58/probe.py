"""Render controlled item scripts and normal inventory operations in Snes9x."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v58'));import build_v58 as b
SLOT=0x368B51
WRAPPER=0x330FC0
CONTEXTS={'09F897':3,'097CCA':3,'097EFA':4,'09F936':1,'09F946':2,'09F970':2,'09F990':1,'09F995':1,'09F99E':1,'09F9A4':1,'09F9AD':1,'09F9B2':1,'09F9BD':1,'09F9C4':1}
OPERATIONS={'eat_card':['Down','A'],'give_card_to_self':['Down','Down','A','A'],'drop_card':['Down','Down','Down','A'],'help_card':['Down','Down','Down','Down','A'],'use_card':['A']}
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
ap.add_argument('--only',help='Optional controlled context address')
ap.add_argument('--mode',choices=['controlled','natural'],required=True);args=ap.parse_args();source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA
summary={'method':args.mode,'rom_modified_for_probe':args.mode=='controlled','wram_modified_for_probe':False,'core_sha256':b.sha(args.core.read_bytes()),'versions':{}}
for version in ((58,) if args.mode=='controlled' else (57,58)):
 plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());profiles={}
 for profile in ('accents','ascii'):
  base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes()));assert b.sha(base)==plan['profiles'][profile]['target_rom_sha256'];cases={}
  for name,value in (CONTEXTS if args.mode=='controlled' else OPERATIONS).items():
   if args.only and name!=args.only:continue
   out=(args.out/f'v{version}'/profile/name).resolve();out.mkdir(parents=True,exist_ok=True);fixture=bytearray(base)
   wrapper=b''
   if args.mode=='controlled':
    destination=int(name,16)
    if destination>=0x09F990 and destination<=0x09F9C4:
     # Reproduce the translated parent prefix and wait after the leaf returns.
     # This controlled wrapper permits reading suffixes that otherwise vanish.
     wrapper=b'\x01'+b.encode('@(Encore un peu plus loin ',profile)+b'\x08'+b.pointer(destination)+b'\x13\x02'
     assert base[WRAPPER:WRAPPER+len(wrapper)]==bytes(len(wrapper))
     fixture[WRAPPER:WRAPPER+len(wrapper)]=wrapper;destination=WRAPPER
    fixture[SLOT:SLOT+4]=b.pointer(destination)
   assert all(x==y for i,(x,y) in enumerate(zip(base,fixture)) if not (args.mode=='controlled' and (SLOT<=i<SLOT+4 or WRAPPER<=i<WRAPPER+len(wrapper))))
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
   rom.unlink();cases[name]={'base_rom_sha256':b.sha(base),'fixture_rom_sha256':b.sha(fixture),'only_declared_probe_ranges_changed':True,'wrapper_offset':f'{WRAPPER:06X}' if wrapper else None,'wrapper_hex':wrapper.hex(),'returncode':proc.returncode,'captures':captures};print(version,profile,name,'completed',flush=True)
  profiles[profile]=cases
 summary['versions'][str(version)]=profiles
(args.out/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
