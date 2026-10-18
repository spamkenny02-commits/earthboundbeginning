"""Exercise full service scripts through a declared temporary action redirection.
Service entry is controlled; menu branches and their effects use the real engine.
No direct WRAM writes. This does not prove natural access to the service location.
"""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v64'))
from session import Session,b
CASES={
 'atm_insert_card':(0x0680B0,[], 'isolated_prompt'),
 'atm_empty_withdrawal':(0x0680A6,[['A'],['A'],['A']], 'full_service'),
 'atm_deposit_one':(0x0680A6,[['A'],['Right','A'],['A'],['A'],['Up','A'],['A']], 'full_service'),
 'atm_deposit_too_much':(0x0680A6,[['A'],['Right','A'],['A'],['A'],['Left','Up','Up','Up','A']], 'full_service'),
 'atm_cancel':(0x0680A6,[['A'],['B']], 'full_service'),
 'atm_withdrawal_prompt':(0x382448,[['A'],['A']], 'isolated_prompt'),
 'phone_dad_save':(0x35C597,[['A']]*10, 'full_service'),
 'phone_mom':(0x35C597,[['A'],['Down','A'],['A'],['A']], 'full_service'),
 'phone_cancel':(0x35C597,[['A'],['B']], 'full_service'),
 'shop_buy':(0x365592,[['A'],['A'],['A'],['A']], 'full_service'),
 'shop_insufficient_cash':(0x365592,[['A'],['A'],['Down','A'],['A']], 'full_service'),
 'storage_refuses_card':(0x34B490,[['A'],['A'],['A'],['A']], 'full_service'),
 'storage_empty_withdrawal':(0x34B490,[['A'],['Right','A']], 'full_service'),
}
def run(args):
 source=args.rom.read_bytes();p=args.profile;summary={'version':'v64','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'method':'controlled service entry followed by controller-only branches; live next-byte cursors sampled per frame','natural_service_location_access_verified':False,'wram_written_directly_by_tester':False,'cases':{}}
 state=(args.states_dir/p/'after_combat.state').resolve();summary['initial_state_sha256']=b.sha(state.read_bytes())
 for name,(entry,steps,kind) in CASES.items():
  if args.case and args.case!=name:continue
  s=Session(source,args.core,args.out/p/name,p,entry,args.version);captures=[]
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in ('A','Right','A','A','A'):s.tap(key)
   s.step(180);captures.append(s.capture('page_00'))
   for i,keys in enumerate(steps,1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'page_{i:02d}'))
   assert s.routing==[{'offset':'368B51','old':s.data[0x368B51:0x368B55].hex(),'new':b.pointer(entry).hex()}]
   case={'entry':f'{entry:06X}','kind':kind,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'temporary_routing':s.routing,'only_declared_routing_changed':True,'steps':steps,'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  case['returncode']=s.proc.returncode;assert case['returncode']==0
  summary['cases'][name]=case;print(p,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--case',choices=CASES);ap.add_argument('--version',type=int,choices=(61,64),default=64)
 run(ap.parse_args())
