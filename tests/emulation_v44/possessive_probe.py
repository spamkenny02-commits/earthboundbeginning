"""Controlled rendering fixtures: route guard's description to ten V44 messages.

Only one four-byte action-description pointer differs from each published ROM.
This validates native text rendering, not natural access to these enemy actions.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v44'))
from build_v44 import ROM_SHA,sha,apply,records,pointer
TARGETS=('2F7192','2F8026','2F804B','2F8239','2F835C','2F83CA','2F8A52','2F8B65','2F9C02','367694')
SLOT=0x368275
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();source=args.rom.read_bytes()
if sha(source)!=ROM_SHA:raise ValueError('Original USA 1.2 ROM required')
plan=json.loads((ROOT/'tools/v44/validation_v44.json').read_text())
v42=json.loads((ROOT/'tools/v42/validation_v42.json').read_text())
summary={'core_sha256':sha(args.core.read_bytes()),'method':'controlled_guard_description_routing','rom_modified_for_probe':True,'wram_modified_for_probe':False,'pointer_slot':f'{SLOT:06X}','natural_access_to_target_actions_verified':False,'profiles':{}}
for profile in ('accents','ascii'):
 base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v44_{profile}.ips').read_bytes()))
 assert sha(base)==plan['profiles'][profile]['target_rom_sha256']
 guard=next(e for e in v42['profiles'][profile]['relocated'] if e['id']=='2F84C6')
 assert base[SLOT:SLOT+4]==pointer(int(guard['offset'],16))
 moved={e['id']:e for e in plan['profiles'][profile]['relocated']}
 history=json.loads((ROOT/f'tests/emulation_v18_work/{profile}_history.json').read_text())
 checkpoint=next(i for i,e in enumerate(history) if e['command'].get('save')=='lamp_checkpoint')
 stop=next(i for i,e in enumerate(history) if e['command'].get('screenshot')=='battle_menu')
 cases={}
 for ident in TARGETS:
  out=(args.out/profile/ident).resolve();out.mkdir(parents=True,exist_ok=True)
  target=int(moved[ident]['offset'],16);fixture=bytearray(base);fixture[SLOT:SLOT+4]=pointer(target)
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
   def send(command):
    p.stdin.write(json.dumps(command)+'\n');p.stdin.flush();return read()
   def tap(button):send({'frames':2,'buttons':[button]});send({'frames':12})
   ready=read();send({'load':str((args.states_dir/profile/'lamp_checkpoint.state').resolve()),'frames':0})
   for e in history[checkpoint+1:stop+1]:send(e['command'])
   tap('Right');tap('Down');tap('A')
   captures=[]
   for frame in range(5,601,5):
    r=send({'frames':5,'screenshot':f'text_{frame:03d}'});captures.append(r['image'])
   send({'quit':True});p.wait(timeout=10)
  rom.unlink()
  cases[ident]={'base_rom_sha256':sha(base),'fixture_rom_sha256':sha(fixture),'new_target':f'{target:06X}','only_pointer_operand_changed':True,'returncode':p.returncode,'captures':captures}
  print(profile,ident,'complete',flush=True)
 summary['profiles'][profile]=cases
args.out.mkdir(parents=True,exist_ok=True)
(args.out/'possessive_results.json').write_text(json.dumps(summary,indent=2)+'\n')
