"""Localize the number abbreviation observed in the complete Escargo phone call."""
import json
from pathlib import Path
from build_v78 import ROOT,b
from item_help_stage import help_path
ENTRY=dict(context='35CEAA',offset='35CFFF',end='35D018',en='@No: *pssst psst pssst*  ',fr='@Num.: *pssst psst pssst*')
def extend(source,out,plan,fixtures):
 out=Path(out);dic=b.dictionary_from_rom(source);profiles={};f={'entries':[ENTRY],'profiles':{}}
 for p in ('accents','ascii'):
  prior=(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();base=b.apply(source,b.records(prior));root,a,z=(int(ENTRY[k],16) for k in ('context','offset','end'));q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));assert q['terminal'] and not q['error'];assert (a-root,z-root) in b.spans_fr(base[root:q['end']]);assert b.decode(base[a:z],dic)==ENTRY['en']
  # Phone dispatch uses native 1A 0A (computed call); its runtime trace is
  # checked separately. The hint-shop graph also provides a typed path.
  path=help_path(base,0x35A925,root)
  for data in (source,base):assert not any(a<t<z for t in b.pointer_index(data))
  raw=b.encode(ENTRY['fr'],p);assert len(raw)<=z-a;raw+=b.encode(' ',p)*(z-a-len(raw));changes=[(a,raw)];ips=b.append(prior,changes);target=b.apply(source,b.records(ips));assert b.commands(base[root:q['end']])==b.commands(target[root:q['end']]);assert b.sprite_digest(base)==b.sprite_digest(target);assert base[0x250000:0x260000]==target[0x250000:0x260000];assert base[0x330FC0:0x331000]==target[0x330FC0:0x331000]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);f['profiles'][p]={'input_records_added':plan['profiles'][p]['records_added'],'input_patch_sha256':b.sha(prior),'input_rom_sha256':b.sha(base),'phone_path':path,'records':[{'offset':f'{a:06X}','hex':raw.hex()}]};profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+1}
 fixtures['phone_label']=f;plan.update(profiles=profiles,distinct_new_translations=plan['distinct_new_translations']+1,changed_text_spans=plan['changed_text_spans']+1,phone_label_new_distinct=1)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
