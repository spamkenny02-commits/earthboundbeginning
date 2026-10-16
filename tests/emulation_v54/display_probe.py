"""Compare controlled menu selections in V53 and V54, with no WRAM edits."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v54'))
from build_v54 import ROM_SHA,sha,apply,records,pointer
SLOT=0x368B51
# name, root, A presses before menu, navigation, confirmation
CASES=[('house_yes','npc:205BFF',0,[],'A'),('house_no','npc:205BFF',0,['Right'],'A'),('house_cancel','npc:205BFF',0,[],'B'),
 ('storage_deposit','34B490',1,[],'A'),('storage_withdraw','34B490',1,['Right'],'A'),('storage_repeat','34B4F0',0,['Right'],'A'),
 ('rest_heal','352AA1',0,[],'A'),('rest_sleep','352AA1',0,['Right'],'A'),
 ('pizza_small','35E3C3',1,[],'A'),('pizza_medium','35E3C3',1,['Down'],'A'),('pizza_large','35E3C3',1,['Down','Down'],'A'),('pizza_cancel','35E3C3',1,[],'B'),
 ('payment_no','35E4E9',1,['Right'],'A'),('shop_no','354D77',2,['Right'],'A')]
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();source=args.rom.read_bytes();assert sha(source)==ROM_SHA
summary={'method':'controlled_bank_card_routing_comparing_original_and_translated_menu_selections','rom_modified_for_probe':True,'wram_modified_for_probe':False,'pointer_slot':f'{SLOT:06X}','core_sha256':sha(args.core.read_bytes()),'natural_scene_access_verified':False,'versions':{}}
for version in (53,54):
 plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());profiles={}
 for profile in ('accents','ascii'):
  base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes()));assert sha(base)==plan['profiles'][profile]['target_rom_sha256'];cases={}
  for name,root,advances,navigation,confirmation in CASES:
   out=(args.out/f'v{version}'/profile/name).resolve();out.mkdir(parents=True,exist_ok=True)
   dest=int.from_bytes(base[int(root[4:],16):int(root[4:],16)+4],'little')-0xC00000 if root.startswith('npc:') else int(root,16)
   fixture=bytearray(base);fixture[SLOT:SLOT+4]=pointer(dest)
   assert all(a==b for i,(a,b) in enumerate(zip(base,fixture)) if not SLOT<=i<SLOT+4)
   rom=out/'fixture.sfc';rom.write_bytes(fixture)
   with (out/'stderr.log').open('w') as err:
    proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(rom),'--core',str(args.core.resolve()),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
    def read():
     while True:
      line=proc.stdout.readline()
      if not line:raise RuntimeError('Emulator exited')
      try:return json.loads(line)
      except json.JSONDecodeError:pass
    def send(c):proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();return read()
    def tap(button):send({'frames':2,'buttons':[button]});send({'frames':12})
    ready=read();send({'load':str((args.states_dir/profile/'after_combat.state').resolve()),'frames':60})
    for button in ('A','Right','A','A','A'):tap(button)
    send({'frames':300})
    for _ in range(advances):tap('A');send({'frames':300})
    captures={'menu':send({'frames':60,'screenshot':'menu'})['image']}
    for button in navigation:tap(button)
    captures['selected']=send({'frames':60,'screenshot':'selected'})['image'];tap(confirmation)
    captures['result']=send({'frames':300,'screenshot':'result'})['image'];send({'quit':True});proc.wait(timeout=10)
   rom.unlink();assert proc.returncode==0
   cases[name]={'base_rom_sha256':sha(base),'fixture_rom_sha256':sha(fixture),'target':f'{dest:06X}','navigation':navigation,'confirmation':confirmation,'only_pointer_operand_changed':True,'returncode':proc.returncode,'captures':captures}
   print(version,profile,name,'completed',flush=True)
  profiles[profile]=cases
 summary['versions'][str(version)]=profiles
comparison={}
for profile in ('accents','ascii'):
 comparison[profile]={name:summary['versions']['53'][profile][name]['captures']['result']['sha256_rgb']==summary['versions']['54'][profile][name]['captures']['result']['sha256_rgb'] for name,*_ in CASES}
summary['result_images_identical_to_v53']=comparison
(args.out/'display_results.json').write_text(json.dumps(summary,indent=2)+'\n')
# All tested choices and cancellations retain the original visible response.
for values in comparison.values():
 if not all(values.values()):raise SystemExit('Menu selection regression')
