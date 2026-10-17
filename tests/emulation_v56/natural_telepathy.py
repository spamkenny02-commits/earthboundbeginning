"""Use Telepathy through the normal menu in V55/V56, without ROM or WRAM edits."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v56'))
import build_v56 as b
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA
summary={'method':'normal_menu_telepathy','rom_modified_for_probe':False,'wram_modified_for_probe':False,'core_sha256':b.sha(args.core.read_bytes()),'versions':{}}
for version in (55,56):
 profiles={};plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text())
 for profile in ('accents','ascii'):
  out=(args.out/f'v{version}'/profile).resolve();out.mkdir(parents=True,exist_ok=True);target=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes()));assert b.sha(target)==plan['profiles'][profile]['target_rom_sha256'];rom=out/'fixture.sfc';rom.write_bytes(target)
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
   for i,key in enumerate(('A','Down','A','A','A')):tap(key);captures.append(send({'frames':60,'screenshot':f'step_{i}'}))
   send({'quit':True});proc.wait(timeout=10);assert proc.returncode==0
  rom.unlink();profiles[profile]={'target_rom_sha256':b.sha(target),'returncode':proc.returncode,'captures':captures};print(version,profile,'completed',flush=True)
 summary['versions'][str(version)]=profiles
(args.out/'natural_results.json').write_text(json.dumps(summary,indent=2)+'\n')
