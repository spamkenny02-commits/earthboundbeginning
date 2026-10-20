"""Broaden the historical graph to custom NPCs and item-help table entries.

An operand is evidence of a reference, not proof of natural gameplay or language.
Candidates retain seed provenance so legacy/debug paths can be qualified.
"""
import argparse,collections,json,re,sys
from pathlib import Path
from build_v78 import ROOT,b
from parser_v62 import length
PATTERN=r"\b(the|you|your|please|what|with|where|have|don't|can't|it's|i'm|does|will|would|should|this|that|which|was|were|said|are|some|cannot|their|anyone|someone|yes|no|select|choose|starting|who|want|look|cool|watch)\b"
def audit(source,data):
 seeds={}
 def seed(root,label):
  if 0<root<len(data):seeds.setdefault(root,[]).append(label)
 for npc in range(1584):
  for field in (9,13):
   q=0x2021A8+17*npc+field;root=int.from_bytes(data[q:q+4],'little')-0xC00000;old=int.from_bytes(source[q:q+4],'little')-0xC00000
   if 0x330000<=root<0x3F0000 or root!=old:seed(root,f'NPC:{npc}:{field}')
 for q in range(0x368215,0x369549,12):seed(int.from_bytes(data[q:q+4],'little')-0xC00000,f'ACTION:{q-4:06X}')
 for item in range(254):
  q=0x155000+39*item+35;seed(int.from_bytes(data[q:q+4],'little')-0xC00000,f'ITEM_HELP:{item:02X}')
 queue=collections.deque(sorted(seeds));seen=set();edges=[];failed=[];spans={};parent={r:None for r in seeds};dic=b.dictionary_from_rom(source)
 while queue:
  root=queue.popleft()
  if root in seen:continue
  seen.add(root);p=b.parse(data,root,8192,extra_glyphs=range(0xB0,0xC0))
  if p['error'] or not p['terminal']:failed.append({'root':f'{root:06X}','error':p['error'] or 'not terminal'});continue
  raw=data[root:p['end']];local=b.spans_fr(raw);cursor=0;bad=False
  for a,z in [*local,(len(raw),len(raw))]:
   pos=cursor
   while pos<a:
    if raw[pos]==9 and raw[pos+1]>64:bad=True;break
    pos+=length(raw,pos)
   if bad:break
   cursor=z
  if bad:failed.append({'root':f'{root:06X}','error':'branch table exceeds 64 entries'});continue
  for a,z in local:
   text=b.decode(raw[a:z],dic)
   if re.search(PATTERN,text,re.I):spans.setdefault((root+a,root+z),{'offset':f'{root+a:06X}','end':f'{root+z:06X}','context':f'{root:06X}','text':text,'unchanged_from_original':data[root+a:root+z]==source[root+a:root+z]})
  for operand,target in p['refs']:
   edges.append((root,operand,target))
   if 0<target<len(data):
    if target not in parent:parent[target]=root
    queue.append(target)
 for e in spans.values():
  root=int(e['context'],16);path=[root]
  while parent.get(root) is not None:root=parent[root];path.append(root)
  e['seed_labels']=seeds.get(root,[]);e['path']=[f'{r:06X}' for r in reversed(path)]
 return {'version':'v78','scope':'custom/rewritten NPC pointers, action table and 254 item-help fields; parsed closure','seed_count':len(seeds),'visited_roots':len(seen),'parsed_edges':len(edges),'candidate_count':len(spans),'natural_access_verified':False,'language_classification_verified':False,'pattern':PATTERN,'candidates':sorted(spans.values(),key=lambda e:e['offset']),'unparsed_roots':failed}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);a=ap.parse_args();source=a.rom.read_bytes();assert b.sha(source)==b.ROM_SHA;plan=json.loads((ROOT/'tools/v78/validation_v78.json').read_text());ips=(ROOT/'patches/EarthBound_Beginnings_FR_v78_accents.ips').read_bytes();assert b.sha(ips)==plan['profiles']['accents']['sha256'];data=b.apply(source,b.records(ips));r=audit(source,data);(ROOT/'tools/v78/active_text_candidates.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print({k:r[k] for k in ('seed_count','visited_roots','candidate_count')});print('unparsed',len(r['unparsed_roots']))
