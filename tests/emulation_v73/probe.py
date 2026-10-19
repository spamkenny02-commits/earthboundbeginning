"""Controlled NPC 898 lodging entry, real rest transition, linked post-rest revisit."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
CASES={
 'decline':{'state':'initial_v33','steps':[['A'],['A'],['Right','A'],['A'],['A']],'wait':0,'status':False,'save':False},
 'accept':{'state':'initial_v33','steps':[['A']]*6,'wait':600,'status':True,'save':True},
 'revisit':{'state':'accept','steps':[['A']]*3,'wait':0,'status':False,'save':False},
}
TRIGGER=['A','Right','A','A','A']
def run(args):
 p=args.profile;source=args.rom.read_bytes();initial=(args.states_dir/p/'after_combat.state').resolve();handoff=None
 report={'version':'v73','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(initial.read_bytes()),'npc_id':898,'entry':'37899B','natural_scene_access_verified':False,'rest_and_warp_called_by_tester':False,'wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  state=initial if cfg['state']=='initial_v33' else handoff;assert state and state.exists();input_sha=b.sha(state.read_bytes());s=ServiceSession(source,args.core,args.out/p/name,p,[0x37899B],args.version);captures=[];saved=None
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in TRIGGER:s.tap(key)
   s.step(180);captures.append(s.capture('page_00'))
   for i,keys in enumerate(cfg['steps'],1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'page_{i:02d}'))
   if cfg['wait']:s.step(cfg['wait']);captures.append(s.capture('rest_settled'))
   if cfg['status']:
    s.tap('A');s.step(180);captures.append(s.capture('status_after_rest'));s.tap('B');s.step(180);captures.append(s.capture('map_after_status'))
   if cfg['save']:saved=Path(s.send({'save':'handoff'})['state']);handoff=saved
   data={'entries':['37899B'],'operations':[],'trigger':TRIGGER,'steps':cfg['steps'],'settle_frames':cfg['wait'],'status_buttons':['A','B'] if cfg['status'] else [],'state_source':cfg['state'],'input_state_sha256':input_sha,'output_state_sha256':b.sha(saved.read_bytes()) if saved else None,'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  data['returncode']=s.proc.returncode;report['cases'][name]=data;print(p,args.version,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(71,73),type=int,default=73);run(ap.parse_args())
