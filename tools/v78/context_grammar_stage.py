"""Qualified shared pronouns and French caller corrections, with no allocation.

Plural helpers return after their new word, before zero-filled unreachable tails.
Possessive originals stay intact; their two callers use an existing empty return
because the French sentence already includes notre. No global helper deletion.
"""
import json
from pathlib import Path
from build_v78 import ROOT,b
from item_help_stage import help_path
PRONOUNS=[
 dict(context='387B19',offset='387B2B',end='387B2E',en='you',fr='toi'),
 dict(context='387B2F',offset='387B2F',end='387B36',en='you all',fr='vous'),
 dict(context='387B37',offset='387B37',end='387B3E',en='you two',fr='vous'),
]
FRENCH=[
 dict(context='32FCA0',offset='32FCA0',end='32FCB9',en='@Mon fils se nomme aussi ',fr='@Fiston se nomme comme ',mode='short_bridge'),
 dict(context='369D9B',offset='369DD7',end='369DD8',en='l',fr='L'),
 dict(context='369E9E',offset='369EA8',end='369EA9',en='l',fr='L'),
]
CALLERS=[('369D9B','369DD2'),('369E9E','369EA3')]
EMPTY=0x38B550
def extend(source,out,plan,fixtures):
 out=Path(out);priors={p:(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()};dic=b.dictionary_from_rom(source);indices=[b.pointer_index(v) for v in (source,*bases.values())];qualified=[]
 for npc,roots in ((586,(0x32FCA0,0x387B19,0x387B2F,0x387B37)),(1157,(0x369D9B,0x369E9E))):
  operand=0x2021A8+17*npc+9;root=int.from_bytes(bases['accents'][operand:operand+4],'little')-0xC00000
  qualified.append({'npc':npc,'operand':f'{operand:06X}','root':f'{root:06X}','paths':[help_path(bases['accents'],root,r) for r in roots]})
 assert indices[1][0x387B19]==[0x33FC4D] and bases['accents'][0x33FC4C]==8
 assert indices[1][0x387AA2]==[int(a,16) for _,a in CALLERS]
 for e in PRONOUNS+FRENCH:
  a,z=int(e['offset'],16),int(e['end'],16)+(5 if e.get('mode')=='short_bridge' else e in PRONOUNS)
  assert not any(a<t<z for ix in indices for t in ix),(e['offset'],'interior reference')
 profiles={};f={'entries':PRONOUNS,'french_corrections':FRENCH,'possessive_callers':[{'context':r,'operand':a} for r,a in CALLERS],'empty_return':f'{EMPTY:06X}','qualified_npcs':qualified,'profiles':{}}
 for p,base in bases.items():
  assert base[EMPTY]==2;changes=[]
  for e in PRONOUNS:
   root,a,z=(int(e[k],16) for k in ('context','offset','end'));q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));assert q['terminal'] and not q['error'];assert b.decode(base[a:z],dic)==e['en'] and base[z]==2;raw=b.encode(e['fr'],p)+b'\x02';assert len(raw)<=z+1-a;changes.append((a,raw+bytes(z+1-a-len(raw))))
  for e in FRENCH:
   a,z=int(e['offset'],16),int(e['end'],16);assert b.decode(base[a:z],dic)==e['en'];raw=b.encode(e['fr'],p)
   if e.get('mode')=='short_bridge':
    assert base[z:z+5]==b'\x0a'+b.pointer(0x33FC4C) and len(raw)<z-a;raw+=base[z:z+5]+bytes(z-a-len(raw))
   else:assert len(raw)==z-a
   changes.append((a,raw))
  for r,a in CALLERS:
   root,operand=int(r,16),int(a,16);q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));assert (operand,0x387AA2) in q['refs'] and base[operand-1]==8;changes.append((operand,b.pointer(EMPTY)))
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for e in PRONOUNS:
   root=int(e['context'],16);old=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));new=b.parse(target,root,8192,extra_glyphs=range(0xb0,0xc0));assert new['terminal'] and not new['error'];assert b.commands(base[root:old['end']])==b.commands(target[root:new['end']])
  normalized=bytearray(target)
  for _,a in CALLERS:
   operand=int(a,16);normalized[operand:operand+4]=base[operand:operand+4]
  for e in FRENCH:
   root=int(e['context'],16);q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));n=b.parse(normalized,root,8192,extra_glyphs=range(0xb0,0xc0));assert n['terminal'] and not n['error'];assert b.commands(base[root:q['end']])==b.commands(normalized[root:n['end']])
  assert target[0x387AA2:0x387AB8]==base[0x387AA2:0x387AB8];assert b.sprite_digest(target)==b.sprite_digest(base) and target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000];assert target[0x2021A8:0x2021A8+1584*17]==base[0x2021A8:0x2021A8+1584*17]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)};f['profiles'][p]={'input_patch_sha256':b.sha(priors[p]),'input_rom_sha256':b.sha(base),'input_records_added':plan['profiles'][p]['records_added'],'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]}
 fixtures['context_grammar']=f;plan.update(profiles=profiles,distinct_new_translations=plan['distinct_new_translations']+3,changed_text_spans=plan['changed_text_spans']+3,context_grammar_new_distinct=3,context_grammar_french_corrections=3)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
