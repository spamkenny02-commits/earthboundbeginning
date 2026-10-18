"""Translate four remaining bank prompts in place, based on V61.
V62 and V63 are audit-only releases. No code, pointer or storage allocation.
"""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
CONFIG=[
 ('0680A6','0680B0','0680C0','@Please insert your ATM card.','@Mets ta carte.'),
 ('382448','38247B','382486','@Balance: $','@Solde : $'),
 ('3824A2','3824A7','3824D0','@Please enter the amount of your deposit.','@Saisis le montant de ton dépôt.'),
 ('3824A2','3824D2','3824DD','@Balance: $','@Solde : $'),
]
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA
 dic=b.dictionary_from_rom(source);old=json.loads((ROOT/'tools/v61/validation_v61.json').read_text())
 profiles={};fixtures={'version':'v64','base':'v61','edits':[]}
 for p in ('accents','ascii'):
  prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes();assert b.sha(prior)==old['profiles'][p]['sha256']
  base=b.apply(source,b.records(prior));assert b.sha(base)==old['profiles'][p]['target_rom_sha256'];changes=[];contexts={}
  for i,(root,start,end,en,fr) in enumerate(CONFIG):
   r,a,z=map(lambda x:int(x,16),(root,start,end));parsed=b.parse(base,r,8192,extra_glyphs=range(0xB0,0xC0));assert not parsed['error'] and parsed['terminal']
   assert (a-r,z-r) in b.spans_fr(base[r:parsed['end']]);raw=base[a:z];assert b.decode(raw,dic)==en
   encoded=b.encode(fr,p);assert len(encoded)<=len(raw);encoded+=b.encode(' ',p)*(len(raw)-len(encoded));changes.append((a,encoded));contexts[r]=parsed['end']
   if p=='accents':fixtures['edits'].append({'context':root,'offset':start,'end':end,'english':en,'french':fr,'profiles':{}})
   fixtures['edits'][i]['profiles'][p]={'baseline_hex':raw.hex(),'replacement_hex':encoded.hex(),'trailing_padding_bytes':len(raw)-len(b.encode(fr,p))}
  ips=b.append(prior,changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  assert b.records(ips)==b.records(prior)+changes
  for a,z in contexts.items():assert b.commands(base[a:z])==b.commands(target[a:z])
  assert b.sprite_digest(base)==b.sprite_digest(target)
  out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/f'EarthBound_Beginnings_FR_v64_{p}.ips').write_bytes(ips)
  profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes),'prior_records_preserved':len(b.records(prior))}
 plan={'version':'v64','input_patch_version':'v61','source_sha256':b.sha(source),'changed_text_spans':4,'contexts_changed':3,'commands_preserved':True,'pointers_rewritten':0,'new_allocations':0,'sprite_digest_preserved_against':'v61','natural_service_location_access_verified':False,'profiles':profiles}
 for name,value in [('v64_fixtures',fixtures),('validation_v64',plan)]:
  (ROOT/f'tools/v64/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
