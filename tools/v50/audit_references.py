import argparse,json,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v49'));import build_v49 as b
from build_v48 import reference_proof
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);args=ap.parse_args()
src=args.rom.read_bytes();assert b.sha(src)==b.ROM_SHA;bases={p:b.apply(src,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v49_{p}.ips').read_bytes())) for p in ('accents','ascii')};idx=b.pointer_index(bases['accents']);allidx=b.pointer_index(src);f=json.loads((ROOT/'tools/v49/v49_fixtures.json').read_text());items=[]
for e in f['deferred']:
 a,z=int(e['offset'],16),int(e['end'],16);sites=[]
 for t,qs in idx.items():
  if not a<t<z:continue
  for q in qs:
   try:proof=reference_proof(bases['accents'],q,t)
   except ValueError:proof=None
   sites.append({'target':f'{t:06X}','site':f'{q:06X}','legacy_window_candidate':proof,'around':bases['accents'][q-8:q+12].hex()})
 root=int(e['context'],16);entries=[]
 for q in idx.get(root,[]):
  try:proof=reference_proof(bases['accents'],q,root)
  except ValueError:proof=None
  entries.append({'site':f'{q:06X}','legacy_window_candidate':proof})
 items.append({**e,'sites':sites,'entry_calls':entries,'accepted_for_text_edit':False,'qualification':'Unanchored byte-window candidates are not accepted pointer proofs.'})
 print(e['offset'],sites,'entries',entries)
(ROOT/'tools/v50/audit_references_v49.json').write_text(json.dumps(items,indent=2))
