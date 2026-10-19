"""Controlled phone order followed by native timed courier arrival and controller choices."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
CASES={
 'deliver_three':{'items':[0x70,0x71,0x72],'badges':0,'spend':0,'courier':[['A']]*6},
 'no_money':{'items':[0x70,0x71,0x72],'badges':0,'spend':20,'courier':[['A']]*6},
 'decline_return':{'items':[0x70,0x71,0x72],'badges':0,'spend':0,'courier':[['A']]*4+[['Right','A']]+[['A']]*3},
 'decline_return_refused':{'items':[0x70,0x71,0x72],'badges':0,'spend':0,'courier':[['A']]*4+[['Right','A'],['A'],['Right','A']]+[['A']]*3},
 'partial_two':{'items':[0x70,0x71,0x72],'badges':11,'spend':0,'courier':[['A']]*8},
 'partial_one':{'items':[0x70,0x71],'badges':12,'spend':0,'courier':[['A']]*8},
 'no_room':{'items':[0x70],'badges':13,'spend':0,'courier':[['A']]*6},
}
def phone_steps(count):
 common=[['A'],['Down','A']]+[['A']]*17+[['Right','A']]
 return common+([['A']]*15 if count==3 else [['A']]*6+[['Right','A']]+[['A']]*5 if count==2 else [['A']]*3+[['Right','A']]+[['A']]*5)
def operations(cfg):return [('store',x) for x in cfg['items']]+[('give',1)]*cfg['badges']+([('spend',cfg['spend'])] if cfg['spend'] else [])
def run(args):
 p=args.profile;source=args.rom.read_bytes();state=(args.states_dir/p/'after_combat.state').resolve();report={'version':'v70','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'initial_phone_access_forced':True,'courier_script_called_by_tester':False,'courier_arrival':'native timed delivery after controller phone order','wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  if args.case and args.case!=name:continue
  ops=operations(cfg);steps=phone_steps(len(cfg['items']));s=ServiceSession(source,args.core,args.out/p/name,p,[0x35C597],args.version,operations=ops);captures=[]
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in ('A','Right','A','A','A'):s.tap(key)
   s.step(180);captures.append(s.capture('phone_00'))
   for i,keys in enumerate(steps,1):
    for key in keys:s.tap(key)
    s.step(180)
    if i==1 or i>=19:captures.append(s.capture(f'phone_{i:02d}'))
   s.step(600);captures.append(s.capture('courier_00'))
   for i,keys in enumerate(cfg['courier'],1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'courier_{i:02d}'))
   for key in ('A','Right','A','A'):s.tap(key)
   s.step(180);captures.append(s.capture('inventory_after'))
   case={'operations':ops,'entries':['35C597'],'phone_steps':steps,'courier_steps':cfg['courier'],'wait_after_phone_frames':600,'inventory_trigger':['A','Right','A','A'],'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  case['returncode']=s.proc.returncode;report['cases'][name]=case;print(p,args.version,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(67,70),type=int,default=70);ap.add_argument('--case',choices=CASES);run(ap.parse_args())
