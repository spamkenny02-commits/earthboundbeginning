"""Controlled phone access, native walk outside and timed courier; linked storage checks."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
TRIGGER=['A','Right','A','A','A']
EXIT=[['Up',20],['Right',35],['Right',35],['Down',10],['Right',20],['Up',20],['Right',20],['Right',45],['Down',10],['Right',30]]
PHONE=[['A'],['Down','A']]+[['A']]*21
THREE=[['A']]*5+[['Right','A']]+[['A']]*2+[['Right','A']]+[['A']]*2+[['Right','A']]+[['A']]*5
ITEMS=[0x70,0x71,0x72,0x73]
CASES={
 'limit_three':{'state':'initial','entry':0x35C597,'operations':[('give',x) for x in ITEMS],'courier':THREE,'phone':True,'inventory':True,'save':True},
 'limit_three_inspect':{'state':'limit_three','entry':0x34B490,'operations':[],'steps':[['A'],['Right','A'],['A']]},
 'full_fill13':{'state':'initial','entry':0x38B550,'operations':[('store',0x70)]*13,'save':True},
 'full_fill26':{'state':'full_fill13','entry':0x38B550,'operations':[('store',0x70)]*13,'save':True},
 'reserve_full':{'state':'full_fill26','entry':0x35C597,'operations':[('give',x) for x in ITEMS],'post_operations':[('store',0x70)]*10,'courier':[['A']]*6,'phone':True,'inventory':True,'save':True},
 'reserve_full_inspect':{'state':'reserve_full','entry':0x34B490,'operations':[],'steps':[['A'],['Right','A'],['A'],['Down']*5+['A'],['A'],['A']]},
}
def run(args):
 p=args.profile;source=args.rom.read_bytes();initial=(args.states_dir/p/'accept/handoff.state').resolve();saved={};report={'version':'v78','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(initial.read_bytes()),'natural_scene_access_verified':False,'initial_phone_access_forced':True,'courier_script_called_by_tester':False,'courier_arrival':'native timed mechanism after complete phone order and controller walk outside','wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  state=initial if cfg['state']=='initial' else saved[cfg['state']];s=ServiceSession(source,args.core,args.out/p/name,p,[cfg['entry']],args.version,cfg['operations'],cfg.get('post_operations',[]));caps=[];handoff=None
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   if cfg.get('phone'):
    for i,(key,n) in enumerate(EXIT):s.step(n,[key]);s.step(180);caps.append(s.capture(f'exit_{i:02d}'))
   for key in TRIGGER:s.tap(key)
   s.step(180);caps.append(s.capture('page_00'))
   steps=PHONE if cfg.get('phone') else cfg.get('steps',[])
   for i,keys in enumerate(steps,1):
    for key in keys:s.tap(key)
    s.step(180)
    if not cfg.get('phone') or i>=18:caps.append(s.capture(f'page_{i:02d}'))
   if cfg.get('phone'):
    s.step(600);caps.append(s.capture('arrival'))
    for i,keys in enumerate(cfg['courier'],1):
     for key in keys:s.tap(key)
     s.step(180);caps.append(s.capture(f'courier_{i:02d}'))
   if cfg.get('inventory'):
    for key in ['A','Right','A']:s.tap(key)
    s.step(180);caps.append(s.capture('inventory_after'))
    for key in ['B','B']:s.tap(key)
    s.step(180);caps.append(s.capture('map_after'))
   if cfg.get('save'):handoff=Path(s.send({'save':'handoff'})['state'])
   c={'logical_entry':f'{cfg["entry"]:06X}','entries':[f'{cfg["entry"]:06X}'],'scope':'controlled initial phone/storage entry; native walking, courier arrival and controller choices; native preparation declared','state_source':cfg['state'],'input_state_sha256':b.sha(state.read_bytes()),'output_state_sha256':b.sha(handoff.read_bytes()) if handoff else None,'operations':cfg['operations'],'post_operations':cfg.get('post_operations',[]),'exit_route':EXIT if cfg.get('phone') else [],'trigger':TRIGGER,'steps':steps,'courier_steps':cfg.get('courier',[]),'wait_after_phone_frames':600 if cfg.get('phone') else 0,'inventory_trigger':['A','Right','A'] if cfg.get('inventory') else [],'inventory_close':['B','B'] if cfg.get('inventory') else [],'settle_frames':180,'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':caps}
  finally:s.close()
  # Raw runner history is regenerable and is never a public artifact.
  (s.out/'history.json').unlink(missing_ok=True)
  c['returncode']=s.proc.returncode;report['cases'][name]=c
  if handoff:saved[name]=handoff
  print(p,args.version,name,s.frame,'frames',len(caps),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);run(ap.parse_args())
