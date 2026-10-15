"""Seek a naturally triggered critical banner by delaying target confirmation.

No ROM bytes or entry points are modified beyond applying the published IPS.
Save states are temporary test accelerators and must not be committed.
"""
import argparse, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import apply,records
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--core',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
source=a.rom.read_bytes();history=json.loads((ROOT/'tests/emulation_v18_work/accents_history.json').read_text())
delays=[0,1,2,3,4,5,7,9,12,16,24,32,48,64];versions={}
for version in ('36','37'):
    out=(a.out/f'v{version}').resolve();out.mkdir(parents=True,exist_ok=True)
    target=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_accents.ips').read_bytes()));rom=out/'test.sfc';rom.write_bytes(target)
    proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--core',str(a.core),'--rom',str(rom),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=open(out/'stderr.log','w'),text=True)
    def response():
        while True:
            line=proc.stdout.readline()
            if not line:raise RuntimeError('Arrêt prématuré du cœur')
            try:return json.loads(line)
            except json.JSONDecodeError:pass
    response()
    for item in history[:158]:
        command={k:v for k,v in item['command'].items() if k not in ('screenshot','save')}
        proc.stdin.write(json.dumps(command)+'\n');proc.stdin.flush();response()
    proc.stdin.write('{"frames":1,"save":"battle_menu_checkpoint"}\n');proc.stdin.flush();saved=response()['state']
    shots={}
    for delay in delays:
        commands=[{'load':saved},{'frames':2,'buttons':['A']},{'frames':45+delay},{'frames':2,'buttons':['A']}]
        commands += [{'frames':8,'screenshot':f'd{delay:02d}_f{frame:03d}'} for frame in range(8,145,8)]
        for command in commands:
            proc.stdin.write(json.dumps(command)+'\n');proc.stdin.flush();r=response()
            if 'image' in r:shots[command['screenshot']]=r['image']['sha256_rgb']
    proc.stdin.write('{"quit":true}\n');proc.stdin.flush();response();proc.wait(timeout=10);rom.unlink()
    versions[version]={'shots':shots,'returncode':proc.returncode}
changed=[name for name,value in versions['37']['shots'].items() if versions['36']['shots'].get(name)!=value]
result={'delays':delays,'captures_per_delay':18,'changed_v37_vs_v36':changed,'natural_critical_observed':bool(changed),'versions':{v:{'returncode':x['returncode'],'capture_count':len(x['shots'])} for v,x in versions.items()}}
(a.out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if not all(x['returncode']==0 for x in versions.values()):raise SystemExit('Échec du cœur')
