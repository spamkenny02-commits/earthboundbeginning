"""Used key descriptions and the native full-HP message exposed by eating."""
import json
from pathlib import Path
from build_v78 import ROOT,b
ENTRIES=[
 ('055546','05554F','055563','@The <Machine that Opens Doors,','@Cette machine ouvre'),
 ('055546','055565','055588','@especially when you have a slightly bad key> machine.','@les portes malgré une clé tordue.'),
 ('055D82','055D8B','055D9F','@A key to a regular locker.',"@Clé d'un casier."),
]
# These phrases were already translated in a scoped V43 copy. Count zero new
# sources for correcting the original native consumer exposed in this run.
CORRECTIONS=[('2F69A1','2F69A5','2F69AB',"'s HP are",' : PV'),('2F69A1','2F69AC','2F69B5','  maxed out!',' au max !')]
def extend(source,out,plan,fixtures):
 out=Path(out);dic=b.dictionary_from_rom(source);keys=('context','offset','end','en','fr');f={'entries':[dict(zip(keys,e)) for e in ENTRIES],'corrections':[dict(zip(keys,e)) for e in CORRECTIONS],'item_help_roots':{'AC':'055546','CD':'055D82'},'profiles':{}};profiles={}
 for p in ('accents','ascii'):
  prior=(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();base=b.apply(source,b.records(prior));changes=[];contexts={}
  for item,root in f['item_help_roots'].items():
   a=0x155000+39*int(item,16)+35;assert base[a:a+4]==b.pointer(int(root,16))
  for e in f['entries']+f['corrections']:
   root,a,z=(int(e[k],16) for k in ('context','offset','end'));q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));assert q['terminal'] and not q['error'];assert (a-root,z-root) in b.spans_fr(base[root:q['end']]);assert b.decode(base[a:z],dic)==e['en'];raw=b.encode(e['fr'],p);assert len(raw)<=z-a,(e,len(raw),z-a);changes.append((a,raw.ljust(z-a,b.encode(' ',p))));contexts[root]=q['end']
  ips=b.append(prior,changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for root,z in contexts.items():assert b.commands(base[root:z])==b.commands(target[root:z])
  assert b.sprite_digest(base)==b.sprite_digest(target);assert target[0x155000:0x155000+39*254]==base[0x155000:0x155000+39*254]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);f['profiles'][p]={'input_records_added':plan['profiles'][p]['records_added'],'input_rom_sha256':b.sha(base),'input_patch_sha256':b.sha(prior),'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]};profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)}
 fixtures['locker_help']=f;plan.update(profiles=profiles,distinct_new_translations=plan['distinct_new_translations']+3,changed_text_spans=plan['changed_text_spans']+3,locker_help_new_distinct=3,native_hp_corrections_not_counted=2)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
