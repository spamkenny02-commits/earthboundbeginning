"""Render V50 messages and complete item-description contexts through the normally owned bank-card action.

Only one description pointer changes in each test ROM. These are display
checks, not tests of natural events or their gameplay effects.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v50'))
from build_v50 import ROM_SHA,sha,apply,records,encode
from build_v48 import pointer
SLOT=0x368B51
CASES={'3479FF':2,'3498EA':1,'349AC0':2,'34B517':2,'35603F':3,'35698B':3,'356E3C':3,'35734D':2,'3573D9':3,'35C6FC':2,'36BAFC':1,'36BB0F':1,'361AFB':1}
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();source=args.rom.read_bytes();assert sha(source)==ROM_SHA
plan=json.loads((ROOT/'tools/v50/validation_v50.json').read_text())
prior=json.loads((ROOT/'tools/v42/validation_v42.json').read_text())
fixtures=json.loads((ROOT/'tools/v50/v50_fixtures.json').read_text())
summary={'method':'controlled_bank_card_routing_with_two_scoped_display_wrappers','rom_modified_for_probe':True,'wram_modified_for_probe':False,'pointer_slot':f'{SLOT:06X}','core_sha256':sha(args.core.read_bytes()),'natural_scene_access_verified':False,'profiles':{}}
for profile in ('accents','ascii'):
 base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v50_{profile}.ips').read_bytes()))
 assert sha(base)==plan['profiles'][profile]['target_rom_sha256']
 old=next(e for e in prior['profiles'][profile]['relocated'] if e['id']=='09FBF2')
 assert base[SLOT:SLOT+4]==pointer(int(old['offset'],16))
 cases={}
 for ident,pages in CASES.items():
  out=(args.out/profile/ident).resolve();out.mkdir(parents=True,exist_ok=True)
  fixture=bytearray(base);dest=int(ident,16);wrapper=b'';wrapper_offset=None
  if ident in ('3498EA','34B517','361AFB'):
   dest=int(next(e['offset'] for e in fixtures['edits'] if ident in e['contexts']),16)
  if ident in ('36BAFC','36BB0F'):
   wrapper_offset=int(fixtures['grammar']['reserve'][1],16)-32
   wrapper=b'\x01'+encode('@Lien: ',profile)+b'\x08'+pointer(dest)+b'\x13\x02'
   assert base[wrapper_offset:wrapper_offset+len(wrapper)]==bytes(len(wrapper))
   assert all(not (int(e['offset'],16)<wrapper_offset+len(wrapper) and int(e['offset'],16)+e['length']>wrapper_offset) for e in plan['profiles'][profile]['grammar_copies'])
   fixture[wrapper_offset:wrapper_offset+len(wrapper)]=wrapper;dest=wrapper_offset
  fixture[SLOT:SLOT+4]=pointer(dest)
  assert all(a==b for i,(a,b) in enumerate(zip(base,fixture)) if not (SLOT<=i<SLOT+4 or wrapper_offset is not None and wrapper_offset<=i<wrapper_offset+len(wrapper)))
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
   for page in range(1,pages+1):
    captures.append(send({'frames':300,'screenshot':f'page_{page:02d}'})['image'])
    if page<pages:tap('A')
   send({'quit':True});p.wait(timeout=10)
  rom.unlink()
  cases[ident]={'base_rom_sha256':sha(base),'fixture_rom_sha256':sha(fixture),'new_target':f'{dest:06X}','only_pointer_operand_changed':not bool(wrapper),'only_declared_ranges_changed':True,'wrapper_offset':f'{wrapper_offset:06X}' if wrapper_offset is not None else None,'wrapper_hex':wrapper.hex(),'forced_text_entry':ident in ('3498EA','34B517','361AFB'),'returncode':p.returncode,'captures':captures}
  print(profile,ident,'completed',flush=True)
 summary['profiles'][profile]=cases
(args.out/'display_results.json').write_text(json.dumps(summary,indent=2)+'\n')
