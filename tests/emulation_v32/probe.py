"""Native display probes using a temporary ROM hook, separate from release IPS.

First run replay.py to produce private after_combat save states. No RAM writes.
The hook replaces the 'nobody to talk to' fallback with a jump to a V32 copy.
This tests the native renderer and dynamic names, not the original story triggers.
"""
import argparse,json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v32'))
from build_v32 import apply,records,pointer,sha,transform
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--core',type=Path,required=True)
ap.add_argument('--only-script',choices=['33C945','3483DC','35E2C2','379FD3']);ap.add_argument('--replay-out',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
source=args.rom.read_bytes();fixture=json.loads((ROOT/'tools/v32/v32_dialogues_fr.json').read_text())
report=json.loads((ROOT/'tools/v32/validation_v32.json').read_text());history=json.loads((ROOT/'tests/emulation_v18_work/accents_history.json').read_text())
results=[]
for profile in ('accents','ascii'):
 base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v32_{profile}.ips').read_bytes()))
 state=args.replay_out/profile/'after_combat.state'
 for ident in ((args.only_script,) if args.only_script else ('33C945','3483DC','35E2C2','379FD3')):
  row=next(e for e in report['profiles'][profile]['relocated'] if e['id']==ident);dest=int(row['offset'],16)
  if ident=='379FD3':
   e=next(x for x in fixture['scripts'] if x['id']==ident)
   _,mapping=transform(bytes.fromhex(e['baseline_hex'][profile]),e['spans'],e['fr'],dest,profile)
   dest+=mapping[e['spans'][0][0]-1] # Start at @, after the story guard and inventory operations.
  out=(args.out/(profile+'_'+ident)).resolve();out.mkdir(parents=True,exist_ok=True)
  test=bytearray(base);test[0x07C588:0x07C58D]=b'\x0A'+pointer(dest)
  rom=out/'probe.sfc';rom.write_bytes(test)
  proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--core',str(args.core),'--rom',str(rom),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=open(out/'stderr.log','w'),text=True)
  def response():
   while True:
    line=proc.stdout.readline()
    if not line:raise RuntimeError('Core ended before response')
    try:return json.loads(line)
    except json.JSONDecodeError:pass
  ready=response()
  def send(c):
   proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();return response()
  send({'load':str(state.resolve()),'frame':history[254]['response']['frame']})
  for item in history[255:290]:
   c=dict(item['command']);c.pop('screenshot',None);c.pop('save',None)
   if 'load' in c:c['load']=str((args.replay_out/profile/Path(c['load']).name).resolve())
   send(c)
  shots=[send({'frames':240,'screenshot':'page_0'})]
  for i in range(1,2 if ident=='379FD3' else 4):
   send({'frames':2,'buttons':['A']});shots.append(send({'frames':160,'screenshot':'page_'+str(i)}))
  send({'quit':True});proc.wait(timeout=10);rom.unlink()
  results.append({'profile':profile,'script':ident,'destination':f'{dest:06X}','base_sha256':sha(base),
    'probe_sha256':sha(test),'hook':'07C588','hook_hex':bytes(test[0x07C588:0x07C58D]).hex(),
    'screens':[{'file':profile+'_'+ident+'/page_'+str(i)+'.png','sha256_rgb':r['image']['sha256_rgb']} for i,r in enumerate(shots)],
    'returncode':proc.returncode,'native_story_trigger_tested':False})
  print(profile,ident,proc.returncode,flush=True)
if args.only_script and (args.out/'results.json').exists():
 previous=json.loads((args.out/'results.json').read_text());keys={(r['profile'],r['script']) for r in results}
 results=[r for r in previous if (r['profile'],r['script']) not in keys]+results
args.out.mkdir(parents=True,exist_ok=True);(args.out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
if any(r['returncode']!=0 for r in results):raise SystemExit('Probe failed')
