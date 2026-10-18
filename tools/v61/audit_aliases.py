"""Find preserved old text entries still referenced by the parsed NPC/action graph.
A graph edge proves a parsed operand, not natural access in gameplay. Missing
edges do not rule out computed or assembly callers. No ROM is written.
"""
import argparse,collections,json,re,sys
from pathlib import Path
import build_v61 as b
from build_v48 import length
ROOT=b.ROOT

def graph(source,data,all_spans=None):
 copies=set()
 for file in (ROOT/'tools').glob('v*/validation*.json'):
  try:plan=json.loads(file.read_text())
  except (ValueError,OSError):continue
  if int(str(plan.get('version','v0')).lstrip('v') or 0)>61:continue
  for profile in plan.get('profiles',{}).values():
   if isinstance(profile,dict):
    copies.update(int(e['offset'],16) for e in profile.get('relocated',[]) if 'offset' in e)
 for version in range(51,62):
  file=ROOT/f'tools/v{version}/v{version}_fixtures.json'
  if file.exists():copies.update(int(e['copy_offset'],16) for e in json.loads(file.read_text()).get('edits',[]) if 'copy_offset' in e)
 seeds={}
 for row in range(1584):
  for field in (9,13):
   q=0x2021A8+17*row+field;t=int.from_bytes(data[q:q+4],'little')-0xC00000
   if 0x330000<=t<0x36BB00 or t in copies:seeds.setdefault(t,[]).append(f'NPC:{row}:{field}')
 for q in range(0x368215,0x369549,12):
  t=int.from_bytes(data[q:q+4],'little')-0xC00000
  if 0<t<len(data):seeds.setdefault(t,[]).append(f'ACTION:{q-4:06X}')
 queue=collections.deque(sorted(seeds));seen=set();edges=[];failed=[];spans={};paths={a:labels for a,labels in seeds.items()};dic=b.dictionary_from_rom(source)
 while queue:
  r=queue.popleft()
  if r in seen:continue
  seen.add(r);parsed=b.parse(data,r,8192,extra_glyphs=range(0xB0,0xC0))
  if parsed['error'] or not parsed['terminal']:
   failed.append({'root':f'{r:06X}','reason':parsed['error'] or 'no terminal'});continue
  raw=data[r:parsed['end']]
  try:local=b.spans_fr(raw)
  except ValueError:
   failed.append({'root':f'{r:06X}','reason':'invalid text boundary'});continue
  # Do not let a mid-instruction target reinterpret the following script as an
  # implausible 245-way jump table (notably 3508F4). Keep the exclusion explicit.
  cursor=0;bad=None
  for a,z in [*local,(len(raw),len(raw))]:
   gap=raw[cursor:a];pos=0
   while pos<len(gap):
    if gap[pos]==9 and gap[pos+1]>64:bad='branch table exceeds 64 entries';break
    pos+=length(gap,pos)
   if bad:break
   cursor=z
  if bad:failed.append({'root':f'{r:06X}','reason':bad});continue
  for lo,hi in local:
   a,z=r+lo,r+hi;text=b.decode(raw[lo:hi],dic);menu=lo>=2 and raw[lo-2:lo]==b'\x19\x02'
   if all_spans is not None and not menu:all_spans[(a,z)]={'offset':f'{a:06X}','end':f'{z:06X}','text':text,'context':f'{r:06X}','unchanged':data[a:z]==source[a:z]}
   if data[a:z]==source[a:z] and any(c.isalpha() for c in text) and not menu:
    e=spans.setdefault((a,z),{'offset':f'{a:06X}','end':f'{z:06X}','text':text,'contexts':[]});e['contexts'].append(f'{r:06X}')
  for q,t in parsed['refs']:
   edges.append((r,q,t))
   if 0<t<len(data):
    if t not in paths:paths[t]=[f'{r:06X}@{q:06X}']
    queue.append(t)
 return seeds,seen,edges,failed,spans,paths

def audit(source,data):
 all_spans={};seeds,seen,edges,failed,spans,paths=graph(source,data,all_spans);preserved=[]
 english_pattern=r"\b(the|you|your|please|what|with|where|have|don't|can't|it's|i'm|does|will|would|should|this|that|which|was|were|said|are|some|cannot|their|anyone|someone)\b"
 flags=[e for e in all_spans.values() if not e['unchanged'] and re.search(english_pattern,e['text'],re.I)]
 for version in (51,52,53,56,57,58,59):
  f=json.loads((ROOT/f'tools/v{version}/v{version}_fixtures.json').read_text())
  for e in f['edits']:
   a=int(e.get('offset',e.get('id')),16);z=int(e['end'],16)
   lo=a if e.get('mode')=='npc_copy' else a+5
   hits=[{'context':f'{r:06X}','operand':f'{q:06X}','target':f'{t:06X}'} for r,q,t in edges if lo<=t<z]
   if hits:preserved.append({'version':version,'original_start':f'{a:06X}','end':f'{z:06X}','mode':e.get('mode','entry_jump'),'parsed_command_edges':hits})
 return {'baseline':'v61','baseline_sha256':b.sha(data),'source_sha256':b.sha(source),'nonmenu_text_spans_examined':len(all_spans),'frequent_english_word_check_pattern':english_pattern,'changed_span_frequent_english_flags':flags,'word_check_is_language_proof':False,'seed_count':len(seeds),'visited_roots':len(seen),'parsed_edges':len(edges),'natural_access_verified':False,'computed_callers_covered':False,'language_classification_verified':False,'unchanged_candidates':list(sorted(spans.values(),key=lambda e:e['offset'])),'preserved_ranges_with_graph_edges':preserved,'unparsed_roots':failed,'seed_labels':{f'{k:06X}':v for k,v in seeds.items()},'paths':{f'{k:06X}':v for k,v in paths.items()}}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();source=a.rom.read_bytes();assert b.sha(source)==b.ROM_SHA;data=b.apply(source,b.records((ROOT/'patches/EarthBound_Beginnings_FR_v61_accents.ips').read_bytes()));result=audit(source,data);a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('candidates',len(result['unchanged_candidates']),'alias ranges',len(result['preserved_ranges_with_graph_edges']),'unparsed',len(result['unparsed_roots']))
 for e in result['preserved_ranges_with_graph_edges']:print(e['version'],e['original_start'],e['parsed_command_edges'])
