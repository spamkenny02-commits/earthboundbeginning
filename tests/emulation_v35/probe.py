"""Temporary entry-point probes; these are not normal narrative triggers."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import apply,records,sha
def pointer(p): return (p+0xC00000).to_bytes(4,'little')
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--core',type=Path,required=True);ap.add_argument('--replay-out',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
source=a.rom.read_bytes(); history=json.loads((ROOT/'tests/emulation_v18_work/accents_history.json').read_text()); plan=json.loads((ROOT/'tools/v35/validation_v35.json').read_text()); wanted=('33C5A2','364FBE','371E94','3770CF','38535C'); results=[]
for profile in ('accents','ascii'):
    base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v35_{profile}.ips').read_bytes())); destinations={e['id']:int(e['offset'],16) for e in plan['profiles'][profile]['relocated']}
    for ident in wanted:
        dest=destinations[ident];out=(a.out/f'{profile}_{ident}').resolve();out.mkdir(parents=True,exist_ok=True);test=bytearray(base);test[0x07C588:0x07C58D]=b'\x0A'+pointer(dest);rom=out/'probe.sfc';rom.write_bytes(test)
        proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--core',str(a.core),'--rom',str(rom),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=open(out/'stderr.log','w'),text=True)
        def response():
            while True:
                line=proc.stdout.readline()
                if not line:raise RuntimeError('Arrêt prématuré du cœur')
                try:return json.loads(line)
                except json.JSONDecodeError:pass
        response()
        def send(c):proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();return response()
        send({'load':str((a.replay_out/profile/'after_combat.state').resolve()),'frame':history[254]['response']['frame']})
        for item in history[255:290]:
            c=dict(item['command']);c.pop('screenshot',None);c.pop('save',None)
            if 'load' in c:c['load']=str((a.replay_out/profile/Path(c['load']).name).resolve())
            send(c)
        shots=[send({'frames':240,'screenshot':'page_0'})]
        for i in range(1,4):send({'frames':2,'buttons':['A']});shots.append(send({'frames':160,'screenshot':f'page_{i}'}))
        send({'quit':True});proc.wait(timeout=10);rom.unlink()
        results.append({'profile':profile,'script':ident,'destination':f'{dest:06X}','base_sha256':sha(base),'probe_sha256':sha(test),'hook':'07C588','screens':[{'file':f'{profile}_{ident}/page_{i}.png','sha256_rgb':s['image']['sha256_rgb']} for i,s in enumerate(shots)],'returncode':proc.returncode,'temporary_entry_point':True,'native_story_trigger_tested':False})
        print(profile,ident,proc.returncode,flush=True)
a.out.mkdir(parents=True,exist_ok=True);(a.out/'results.json').write_text(json.dumps({'core_sha256':hashlib.sha256(a.core.read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
if any(r['returncode'] for r in results):raise SystemExit('Échec de sonde')
