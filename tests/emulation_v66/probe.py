"""Sequential native service scripts via a temporary, declared text wrapper.
No direct WRAM changes; these tests do not establish natural map access.
"""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v65'))
from service_session import ServiceSession,b
CASES={
 'mom_pickup':([0x35C597],[['A'],['Down','A']]+[['A']]*21),
 'mom_delivery':([0x35C597],[['A'],['Down','A']]+[['A']]*17+[['Right','A']]+[['A']]*3),
 'dad_no_save':([0x35C597],[['A']]*5+[['Right','A']]+[['A']]*2),
 'paid_dad_no_save':([0x35C53A],[['A']]*5+[['Right','A']]+[['A']]*2),
 'paid_no_cash':([0x365592,0x35C53A],[['A']]*5+[['Right','A'],['A'],['A']]),
 'bank_overdraft':([0x0680A6]*2,[['A'],['Right','A'],['A'],['A'],['Up','A'],['A'],['A'],['A'],['A'],['A'],['A'],['Up','Up','A'],['A']]),
}
def run(args):
 source=args.rom.read_bytes();p=args.profile;state=(args.states_dir/p/'after_combat.state').resolve()
 report={'version':'v66','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'method':'temporary wrapper calls complete service scripts; subsequent branches use controller input','natural_scene_access_verified':False,'wram_written_directly_by_tester':False,'cases':{}}
 for name,(entries,steps) in CASES.items():
  if args.case and args.case!=name:continue
  s=ServiceSession(source,args.core,args.out/p/name,p,entries,args.version);captures=[]
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in ('A','Right','A','A','A'):s.tap(key)
   s.step(180);captures.append(s.capture('page_00'))
   for i,keys in enumerate(steps,1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'page_{i:02d}'))
   case={'entries':[f'{a:06X}' for a in entries],'steps':steps,'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  case['returncode']=s.proc.returncode;report['cases'][name]=case;print(p,args.version,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(65,66),type=int,default=66);ap.add_argument('--case',choices=CASES)
 run(ap.parse_args())
