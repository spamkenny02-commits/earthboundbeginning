"""Inventory anchored inline menus reachable from remake NPC/action seeds in V53.

This is a conservative inventory, not proof that every seed is naturally spawned.
The builder separately validates every chosen definition and its full context.
"""
import sys,json,collections,bisect
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v53'));import build_v53 as b
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
s=args.rom.read_bytes();assert b.sha(s)==b.ROM_SHA;bases={p:b.apply(s,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v53_{p}.ips').read_bytes())) for p in ('accents','ascii')};base=bases['accents'];d=b.dictionary_from_rom(s)
# Current relocated script starts, used only to recognize NPC entry destinations.
copies=set()
for f in (ROOT/'tools').glob('v*/validation*json'):
 try:x=json.loads(f.read_text())
 except:continue
 for p in x.get('profiles',{}).values():
  if not isinstance(p,dict):continue
  for e in p.get('relocated',[]):
   if 'offset' in e:copies.add(int(e['offset'],16))
for v in (51,52,53):
 for e in json.load(open(ROOT/f'tools/v{v}/v{v}_fixtures.json'))['edits']:copies.add(int(e['copy_offset'],16))
seeds={};
for row in range(1584):
 a=0x2021A8+17*row
 for pos in (9,13):
  t=int.from_bytes(base[a+pos:a+pos+4],'little')-0xC00000
  if 0x330000<=t<0x36BB00 or t in copies:seeds.setdefault(t,[]).append(f'NPC:{row}:{pos}')
for a in range(0x368211,0x369549,12):
 t=int.from_bytes(base[a+4:a+8],'little')-0xC00000
 if t>0 and t<len(base):seeds.setdefault(t,[]).append(f'ACTION:{a:06X}')
queue=collections.deque(sorted(seeds));seen=set();contexts={};groups={};paths={r:';'.join(seeds[r]) for r in seeds}
while queue:
 r=queue.popleft()
 if r in seen or r==0x3508F4:continue
 seen.add(r);parsed=b.parse(base,r,8192,extra_glyphs=range(0xB0,0xC0))
 if parsed['error'] or not parsed['terminal'] or len(parsed['refs'])>64:continue
 raw=base[r:parsed['end']]
 try:spans=b.spans_fr(raw)
 except:continue
 options=[]
 for lo,hi in spans:
  if lo>=2 and raw[lo-2:lo]==b'\x19\x02' and raw[hi:hi+1]==b'\x02':options.append((r+lo-2,r+hi+1,b.decode(raw[lo:hi],d)))
 i=0
 while i<len(options):
  opts=[options[i]];i+=1
  while i<len(options) and opts[-1][1]==options[i][0]:opts.append(options[i]);i+=1
  if len(opts)<2:continue
  a,z=opts[0][0],opts[-1][1];key=(a,z)
  e=groups.setdefault(key,{'offset':f'{a:06X}','end':f'{z:06X}','options':[e[2] for e in opts],'contexts':[]});e['contexts'].append(f'{r:06X}')
 for q,t in parsed['refs']:
  if 0<t<len(base):
   if t not in paths:paths[t]=f'{r:06X}@{q:06X}'
   queue.append(t)
refs=sorted(set(b.pointer_index(s))|set().union(*(set(b.pointer_index(x)) for x in bases.values())))
for e in groups.values():
 a,z=int(e['offset'],16),int(e['end'],16);i=bisect.bisect_right(refs,a);e['first_interior_target']=f'{refs[i]:06X}' if i<len(refs) and refs[i]<z else None;e['guarded']=i<len(refs) and refs[i]<a+5
out=sorted(groups.values(),key=lambda e:e['offset']);args.out.write_text(json.dumps({'groups':out,'paths':{f'{k:06X}':v for k,v in paths.items()}},ensure_ascii=False,indent=2));print('SEEDS',len(seeds),'VISITED',len(seen),'GROUPS',len(out));print(collections.Counter(tuple(e['options']) for e in out));print('GUARDED',[(e['offset'],e['options'],e['first_interior_target']) for e in out if e['guarded']]);print('OTHER',[(e['offset'],e['options']) for e in out if e['options']!=['Yes','No']])
