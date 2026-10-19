"""Canary NPC root and explicitly forced melody branch; no direct WRAM writes."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import ServiceSession,b
CASES={
 'no_canary':{'entry':0x3861D3,'give':False,'steps':[['A']]*2,'scope':'complete NPC entry, no canary'},
 'canary_yes':{'entry':0x3861D3,'give':True,'steps':[['A']]*3,'scope':'complete NPC entry with native item grant'},
 'canary_no':{'entry':0x3861D3,'give':True,'steps':[['A'],['Right','A'],['A'],['A']],'scope':'complete NPC entry with native item grant'},
 'melody_yes':{'entry':0x32CC90,'give':False,'steps':[['A']]*4,'scope':'direct melody sub-branch, prerequisite flag not verified'},
 'melody_no':{'entry':0x32CC90,'give':False,'steps':[['A'],['Right','A'],['A']],'scope':'direct melody sub-branch, prerequisite flag not verified'},
}
TRIGGER=['A','Right','A','A','A']
def operations(cfg):return [('give',0xA8)] if cfg['give'] else []
def run(args):
 p=args.profile;source=args.rom.read_bytes();state=(args.states_dir/p/'accept/handoff.state').resolve();report={'version':'v75','patch_tested':f'v{args.version}','profile':p,'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'initial_state_source':'private V71 reference lodging accept handoff; Ninten after rest, 30 HP, 20 dollars, bank card','npc_id':291,'natural_scene_access_verified':False,'wram_written_directly_by_tester':False,'cases':{}}
 for name,cfg in CASES.items():
  ops=operations(cfg);s=ServiceSession(source,args.core,args.out/p/name,p,[cfg['entry']],args.version,operations=ops);captures=[]
  try:
   s.send({'load':str(state),'frames':0});s.step(60)
   for key in TRIGGER:s.tap(key)
   s.step(180);captures.append(s.capture('page_00'))
   for i,keys in enumerate(cfg['steps'],1):
    for key in keys:s.tap(key)
    s.step(180);captures.append(s.capture(f'page_{i:02d}'))
   data={'entries':[f'{cfg["entry"]:06X}'],'scope':cfg['scope'],'operations':ops,'trigger':TRIGGER,'steps':cfg['steps'],'temporary_rom_writes':s.routing,'base_rom_sha256':b.sha(s.data),'fixture_rom_sha256':b.sha(s.fixture),'sampled_frames':s.frame,'events':s.events,'pointer_frame_counts':dict(sorted(s.counts.items())),'captures':captures}
  finally:s.close()
  data['returncode']=s.proc.returncode;report['cases'][name]=data;print(p,args.version,name,s.frame,'frames',len(captures),'captures',flush=True)
 args.out.mkdir(parents=True,exist_ok=True);(args.out/f'results_{p}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(74,75),type=int,default=75);run(ap.parse_args())
