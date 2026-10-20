"""Batch V78 controlled NPC entry checks; rocket launch not forced."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
CASES={
 'haunted_yes':{'entry':0x36EB50,'steps':[['A']]*3},
 'haunted_no':{'entry':0x36EB50,'steps':[['Right','A'],['A']]},
 'monkey1_yes':{'entry':0x376ABE,'steps':[['A']]*3},
 'monkey1_no':{'entry':0x376ABE,'steps':[['A'],['Right','A'],['A'],['A']]},
 'monkey2_yes':{'entry':0x376BB7,'steps':[['A']]*5},
 'monkey2_no':{'entry':0x376BB7,'steps':[['A'],['Right','A'],['A']]},
 'monkey3_yes':{'entry':0x377108,'steps':[['A']]*5},
 'monkey3_no':{'entry':0x377108,'steps':[['A'],['Right','A'],['A'],['A']]},
 'sign':{'entry':0x37D45C,'steps':[['A'],['A']]},
 'rocket_no':{'entry':0x380A2A,'steps':[['Right','A']]},
 'doctor_decline':{'entry':0x381D24,'steps':[['Right','A'],['A']],'wait':300},
 'doctor_insufficient':{'entry':0x381D24,'steps':[['A']]*3,'wait':300},
 'nurse_explanation':{'entry':0x381D1C,'steps':[['A']]*8,'wait':300},
 'healer_entry':{'entry':0x381D2C,'steps':[['A']]*7,'wait':300},
 'hospital_explanation':{'entry':0x091486,'steps':[['A']]*6,'wait':300},
}
TRIGGER=['A','Right','A','A','A']
def run(args):
 p=args.profile;source=args.rom.read_bytes();state=(args.states_dir/p/'accept/handoff.state').resolve();report={'version':'v78','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'initial_state_source':'private V71 reference lodging accept handoff; Ninten after rest, 30 HP, 20 dollars, bank card','natural_scene_access_verified':False,'wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  entry=cfg['entry'];operations=cfg.get('operations',[])
  if cfg.get('copied') and args.version==78:
   f=json.loads((ROOT/'tools/v78/v78_fixtures.json').read_text());entry=int(next(n for n in f['remaining']['moved_scripts'] if int(n['root'],16)==entry)['chunks'][0]['destination'],16)
  if cfg.get('scoped_copy') and args.version==78:
   f=json.loads((ROOT/'tools/v78/v78_fixtures.json').read_text());entry=int(next(n for n in f['scoped_help']['entries'] if int(n['context'],16)==entry)['chunks'][0]['destination'],16)
  entries=cfg.get('entries',[entry]);s=ServiceSession(source,args.core,args.out/p/name,p,entries,args.version,operations);captures=[]
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in TRIGGER:s.tap(key)
   s.step(cfg.get('wait',180));captures.append(s.capture('page_00'))
   for i,keys in enumerate(cfg['steps'],1):
    for key in keys:s.tap(key)
    s.step(cfg.get('wait',180));captures.append(s.capture(f'page_{i:02d}'))
   data={'entries':[f'{a:06X}' for a in entries],'logical_entry':f'{cfg["entry"]:06X}','scope':cfg.get('scope','direct hospital explanation branch' if name=='hospital_explanation' else 'complete NPC entry forced by bank card; initial map context is not natural'),'settle_frames':cfg.get('wait',180),'operations':operations,'trigger':TRIGGER,'steps':cfg['steps'],'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  data['returncode']=s.proc.returncode;report['cases'][name]=data;print(p,args.version,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);run(ap.parse_args())
