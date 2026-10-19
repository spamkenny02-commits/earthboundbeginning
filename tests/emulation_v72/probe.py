"""Linked private states: native courier transfer, then controlled storage inspection."""
import argparse,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
def load_probe(v):
 spec=importlib.util.spec_from_file_location(f'probe{v}',ROOT/f'tests/emulation_v{v}/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p70=load_probe(70);p71=load_probe(71)
CASES={
 'pickup_three':{'operations':p71.operations(p71.CASES['pickup_three']),'phone':p71.phone_steps(),'courier':p71.CASES['pickup_three']['courier']},
 'partial_two':{'operations':p70.operations(p70.CASES['partial_two']),'phone':p70.phone_steps(3),'courier':p70.CASES['partial_two']['courier']},
 'partial_one':{'operations':p70.operations(p70.CASES['partial_one']),'phone':p70.phone_steps(2),'courier':p70.CASES['partial_one']['courier']},
}
TRIGGER=['A','Right','A','A','A'];INSPECT=[['A'],['Right','A'],['A']]
def run(args):
 source=args.rom.read_bytes();p=args.profile;initial=(args.states_dir/p/'after_combat.state').resolve()
 report={'audit_version':'v72','patch_tested':'v71','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(initial.read_bytes()),'natural_initial_phone_access_verified':False,'courier_script_called_by_tester':False,'storage_inspection_access_forced':True,'wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  if args.case and name!=args.case:continue
  state=initial;case={'phases':{}}
  for phase,entry,ops,steps in [('courier',0x35C597,cfg['operations'],cfg['phone']),('inspect',0x34B490,[('take',1)] if name!='pickup_three' else [],INSPECT)]:
   input_sha=b.sha(state.read_bytes());s=ServiceSession(source,args.core,args.out/p/name/phase,p,[entry],71,operations=ops);captures=[];saved=None;trigger=TRIGGER+(['A'] if phase=='inspect' and name!='pickup_three' else [])
   try:
    s.send({'load':str(state),'frames':0});s.step(60)
    for key in trigger:s.tap(key)
    s.step(180);captures.append(s.capture('page_00'))
    for i,keys in enumerate(steps,1):
     for key in keys:s.tap(key)
     s.step(180)
     if phase=='inspect' or i>=19:captures.append(s.capture(f'page_{i:02d}'))
    if phase=='courier':
     s.step(600);captures.append(s.capture('arrival'))
     for i,keys in enumerate(cfg['courier'],1):
      for key in keys:s.tap(key)
      s.step(180);captures.append(s.capture(f'courier_{i:02d}'))
     saved=Path(s.send({'save':'handoff'})['state'])
    data={'operations':ops,'entries':[f'{entry:06X}'],'trigger':trigger,'steps':steps,'courier_steps':cfg['courier'] if phase=='courier' else [],'wait_after_phone_frames':600 if phase=='courier' else 0,'state_source':'initial_v33' if phase=='courier' else 'courier','input_state_sha256':input_sha,'output_state_sha256':b.sha(saved.read_bytes()) if saved else None,'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
   finally:s.close()
   data['returncode']=s.proc.returncode;case['phases'][phase]=data
   if saved:state=saved
   print(p,name,phase,s.frame,'frames',len(captures),'captures',flush=True)
  report['cases'][name]=case
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--case',choices=CASES);run(ap.parse_args())
