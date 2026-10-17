"""Render V56 messages and complete item-description contexts through the normally owned bank-card action.

Only one description pointer changes in each test ROM. These are display
checks, not tests of natural events or their gameplay effects.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v56'))
from build_v56 import ROM_SHA,sha,apply,records,pointer
SLOT=0x368B51
CASES={'33DC44': 1, '351AC4': 1, '352432': 1, '38D231': 1, '38D947': 2, '38D968': 1, '38D973': 1, '38D97F': 1, '38D99E': 1, '06BEF9': 1, '07C802': 1, '07C812': 1, '07DA10': 1, '07DA26': 1, '07DA34': 1, '07DA5C': 1, '07DA7D': 1, '07DA93': 1, '07DAB7': 1, '35EC64': 1, '37A956': 1, '38D1B0': 6, '38D93F': 2, '33DBF6': 3}
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
ap.add_argument('--temporal-check',action='store_true')
args=ap.parse_args();
if args.temporal_check:CASES={'07DA0C':1,'07DA58':1,'07DA8F':1,'38D1B0':6}
source=args.rom.read_bytes();assert sha(source)==ROM_SHA
plan=json.loads((ROOT/'tools/v56/validation_v56.json').read_text())
prior=json.loads((ROOT/'tools/v42/validation_v42.json').read_text())
summary={'method':'controlled_bank_card_routing_to_each_text_run_and_four_complete_contexts','rom_modified_for_probe':True,'wram_modified_for_probe':False,'pointer_slot':f'{SLOT:06X}','core_sha256':sha(args.core.read_bytes()),'natural_scene_access_verified':False,'profiles':{}}
for profile in ('accents','ascii'):
 base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v56_{profile}.ips').read_bytes()))
 assert sha(base)==plan['profiles'][profile]['target_rom_sha256']
 old=next(e for e in prior['profiles'][profile]['relocated'] if e['id']=='09FBF2')
 assert base[SLOT:SLOT+4]==pointer(int(old['offset'],16))
 cases={}
 for ident,pages in CASES.items():
  out=(args.out/profile/ident).resolve();out.mkdir(parents=True,exist_ok=True)
  fixture=bytearray(base);dest=int(ident,16)
  fixture[SLOT:SLOT+4]=pointer(dest)
  assert all(a==b for i,(a,b) in enumerate(zip(base,fixture)) if not (SLOT<=i<SLOT+4))
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
   if args.temporal_check:
    elapsed=0
    for frame in (15,45,50,105):
     captures.append(send({'frames':frame-elapsed,'screenshot':f'early_{frame:03d}'})['image']);elapsed=frame
   for page in range(1,pages+1):
    captures.append(send({'frames':300,'screenshot':f'page_{page:02d}'})['image'])
    if page<pages:tap('A')
   send({'quit':True});p.wait(timeout=10)
  rom.unlink();assert p.returncode==0
  cases[ident]={'base_rom_sha256':sha(base),'fixture_rom_sha256':sha(fixture),'new_target':f'{dest:06X}','only_pointer_operand_changed':True,'only_declared_ranges_changed':True,'forced_text_entry':ident not in ('38D1B0','38D93F','33DBF6'),'returncode':p.returncode,'captures':captures}
  print(profile,ident,'completed',flush=True)
 summary['profiles'][profile]=cases
(args.out/'display_results.json').write_text(json.dumps(summary,indent=2)+'\n')
