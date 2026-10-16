"""Render eight V47 messages through the normally owned bank-card action.

Only one description pointer changes in each test ROM. These are display
checks, not tests of natural events or their gameplay effects.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v47'))
from build_v47 import ROM_SHA,sha,apply,records,pointer
SLOT=0x368B51
TARGETS=('366E26','366E39','366E5B','36804C','3603C7','34B686','373CD8','38227C')
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();source=args.rom.read_bytes();assert sha(source)==ROM_SHA
plan=json.loads((ROOT/'tools/v47/validation_v47.json').read_text())
prior=json.loads((ROOT/'tools/v42/validation_v42.json').read_text())
summary={'method':'controlled_bank_card_description_routing','rom_modified_for_probe':True,'wram_modified_for_probe':False,'pointer_slot':f'{SLOT:06X}','core_sha256':sha(args.core.read_bytes()),'natural_inventory_saturation_verified':False,'profiles':{}}
for profile in ('accents','ascii'):
 base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v47_{profile}.ips').read_bytes()))
 assert sha(base)==plan['profiles'][profile]['target_rom_sha256']
 old=next(e for e in prior['profiles'][profile]['relocated'] if e['id']=='09FBF2')
 assert base[SLOT:SLOT+4]==pointer(int(old['offset'],16))
 moved={e['id']:e for e in plan['profiles'][profile]['relocated']};cases={}
 for ident in TARGETS:
  out=(args.out/profile/ident).resolve();out.mkdir(parents=True,exist_ok=True)
  fixture=bytearray(base);dest=int(moved[ident]['offset'],16);fixture[SLOT:SLOT+4]=pointer(dest)
  assert all(a==b for i,(a,b) in enumerate(zip(base,fixture)) if not SLOT<=i<SLOT+4)
  rom=out/'fixture.sfc';rom.write_bytes(fixture)
  with (out/'stderr.log').open('w') as err:
   p=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(rom),'--core',str(args.core.resolve()),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
   def read():
    while True:
     line=p.stdout.readline()
     if not line:raise RuntimeError('Emulator exited')
     try:return json.loads(line)
     except json.JSONDecodeError:pass
   def send(c):p.stdin.write(json.dumps(c)+'\n');p.stdin.flush();return read()
   def tap(b):send({'frames':2,'buttons':[b]});send({'frames':12})
   ready=read();send({'load':str((args.states_dir/profile/'after_combat.state').resolve()),'frames':60})
   for b in ('A','Right','A','A','A'):tap(b)
   captures=[]
   pages=4 if ident=='3603C7' else 1
   for page in range(1,pages+1):
    captures.append(send({'frames':300,'screenshot':f'page_{page:02d}'})['image'])
    if ident=='2F7C73' and page==3:tap('Right')
    tap('A')
   send({'quit':True});p.wait(timeout=10)
  rom.unlink()
  cases[ident]={'base_rom_sha256':sha(base),'fixture_rom_sha256':sha(fixture),'new_target':f'{dest:06X}','only_pointer_operand_changed':True,'returncode':p.returncode,'captures':captures}
  print(profile,ident,'completed',flush=True)
 summary['profiles'][profile]=cases
(args.out/'display_results.json').write_text(json.dumps(summary,indent=2)+'\n')
