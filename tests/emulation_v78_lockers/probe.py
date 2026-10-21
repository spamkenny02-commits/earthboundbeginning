"""Native warp preparation; existing door and ordinary Examine/item Use on placed lockers."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
TRIGGER=['A','Right','A','A','A']
CASES={
 'pickup':{'item':0xAC,'badges':0,'left_frames':58,'after_use_pages':3,'npc':608},
 'empty':{'item':0xAC,'badges':0,'left_frames':48,'after_use_pages':2,'npc':613},
 'bent':{'item':0xCD,'badges':0,'left_frames':58,'after_use_pages':1,'npc':608},
 'full':{'item':0xAC,'badges':12,'left_frames':58,'after_use_pages':4,'npc':608},
}
def actions(cfg):
 result=[{'name':'hall','move':[['Down',4]]},{'name':'room','move':[['Right',40]]},{'name':'front','move':[['Left',92]]},{'name':'position','move':[['Down',12],['Left',cfg['left_frames']],['Up',15]]}, {'name':'locked','keys':['A','Down','Down','A']},{'name':'closed','keys':['A']},{'name':'inventory_before','keys':['A','Right','A']},{'name':'action_menu','keys':['Right','A']},{'name':'use_00','keys':['A']}]
 result.extend({'name':f'use_{i:02d}','keys':['A']} for i in range(1,cfg['after_use_pages']+1))
 result.append({'name':'inventory_after','keys':['A','Right','A']})
 return result
def run(args):
 source=args.rom.read_bytes();p=args.profile;initial=(args.states_dir/p/'accept/handoff.state').resolve();report={'version':'v78','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(initial.read_bytes()),'natural_scene_access_verified':False,'initial_map_access':'native warp D1 via declared private preparation, then walking through existing door','locker_script_called_by_tester':False,'wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  operations=[('give',cfg['item'])]+[('give',1)]*cfg['badges']+[('warp',0xD1)];sequence=actions(cfg);s=ServiceSession(source,args.core,args.out/p/name,p,[0x38B550],args.version,operations);caps=[]
  try:
   s.send({'load':str(initial),'frames':0});s.step(60)
   for key in TRIGGER:s.tap(key)
   s.step(600);caps.append(s.capture('warped'))
   for action in sequence:
    for key,n in action.get('move',[]):s.step(n,[key])
    for key in action.get('keys',[]):s.tap(key)
    s.step(180);caps.append(s.capture(action['name']))
   c={'entries':['38B550'],'logical_entry':'38B550','scope':'native warp/item preparation; existing door and ordinary Examine/Use; no direct locker root call or natural initial journey certified','npc':cfg['npc'],'operations':operations,'trigger':TRIGGER,'steps':sequence,'settle_frames':180,'wait_after_preparation_frames':600,'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':caps}
  finally:s.close()
  (s.out/'history.json').unlink(missing_ok=True);c['returncode']=s.proc.returncode;report['cases'][name]=c;print(p,args.version,name,s.frame,'frames',len(caps),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);run(ap.parse_args())
