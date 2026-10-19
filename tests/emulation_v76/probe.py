"""Pippi complete entry and isolated text branches; no direct WRAM writes."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
CASES={
 'pippi_entry':{'entry':0x386B63,'steps':[['A']]*4,'scope':'complete NPC 319 entry from retained post-rest state'},
 'podunk_and_secret':{'entry':0x386BAD,'steps':[['A']]*4,'scope':'direct inner branch for dynamic name and secret'},
 'secret_only':{'entry':0x386BC9,'steps':[['A']]*3,'scope':'direct inner secret branch'},
 'morning':{'entry':0x386C58,'steps':[['A']]*2,'scope':'direct post-rest morning branch'},
}
TRIGGER=['A','Right','A','A','A']
def run(args):
 p=args.profile;source=args.rom.read_bytes();state=(args.states_dir/p/'accept/handoff.state').resolve();report={'version':'v76','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'initial_state_source':'private V71 reference lodging accept handoff; Ninten after rest, 30 HP, 20 dollars, bank card','npc_id':319,'natural_scene_access_verified':False,'wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  s=ServiceSession(source,args.core,args.out/p/name,p,[cfg['entry']],args.version);captures=[]
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in TRIGGER:s.tap(key)
   s.step(180);captures.append(s.capture('page_00'))
   for i,keys in enumerate(cfg['steps'],1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'page_{i:02d}'))
   data={'entries':[f'{cfg["entry"]:06X}'],'scope':cfg['scope'],'operations':[],'trigger':TRIGGER,'steps':cfg['steps'],'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  data['returncode']=s.proc.returncode;report['cases'][name]=data;print(p,args.version,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(75,76),type=int,default=76);run(ap.parse_args())
