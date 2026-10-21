"""Reuse V65's classifier-preserving neutral article at two qualified callers.

French caption/confirmation repairs are excluded from the new-source counter.
An older return copy at 32F120 remains unqualified and is not modified.
"""
import json
from pathlib import Path
from build_v78 import ROOT,b
from item_help_stage import help_path
CALLS=[(1420,0x3803F1,0x32B500,0x32B50A,0x38B551),(204,0x36B788,0x36B7D5,0x36B830,0x38B56C)]
def extend(source,out,plan,fixtures):
 out=Path(out);priors={p:(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()};indices=[b.pointer_index(v) for v in (source,*bases.values())];dic=b.dictionary_from_rom(source);neutral=int(json.loads((ROOT/'tools/v65/v65_fixtures.json').read_text())['copy_offset'],16);qualified=[]
 for npc,root,context,caller,helper in CALLS:
  operand=0x2021A8+17*npc+9;assert bases['accents'][operand:operand+4]==b.pointer(root);path=help_path(bases['accents'],root,context);q=b.parse(bases['accents'],context,8192,extra_glyphs=range(0xb0,0xc0));assert (caller,helper) in q['refs'];qualified.append(dict(npc=npc,npc_operand=f'{operand:06X}',root=f'{root:06X}',context=f'{context:06X}',caller=f'{caller:06X}',helper=f'{helper:06X}',path=path))
 for a,z in ((0x32B501,0x32B509),(0x32B511,0x32B523),(0x36B839,0x36B856),(0x36BA48,0x36BA4C)):
  assert not any(a<t<z for ix in indices for t in ix)
 withdrawal={'npc':204,'context':'36BA13','offset':'36BA48','end':'36BA4C','before':'@Le ','after':'@   ','path':help_path(bases['accents'],0x36B788,0x36BA13)}
 f={'qualified_contexts':qualified,'withdrawal_prefix':withdrawal,'neutral_helper':f'{neutral:06X}','new_source_count':0,'unqualified_return_copy_preserved':'32F120','profiles':{}};profiles={}
 for p,base in bases.items():
  helper=b.parse(base,neutral,8192,extra_glyphs=range(0xb0,0xc0));assert helper['terminal'] and not helper['error'] and helper['end']==neutral+27;assert [t for _,t in helper['refs']]==[0x38B550]*5;assert base[0x38B550]==2;changes=[]
  for _,_,_,caller,old in CALLS:
   assert base[caller-1:caller+4]==b'\x08'+b.pointer(old);assert base[neutral:neutral+6]==base[old:old+6]==b'\x1a\x0f\x00\x1f\xc0\x05';changes.append((caller,b.pointer(neutral)))
  assert b.decode(base[0x32B501:0x32B509],dic)=='@Il y a ';changes.append((0x32B501,b.encode('@Objet: ',p)))
  assert base[0x32B511:0x32B521]==b.encode(" à l'intérieur !",p) and base[0x32B521:0x32B523]==b'\x03\x02';changes.append((0x32B511,b.encode('.',p)+b'\x03\x02'+bytes(15)))
  assert base[0x36B839:0x36B856]==b.encode('  Je le garderai en lieu sûr.',p);raw=b.encode('  Cet objet sera bien gardé.',p);assert len(raw)==28;changes.append((0x36B839,raw+b.encode(' ',p)))
  # Keep the four-glyph span and every native command in place. A neutral
  # indented item label avoids the former masculine article before Fiole.
  assert base[0x36BA48:0x36BA4C]==b.encode('@Le ',p);changes.append((0x36BA48,b.encode('@   ',p)))
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes);normalized=bytearray(target)
  for _,_,_,caller,old in CALLS:normalized[caller:caller+4]=b.pointer(old)
  for root in (0x32B500,0x36B7D5,0x36BA13):
   old=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));new=b.parse(normalized,root,8192,extra_glyphs=range(0xb0,0xc0));assert old['terminal'] and new['terminal'] and not old['error'] and not new['error'];assert b.commands(base[root:old['end']])==b.commands(normalized[root:new['end']])
  assert target[0x38B52B:0x38B5A2]==base[0x38B52B:0x38B5A2];assert target[neutral:neutral+27]==base[neutral:neutral+27];assert target[0x32F120:0x32F1B2]==base[0x32F120:0x32F1B2];assert b.sprite_digest(target)==b.sprite_digest(base) and target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000];assert target[0x2021A8:0x2021A8+1584*17]==base[0x2021A8:0x2021A8+1584*17]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)};f['profiles'][p]={'input_patch_sha256':b.sha(priors[p]),'input_rom_sha256':b.sha(base),'input_records_added':plan['profiles'][p]['records_added'],'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]}
 fixtures['article_context']=f;plan.update(profiles=profiles,article_contexts_corrected=3,article_new_sources_counted=0)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
