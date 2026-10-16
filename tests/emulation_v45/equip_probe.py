"""Insert one test weapon, then use the ordinary inventory Equip command.

The IPS ROM is unchanged; only the initial bank-card inventory byte is replaced.
This does not verify natural acquisition of the weapon.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import ROM_SHA,sha,apply,records
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();source=args.rom.read_bytes();assert sha(source)==ROM_SHA
summary={'method':'controlled_one_byte_weapon_inventory_then_normal_equip','rom_modified_for_probe':False,'wram_modified_for_probe':True,'inventory_offset':'0099F1','original_item':'B1','fixture_item':'11','core_sha256':sha(args.core.read_bytes()),'profiles':{}}
for profile in ('accents','ascii'):
 out=(args.out/profile).resolve();out.mkdir(parents=True,exist_ok=True)
 rom=out/'test.sfc';rom.write_bytes(apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v45_{profile}.ips').read_bytes())))
 with (out/'stderr.log').open('w') as err:
  p=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v39/inventory_fixture_runner.py'),'--rom',str(rom),'--core',str(args.core.resolve()),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
  def read():
   while True:
    line=p.stdout.readline()
    if not line:raise RuntimeError('Emulator exited')
    try:return json.loads(line)
    except json.JSONDecodeError:pass
  def send(c):p.stdin.write(json.dumps(c)+'\n');p.stdin.flush();return read()
  def tap(b):send({'frames':2,'buttons':[b]});send({'frames':12})
  ready=read();send({'load':str((args.states_dir/profile/'after_combat.state').resolve()),'frames':1})
  before=send({'ram':{'offset':'0x99f1','length':1}});assert before['ram_hex']=='b1'
  send({'write_ram':{'offset':'0x99f1','hex':'11'}})
  send({'frames':60})
  for b in ('A','Right','Down'):tap(b)
  send({'screenshot':'equip_selected','frames':1})
  captures=[]
  for stage in range(1,9):
   tap('A');captures.append(send({'frames':180,'screenshot':f'equip_stage_{stage}'})['image'])
  send({'quit':True});p.wait(timeout=10)
 rom.unlink()
 summary['profiles'][profile]={'ready':ready,'returncode':p.returncode,'captures':captures}
 print(profile,'completed',flush=True)
(args.out/'equip_results.json').write_text(json.dumps(summary,indent=2)+'\n')
