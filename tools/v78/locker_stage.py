"""Translate placed school lockers after normal Examine/Use interaction was observed."""
import json
from pathlib import Path
from build_v78 import ROOT,b
ENTRIES=[
 ('06F8D9','06F8D9','06F8E4','@This one is locked.','@Verrouillé'),
 ('06FA0C','06FA14','06FA24',' opened the locker using the ',' ouvre avec la '),
 ('06FA2E','06FA30','06FA38','@There was a ','@Objet: '),
 ('06FA2E','06FA3B','06FA42',' in the locker.','.'),
 ('06FA2E','06FA5D','06FA61',' got it.'," l'a"),
 ('06FA68','06FA6B','06FA8E',"@(The key is bent and doesn't fit into the key hole!)",'@(Clé tordue : ça coince !)'),
 ('06FA93','06FA93','06FAB2','@(Unfortunately, there is nothing in this locker.)','@(Ce casier est vide.)'),
 ('06FAB4','06FAB4','06FAC9','@However, you already have too many things to carry.',"@Ton sac est plein."),
 ('06FAB4','06FAD6','06FAE3',' left it in the locker.',' le laisse.'),
]
NPCS={606:0x38E350,608:0x38E2C2,609:0x38E309,612:0x38E397,613:0x38E397,616:0x38E397}
def qualification(data):
 table=int.from_bytes(data[0x2261:0x2264],'little')-0xC00000;assert 0<=table<len(data)-2560;placements=[]
 for sector in range(1280):
  short=int.from_bytes(data[table+2*sector:table+2*sector+2],'little')
  if not short:continue
  a=0xF0000|short;n=int.from_bytes(data[a:a+2],'little');assert n<=1584 and a+2+4*n<=len(data)
  for z in range(a+2,a+2+4*n,4):
   npc=int.from_bytes(data[z:z+2],'little')
   if npc in NPCS:placements.append({'npc':npc,'sector':sector,'operand':f'{z:06X}','x':data[z+3],'y':data[z+2]})
 assert {v['npc'] for v in placements}==set(NPCS) and {v['npc'] for v in placements if v['sector']==823}==set(NPCS)
 rows=[]
 for npc,root in NPCS.items():
  a=0x2021A8+17*npc;assert data[a+9:a+13]==b.pointer(0x06F8D9) and data[a+13:a+17]==b.pointer(root);rows.append({'npc':npc,'primary':'06F8D9','secondary':f'{root:06X}','secondary_operand':f'{a+13:06X}'})
 return {'placement_pointer_operand':'002261','placement_table':f'{table:06X}','placements':placements,'npc_rows':rows,'initial_access':'native warp D1 to school hallway; then existing door and controller Examine/Use; no direct locker entry call','natural_initial_map_access_verified':False,'format_sources':[
  'https://github.com/pk-hack/CoilSnake/blob/master/coilsnake/modules/eb/MapSpriteModule.py',
  'https://github.com/pk-hack/CoilSnake/blob/master/coilsnake/model/eb/map_sprites.py']}
def extend(source,out,plan,fixtures):
 out=Path(out);dic=b.dictionary_from_rom(source);f={'entries':[dict(zip(('context','offset','end','en','fr'),e)) for e in ENTRIES],'qualification':None,'profiles':{}};profiles={}
 for p in ('accents','ascii'):
  prior=(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();base=b.apply(source,b.records(prior));proof=qualification(base)
  if f['qualification'] is None:f['qualification']=proof
  else:assert f['qualification']==proof
  indices=[b.pointer_index(v) for v in (source,base)];changes=[];contexts={}
  for e in f['entries']:
   root,a,z=(int(e[k],16) for k in ('context','offset','end'));q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));assert q['terminal'] and not q['error'];assert (a-root,z-root) in b.spans_fr(base[root:q['end']]);assert b.decode(base[a:z],dic)==e['en'];assert not any(a<t<z for ix in indices for t in ix);raw=b.encode(e['fr'],p);assert len(raw)<=z-a,(e['offset'],len(raw),z-a);raw+=b.encode(' ',p)*(z-a-len(raw));changes.append((a,raw));contexts[root]=q['end']
  ips=b.append(prior,changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for root,z in contexts.items():assert b.commands(base[root:z])==b.commands(target[root:z])
  assert b.sprite_digest(base)==b.sprite_digest(target)
  for a,z in ((0x250000,0x260000),(0x2021A8,0x2021A8+1584*17),(0x330FC0,0x331000)):assert target[a:z]==base[a:z]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);f['profiles'][p]={'input_records_added':plan['profiles'][p]['records_added'],'input_patch_sha256':b.sha(prior),'input_rom_sha256':b.sha(base),'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]};profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)}
 fixtures['locker']=f;plan.update(profiles=profiles,distinct_new_translations=plan['distinct_new_translations']+9,changed_text_spans=plan['changed_text_spans']+9,locker_new_distinct=9)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
