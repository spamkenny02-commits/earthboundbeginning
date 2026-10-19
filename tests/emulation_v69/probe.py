"""Three linked controlled storage phases. V67 IPS unchanged; private states stay out."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v69'))
from service_session import ServiceSession,b
BASE_STEPS=[['A'],['A'],['A'],['Right','A'],['A'],['A'],['A'],['A'],['Right','A'],['A'],['A'],['Right','A'],['A'],['Right','A'],['A'],['A'],['Right','A'],['A']]
PHASES={
 'fill_13':{'operations':[('store',0x70)]*13,'entries':[],'trigger':['A','Right','A','A','A'],'steps':[]},
 'fill_26':{'operations':[('store',0x70)]*13,'entries':[],'trigger':['A','Right','A','A','A'],'steps':[]},
 'exercise':{'operations':[('store',0x70)]*10+[('give',0x70)],'entries':[0x34B490],'trigger':['A','Right','A','A','A'],'steps':BASE_STEPS[:5]+[['Down']*5+['A'],['A'],['A'],['Down']]+BASE_STEPS[5:]},
}
def run(args):
 source=args.rom.read_bytes();p=args.profile;state=(args.states_dir/p/'after_combat.state').resolve();previous=None
 report={'audit_version':'v69','patch_tested':'v67','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'natural_scene_access_verified':False,'wram_written_directly_by_tester':False,'method':'linked private states after service exit; native storage insertions and one item grant and complete storage script via temporary wrapper; controller branches','phases':{}}
 for name,cfg in PHASES.items():
  input_sha=b.sha(state.read_bytes());s=ServiceSession(source,args.core,args.out/p/name,p,cfg['entries'],67,operations=cfg['operations']);captures=[];saved=None
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in cfg['trigger']:s.tap(key)
   s.step(180);captures.append(s.capture('page_00'))
   for i,keys in enumerate(cfg['steps'],1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'page_{i:02d}'))
   if name!='exercise':saved=Path(s.send({'save':'handoff'})['state'])
   phase={'operations':cfg['operations'],'trigger':cfg['trigger'],'steps':cfg['steps'],'entries':[f'{a:06X}' for a in cfg['entries']],'state_source':previous or 'initial_v33','input_state_sha256':input_sha,'output_state_sha256':b.sha(saved.read_bytes()) if saved else None,'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  phase['returncode']=s.proc.returncode;report['phases'][name]=phase
  if saved:state=saved
  previous=name;print(p,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);run(ap.parse_args())
