"""Replay the established smoke history against both V35 profiles."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import apply,records
ap=argparse.ArgumentParser(); ap.add_argument('--rom',type=Path,required=True); ap.add_argument('--core',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
source=a.rom.read_bytes(); summary={'core_sha256':hashlib.sha256(a.core.read_bytes()).hexdigest(),'profiles':{}}
keys=['title_final','intro','after_combat','state_restored','game_menu']
for profile in ('accents','ascii'):
    out=(a.out/profile).resolve(); out.mkdir(parents=True,exist_ok=True)
    target=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v35_{profile}.ips').read_bytes())); rom=out/'test.sfc'; rom.write_bytes(target)
    history=json.loads((ROOT/f'tests/emulation_v18_work/{profile}_history.json').read_text())
    proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--core',str(a.core),'--rom',str(rom),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=open(out/'stderr.log','w'),text=True)
    def response():
        while True:
            line=proc.stdout.readline()
            if not line: raise RuntimeError('Arrêt prématuré du cœur')
            try:return json.loads(line)
            except json.JSONDecodeError:pass
    ready=response(); replay=[]
    for item in history:
        command=dict(item['command'])
        if 'load' in command: command['load']=str(out/Path(command['load']).name)
        proc.stdin.write(json.dumps(command)+'\n');proc.stdin.flush();replay.append({'command':command,'response':response()})
    proc.stdin.write('{"quit":true}\n');proc.stdin.flush();response();proc.wait(timeout=10);rom.unlink()
    checks={k:[x for x in history if x['command'].get('screenshot')==k][-1]['response']['image']['sha256_rgb']==[x for x in replay if x['command'].get('screenshot')==k][-1]['response']['image']['sha256_rgb'] for k in keys}
    summary['profiles'][profile]={'ready':ready,'commands_replayed':len(replay),'last_frame':replay[-1]['response']['frame'],'screens_match_v18':checks,'returncode':proc.returncode}
    print(profile,summary['profiles'][profile],flush=True)
(a.out/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
if not all(p['returncode']==0 and all(p['screens_match_v18'].values()) for p in summary['profiles'].values()): raise SystemExit('Régression visuelle')
