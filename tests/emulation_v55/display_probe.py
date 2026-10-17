"""Compare V54/V55 transport choices using declared temporary ROM routing."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v55'))
from build_v55 import ROM_SHA,sha,apply,records,pointer
SLOT=0x368B51
# name, root, A presses before menu, navigation, confirmation
STATIONS=[('podunk','33F0CF',('33F182','33F1A4')),('merry','355558',('35560D','355631')),('reindeer','363D16',('363DC8','363DEA')),('snowman','3781AA',None)]
CASES=[(name+'_'+str(i),root,2,['Down']*i,'A',gate if i==3 else None) for name,root,gate in STATIONS for i in range(4)]+[(name+'_cancel',root,2,[],'B',None) for name,root,gate in STATIONS]
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
ap.add_argument('--intro-only',action='store_true')
args=ap.parse_args();
if args.intro_only:CASES=[('snowman_intro','3781AA',0,[],'A',None)]
source=args.rom.read_bytes();assert sha(source)==ROM_SHA
summary={'method':'controlled_bank_card_routing_comparing_original_and_translated_menu_selections','rom_modified_for_probe':True,'wram_modified_for_probe':False,'pointer_slot':f'{SLOT:06X}','core_sha256':sha(args.core.read_bytes()),'natural_scene_access_verified':False,'versions':{}}
for version in ((55,) if args.intro_only else (54,55)):
 plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());profiles={}
 for profile in ('accents','ascii'):
  base=apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes()));assert sha(base)==plan['profiles'][profile]['target_rom_sha256'];cases={}
  for name,root,advances,navigation,confirmation,gate in CASES:
   out=(args.out/f'v{version}'/profile/name).resolve();out.mkdir(parents=True,exist_ok=True)
   dest=int.from_bytes(base[int(root[4:],16):int(root[4:],16)+4],'little')-0xC00000 if root.startswith('npc:') else int(root,16)
   fixture=bytearray(base);fixture[SLOT:SLOT+4]=pointer(dest)
   allowed=set(range(SLOT,SLOT+4))
   if gate:
    g,t=map(lambda v:int(v,16),gate);assert base[g:g+7]==b'\x06\x39\x03'+pointer(t);fixture[g:g+5]=b'\x0a'+pointer(t);allowed.update(range(g,g+5))
   assert all(a==b for i,(a,b) in enumerate(zip(base,fixture)) if i not in allowed)
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
   cases[name]={'base_rom_sha256':sha(base),'fixture_rom_sha256':sha(fixture),'target':f'{dest:06X}','navigation':navigation,'confirmation':confirmation,'only_declared_routing_and_optional_gate_changed':True,'optional_gate_forced':bool(gate),'returncode':proc.returncode,'captures':captures}
   print(version,profile,name,'completed',flush=True)
  profiles[profile]=cases
 summary['versions'][str(version)]=profiles
(args.out/'display_results.json').write_text(json.dumps(summary,indent=2)+'\n')
