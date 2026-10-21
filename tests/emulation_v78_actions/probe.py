"""Native item actions and locker retry; declared temporary native preparation."""
import argparse,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
spec=importlib.util.spec_from_file_location('locker_paths',ROOT/'tests/emulation_v78_lockers/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
TRIGGER=m.TRIGGER
def action(name,*keys):return {'name':name,'keys':list(keys)}
OPEN=[action('inventory','A','Right','A'),action('action_menu','Right','A')]
CASES={
 'paper_locker':{'operations':[('give',0xAC),('warp',0xD1)],'steps':m.actions({'left_frames':22,'after_use_pages':3}),'scope':'native warp D1; existing door; native Examine/Use on placed NPC606; paper received'},
 'retry_locker':{'operations':[('give',0xAC)]+[('give',0x58)]*12+[('warp',0xD1)],'steps':m.actions({'left_frames':58,'after_use_pages':4})+[
  action('eat_menu','Down','A'),action('eat_result','Down','A'),action('hp_result','A'),action('eat_close','A'),action('retry_bag','A','Right','A'),action('retry_action','Right','A'),action('retry_open','A'),action('retry_content','A'),action('retry_receive','A'),action('retry_map','A'),action('retry_inventory','A','Right','A')],'scope':'native warp D1; placed NPC608; bag full with twelve cookies; ordinary Eat frees one slot then ordinary Use recovers rocket'},
 'help_machine':{'operations':[('give',0xAC)],'steps':OPEN+[action('help_00','Down','Down','Down','Down','A'),action('help_01','A'),action('help_02','A')],'scope':'native item action Help on granted Machine AC; original item help pointer; no help root called directly'},
 'help_key':{'operations':[('give',0xCD)],'steps':OPEN+[action('help_00','Down','Down','Down','Down','A'),action('help_01','A')],'scope':'native item action Help on granted key CD; original item help pointer; no help root called directly'},
 'drop_paper':{'operations':[('give',0x49)],'steps':OPEN+[action('drop_result','Down','Down','Down','A'),action('drop_close','A'),action('drop_back','B'),action('inventory_after','A','Right','A')],'scope':'ordinary Drop of granted paper49; final inventory inspected'},
 'give_paper':{'operations':[('join',2),('give',0x49)],'steps':[action('inventory','A','Right','A'),action('action_menu','A','Right','A'),action('give_target','Down','Down','A'),action('give_result','Right','A'),action('give_close','A'),action('inventory_ninten','A'),action('inventory_ana','Right')],'scope':'ordinary Give of granted paper49 to Ana; native join02 preparation; both final inventories inspected'},
}
def run(args):
 source=args.rom.read_bytes();p=args.profile;initial=args.states_dir/p/'accept/handoff.state';report={'version':'v78','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(initial.read_bytes()),'natural_scene_access_verified':False,'wram_written_directly_by_tester':False,'target_scripts_called_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  s=ServiceSession(source,args.core,args.out/p/name,p,[0x38B550],args.version,cfg['operations']);caps=[]
  try:
   s.send({'load':str(initial.resolve()),'frames':0});s.step(60)
   for key in TRIGGER:s.tap(key)
   s.step(600);caps.append(s.capture('prepared'))
   for a in cfg['steps']:
    for key,n in a.get('move',[]):s.step(n,[key])
    for key in a.get('keys',[]):s.tap(key)
    s.step(180);caps.append(s.capture(a['name']))
   c={'entries':['38B550'],'logical_entry':'38B550','scope':cfg['scope'],'operations':cfg['operations'],'trigger':TRIGGER,'steps':cfg['steps'],'settle_frames':180,'wait_after_preparation_frames':600,'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':caps}
  finally:s.close()
  (s.out/'history.json').unlink(missing_ok=True);c['returncode']=s.proc.returncode;report['cases'][name]=c;print(p,args.version,name,s.frame,len(caps),flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);run(ap.parse_args())
