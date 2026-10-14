import argparse,json,sys,subprocess,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'tools/v19'))
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--core',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
from build_v19 import apply,records
rom=args.rom.read_bytes()
core=args.core
summary={'core_sha256':hashlib.sha256(core.read_bytes()).hexdigest(),'profiles':{}}
keys=['title_final','intro','after_combat','state_restored','game_menu']
for profile in ('accents','ascii'):
 out=args.out/profile;out.mkdir(parents=True,exist_ok=True);out=out.resolve()
 target=apply(rom,records((r/f'patches/EarthBound_Beginnings_FR_v25_{profile}.ips').read_bytes()));rp=out/'test.sfc';rp.write_bytes(target)
 old=json.load(open(r/f'tests/emulation_v18_work/{profile}_history.json'))
 proc=subprocess.Popen([sys.executable,str(r/'tests/emulation_v18_work/libretro_runner.py'),'--core',str(core),'--rom',str(rp),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=open(out/'stderr.log','w'),text=True)
 # The core can emit diagnostics before the JSON response.
 def response():
  while True:
   line=proc.stdout.readline()
   if not line:raise RuntimeError('emulator ended unexpectedly')
   try:return json.loads(line)
   except json.JSONDecodeError:pass
 ready=response();new=[]
 for item in old:
  c=dict(item['command'])
  if 'load' in c:c['load']=str(out/Path(c['load']).name)
  proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();new.append({'command':c,'response':response()})
 proc.stdin.write('{"quit":true}\n');proc.stdin.flush();response();proc.wait(timeout=10)
 checks={}
 for key in keys:
  a=[x for x in old if x['command'].get('screenshot')==key]
  b=[x for x in new if x['command'].get('screenshot')==key]
  if a and b:checks[key]=a[-1]['response']['image']['sha256_rgb']==b[-1]['response']['image']['sha256_rgb']
 summary['profiles'][profile]={'ready':ready,'commands_replayed':len(new),'last_frame':new[-1]['response']['frame'],'screens_match_v18':checks,'returncode':proc.returncode}
 print(profile,summary['profiles'][profile],flush=True)
 rp.unlink()
(args.out/'results.json').write_text(json.dumps(summary,indent=2))

if not all(all(p['screens_match_v18'].values()) and p['returncode']==0 for p in summary['profiles'].values()):
    raise SystemExit('Smoke replay differs from V18 references; inspect captures')
