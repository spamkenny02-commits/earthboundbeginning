"""Fixed native item-action labels: five null-terminated six-byte slots."""
import json
from pathlib import Path
from build_v78 import ROOT,b
LABELS=[('Use','Util.'),('Eat','Aval.'),('Give','Donne'),('Drop','Jette'),('Help!','Aide')]
READER=0x1369D
READER_HEX='a934e88506a9f80085089885040a65040a1865068506850ea5088510'
def extend(source,out,plan,fixtures):
 out=Path(out);f={'reader_offset':f'{READER:06X}','reader_hex':READER_HEX,'table':'38E834','stride':6,'slots':5,'entries':[{'offset':f'{0x38E834+6*i:06X}','en':en,'fr':fr} for i,(en,fr) in enumerate(LABELS)],'profiles':{}};profiles={}
 for p in ('accents','ascii'):
  prior=(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();base=b.apply(source,b.records(prior));assert base[READER:READER+len(bytes.fromhex(READER_HEX))]==bytes.fromhex(READER_HEX);writes=[]
  for e in f['entries']:
   a=int(e['offset'],16);old=b.encode(e['en'],p).ljust(6,b'\0');assert base[a:a+6]==old;raw=b.encode(e['fr'],p);assert len(raw)<=5 and b'\0' not in raw;writes.append((a,raw.ljust(6,b'\0')))
  ips=b.append(prior,writes);target=b.apply(source,b.records(ips));assert target==b.apply(base,writes)
  assert target[:0x38E834]==base[:0x38E834] and target[0x38E852:]==base[0x38E852:]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);f['profiles'][p]={'input_records_added':plan['profiles'][p]['records_added'],'input_rom_sha256':b.sha(base),'input_patch_sha256':b.sha(prior),'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in writes]};profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+5}
 fixtures['item_action']=f;plan.update(profiles=profiles,distinct_new_translations=plan['distinct_new_translations']+5,changed_text_spans=plan['changed_text_spans']+5,item_action_new_distinct=5)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
