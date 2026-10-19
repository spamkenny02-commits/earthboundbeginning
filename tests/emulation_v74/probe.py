"""Controlled complete NPC 87 resale service; native sale/refusal operations."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
CASES={
 'decline_entry':{'give':False,'steps':[['A'],['Right','A'],['A'],['A']],'inventory':False},
 'protected_card':{'give':False,'steps':[['A']]*5+[['Right','A'],['A']],'inventory':False},
 'sale_accept':{'give':True,'steps':[['A']]*3+[['Right','A'],['A'],['Right','A'],['A']],'inventory':True},
 'sale_decline':{'give':True,'steps':[['A']]*3+[['Right','A'],['Right','A']],'inventory':False},
}
TRIGGER=['A','Right','A','A','A']
def operations(cfg):return [('give',0x70)] if cfg['give'] else []
def run(args):
 p=args.profile;source=args.rom.read_bytes();state=(args.states_dir/p/'accept/handoff.state').resolve();report={'version':'v74','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'initial_state_source':'private V71 reference lodging accept handoff; Ninten after rest, 30 HP, 20 dollars, bank card','npc_id':87,'entry':'387221','natural_scene_access_verified':False,'wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  ops=operations(cfg);s=ServiceSession(source,args.core,args.out/p/name,p,[0x387221],args.version,operations=ops);captures=[]
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in TRIGGER:s.tap(key)
   s.step(180);captures.append(s.capture('page_00'))
   for i,keys in enumerate(cfg['steps'],1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'page_{i:02d}'))
   if cfg['inventory']:
    for key in ('A','Right','A','A'):s.tap(key)
    s.step(180);captures.append(s.capture('inventory_after'))
   data={'entries':['387221'],'operations':ops,'trigger':TRIGGER,'steps':cfg['steps'],'inventory_trigger':['A','Right','A','A'] if cfg['inventory'] else [],'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  data['returncode']=s.proc.returncode;report['cases'][name]=data;print(p,args.version,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(73,74),type=int,default=74);run(ap.parse_args())
