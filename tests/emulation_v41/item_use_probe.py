"""Try the naturally owned bank card through the normal item menu after combat."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import ROM_SHA,sha,apply,records
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();source=args.rom.read_bytes()
if sha(source)!=ROM_SHA:raise ValueError('Original USA 1.2 ROM required')
args.out.mkdir(parents=True,exist_ok=True)
summary={'method':'normal_menu_use_of_naturally_owned_bank_card','rom_modified_for_probe':False,'wram_modified_for_probe':False,'profiles':{}}
for profile in ('accents','ascii'):
 out=(args.out/profile).resolve();out.mkdir(parents=True,exist_ok=True)
 rom=out/'test.sfc';rom.write_bytes(apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v41_{profile}.ips').read_bytes())))
 with (out/'stderr.log').open('w') as err:
  p=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(rom),'--core',str(args.core.resolve()),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
  def read():
   while True:
    line=p.stdout.readline()
    if not line:raise RuntimeError('Emulator exited')
    try:return json.loads(line)
    except json.JSONDecodeError:pass
  def send(command):
   p.stdin.write(json.dumps(command)+'\n');p.stdin.flush();return read()
  def tap(button):send({'frames':2,'buttons':[button]});send({'frames':12})
  ready=read();send({'load':str((args.states_dir/profile/'after_combat.state').resolve()),'frames':60})
  for button in ('A','Right','A','A'):tap(button)
  send({'frames':1,'screenshot':'item_actions'});tap('A')
  captures=[]
  for page in range(1,7):
   r=send({'frames':300,'screenshot':f'use_card_{page}'});captures.append(r['image']);tap('A')
  send({'quit':True});p.wait(timeout=10)
 summary['profiles'][profile]={'ready':ready,'returncode':p.returncode,'captures':captures}
 print(profile,'completed',flush=True)
(args.out/'use_card_results.json').write_text(json.dumps(summary,indent=2)+'\n')
