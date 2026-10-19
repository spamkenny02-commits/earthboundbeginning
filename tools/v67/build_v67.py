"""Translate the quantity selector used by the native purchase service."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
CONFIG=[(0x37BBB0,0x37BBB8,'Just one','Un seul'),(0x37BBBB,0x37BBC3,'Multiple','En lot')]
CONTEXT=0x37BBAE
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA
 plan66=json.loads((ROOT/'tools/v66/validation_v66.json').read_text());profiles={};fixtures={'base':'v66','context':f'{CONTEXT:06X}','profiles':{}}
 for p in ('accents','ascii'):
  prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v66_{p}.ips').read_bytes();assert b.sha(prior)==plan66['profiles'][p]['sha256']
  base=b.apply(source,b.records(prior));assert b.sha(base)==plan66['profiles'][p]['target_rom_sha256']
  parsed=b.parse(base,CONTEXT,8192,extra_glyphs=range(0xB0,0xC0));assert parsed['terminal'] and not parsed['error'];edits=[];proof=[]
  for a,z,en,fr in CONFIG:
   assert (a-CONTEXT,z-CONTEXT) in b.spans_fr(base[CONTEXT:parsed['end']])
   raw=base[a:z];assert raw==b.encode(en,p);replacement=b.encode(fr,p);assert len(replacement)<=len(raw)
   replacement+=b.encode(' ',p)*(len(raw)-len(replacement));edits.append((a,replacement));proof.append({'offset':f'{a:06X}','end':f'{z:06X}','english':en,'french':fr,'baseline_hex':raw.hex(),'replacement_hex':replacement.hex()})
  ips=b.append(prior,edits);target=b.apply(source,b.records(ips));assert target==b.apply(base,edits)
  assert b.commands(base[CONTEXT:parsed['end']])==b.commands(target[CONTEXT:parsed['end']]);assert b.sprite_digest(base)==b.sprite_digest(target)
  assert base[0x250000:0x260000]==target[0x250000:0x260000]
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v67_{p}.ips').write_bytes(ips)
  fixtures['profiles'][p]=proof;profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':2}
 plan={'version':'v67','input_patch_version':'v66','source_sha256':b.sha(source),'changed_text_spans':2,'commands_preserved':True,'pointers_rewritten':0,'new_allocations':0,'sprite_digest_preserved_against':'v66','natural_service_location_access_verified':False,'profiles':profiles}
 for name,value in [('v67_fixtures',fixtures),('validation_v67',plan)]:
  (ROOT/f'tools/v67/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
