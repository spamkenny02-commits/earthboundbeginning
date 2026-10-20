"""Translate residual help text only for items referenced by custom shop stocks.

The seven-byte stock layout is calibrated against the displayed pharmacy list:
A5 (20 dollars), 07 (148), 6D (294), 95 (20), 96 (89). Other rows are linked to
the original typed 1A 06 command and a custom NPC wrapper. This establishes a
script/data path, not a natural encounter. Interior references remain guarded.
"""
import collections,json
from pathlib import Path
from build_v78 import ROOT,b
CONFIG=[
 (0x38,'053D00','053D10','053D1F','@It also increases your Speed.','@Vitesse accrue'),
 (0x4A,'053F58','053F68','053F87','@It has the logo of your favorite baseball team.','@Logo de ton équipe préférée.'),
 (0x5C,'05416D','054184','054195',"@So fresh, it's still warm!",'@Frais et chaud !'),
 (0x5D,'054197','0541AE','0541C9',"@There's even a slice of your favorite cake!",'@Avec ton gâteau préféré !'),
 (0x6E,'054733','05473C','054758','@When you drink it, your PP slightly increases.','@Rend quelques PP en buvant.'),
 (0x7E,'0548FC','054905','05491C','@Use by sprinkling it over food.','@À mettre sur un plat.'),
 (0x7E,'0548FC','05491E','054937','@It tastes good with any kind of food, thereby','@Bonne avec tout plat,'),
 (0x7E,'0548FC','054939','054950','@increasing the recovery power of the food.','@renforce ses soins.'),
 (0x96,'054FA2','054FAB','054FCF','@Quickly rusts metallic enemies when used during battle.','@Rouille les ennemis métalliques.'),
 (0x96,'054FA2','054FD1','054FE7','@The enemy will take about 200 points of damage.','@Environ 200 dégâts.'),
 (0xD5,'055EBB','055ECB','055EF4',"@Wow! Look at the pine tar! It's almost all the way to the end!","@De la résine presque jusqu'au bout !"),
 (0x02,'056B5D','056B5D','056B6E','A cute teddy bear!','Un joli nounours!'),
 (0x38,'056BC0','056BC5','056BDE','@It protects you from paralysis attacks.','@Protège de la paralysie.'),
 (0x4E,'056C6D','056C6D','056C8C','@Miscellaneous equipment that can only be used by ','@Accessoire exclusif destiné à '),
 (0x76,'056D63','056D63','056D78','@To use, sprinkle over food.','@Saupoudre ton plat.'),
 (0x76,'056D63','056D7A','056D9A','@A good combination increases the strength of your recovery.','@Un bon mélange soigne mieux.'),
]
def help_path(data,root,target):
 queue=collections.deque([(root,[root])]);seen=set()
 while queue:
  r,path=queue.popleft()
  if r==target:return [f'{a:06X}' for a in path]
  if r in seen:continue
  seen.add(r);assert len(seen)<10000;p=b.parse(data,r,8192,extra_glyphs=range(0xb0,0xc0));assert not p['error'] and p['terminal']
  queue.extend((t,path+[t]) for _,t in p['refs'] if 0<t<len(data))
 raise ValueError('No typed item-help path to context')
def qualify(data,source):
 dic=b.dictionary_from_rom(source);wrappers={}
 for npc in range(1584):
  q=0x2021A8+17*npc+9;root=int.from_bytes(data[q:q+4],'little')-0xC00000
  if 0x365592<=root<0x3656DC:
   assert data[root]==4;flag=int.from_bytes(data[root+1:root+3],'little');wrappers.setdefault(flag,[]).append({'npc':npc,'entry':f'{root:06X}'})
 p=b.parse(data,0x3656DC,8192,extra_glyphs=range(0xb0,0xc0));assert p['terminal'] and not p['error'];rows=[]
 for operand,target in p['refs']:
  flag=int.from_bytes(data[operand-2:operand],'little')
  if flag not in wrappers:continue
  assert data[operand-3]==6 and data[target:target+2]==b'\x1a\x06';shop=data[target+2];a=0x1576B2+7*shop;stock=list(data[a:a+7]);rows.append({'flag':f'{flag:04X}','wrappers':wrappers[flag],'dispatch_operand':f'{operand:06X}','command':f'{target:06X}','shop_id':shop,'stock_offset':f'{a:06X}','items':[f'{i:02X}' for i in stock if i]})
 calibration=next(r for r in rows if r['shop_id']==0x10);assert calibration['items']==['A5','07','6D','95','96'];assert [int.from_bytes(data[0x155000+39*i+26:0x155000+39*i+28],'little') for i in (0xA5,7,0x6D,0x95,0x96)]==[20,148,294,20,89]
 ids=sorted({int(i,16) for r in rows for i in r['items']});items=[]
 for i in ids:
  a=0x155000+39*i;name=b.decode(data[a:a+25].split(b'\0')[0],dic);help_root=int.from_bytes(data[a+35:a+39],'little')-0xC00000;items.append({'id':f'{i:02X}','name':name,'price':int.from_bytes(data[a+26:a+28],'little'),'help_root':f'{help_root:06X}','shop_ids':sorted({r['shop_id'] for r in rows if f'{i:02X}' in r['items']})})
 return {'scope':'typed custom-NPC wrappers, flag dispatch, 1A 06 shop selector, seven-byte stock records and item-help pointers','natural_access_verified':False,'stock_stride_calibrated_against':'V78 controlled pharmacy list; five names and prices','rows':rows,'items':items}
def extend(source,out,plan,fixtures):
 out=Path(out);priors={p:(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()};qualification=qualify(bases['accents'],source);ids={int(i['id'],16):i for i in qualification['items']};indices=[b.pointer_index(source),*[b.pointer_index(d) for d in bases.values()]];eligible=[];blocked=[]
 for item,root,a,z,en,fr in CONFIG:
  assert item in ids;path=help_path(bases['accents'],int(ids[item]['help_root'],16),int(root,16));e=dict(item_id=f'{item:02X}',context=root,offset=a,end=z,en=en,fr=fr,help_path=path);lo,hi=int(a,16),int(z,16);refs=sorted({t for index in indices for t in index if lo<t<hi})
  if refs:blocked.append({**e,'reason':'unqualified interior raw reference; source span preserved','targets':[f'{t:06X}' for t in refs]})
  else:eligible.append(e)
 f={'entries':eligible,'blocked_entries':blocked,'qualification':qualification,'profiles':{}};profiles={};dic=b.dictionary_from_rom(source)
 for p,base in bases.items():
  changes=[]
  for e in eligible:
   root,a,z=(int(e[k],16) for k in ('context','offset','end'));q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));assert q['terminal'] and not q['error'];assert (a-root,z-root) in b.spans_fr(base[root:q['end']]);assert b.decode(base[a:z],dic)==e['en'];raw=b.encode(e['fr'],p);assert len(raw)<=z-a;changes.append((a,raw+b.encode(' ',p)*(z-a-len(raw))))
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for e in eligible:
   root=int(e['context'],16);end=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0))['end'];assert b.commands(target[root:end])==b.commands(base[root:end])
  assert b.sprite_digest(target)==b.sprite_digest(base) and target[0x250000:0x260000]==base[0x250000:0x260000]
  for e in blocked:
   a,z=int(e['offset'],16),int(e['end'],16);assert target[a:z]==base[a:z]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)};f['profiles'][p]={'input_patch_sha256':b.sha(priors[p]),'input_rom_sha256':b.sha(base),'input_records_added':plan['profiles'][p]['records_added'],'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]}
 existing={e['english'] for e in fixtures['profiles']['accents']['edits']}|{'No'}|{e['en'] for e in fixtures['medical']['entries']+fixtures['remaining']['entries']+fixtures['remaining']['labels']};count=len({e['en'] for e in eligible}-existing);fixtures['item_help']=f;plan.update(profiles=profiles,distinct_new_translations=plan['distinct_new_translations']+count,changed_text_spans=plan['changed_text_spans']+len(eligible),item_help_new_distinct=count,item_help_qualified_shop_items=len(ids))
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
