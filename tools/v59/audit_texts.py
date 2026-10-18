"""Inventory unchanged, non-menu text spans reachable from V55 NPC/action seeds.

This is a conservative candidate list, including inherited and debug scripts.
Neither natural scene reachability nor English-language classification is proven.
Already modified or relocated English text may be missed by the unchanged filter.
"""
import sys,json,collections,bisect
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v58'));import build_v58 as b
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
s=args.rom.read_bytes();assert b.sha(s)==b.ROM_SHA;bases={p:b.apply(s,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v58_{p}.ips').read_bytes())) for p in ('accents','ascii')};base=bases['accents'];d=b.dictionary_from_rom(s)
# Current relocated script starts, used only to recognize NPC entry destinations.
copies=set()
for f in (ROOT/'tools').glob('v*/validation*json'):
 try:x=json.loads(f.read_text())
 except:continue
 for p in x.get('profiles',{}).values():
  if not isinstance(p,dict):continue
  for e in p.get('relocated',[]):
   if 'offset' in e:copies.add(int(e['offset'],16))
for v in range(51,59):
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
texts={}
queue=collections.deque(sorted(seeds));seen=set();contexts={};groups={};paths={r:';'.join(seeds[r]) for r in seeds}
while queue:
 r=queue.popleft()
 if r in seen or r==0x3508F4:continue
 seen.add(r);parsed=b.parse(base,r,8192,extra_glyphs=range(0xB0,0xC0))
 if parsed['error'] or not parsed['terminal'] or len(parsed['refs'])>64:continue
 raw=base[r:parsed['end']]
 try:spans=b.spans_fr(raw)
 except:continue
 for lo,hi in spans:
  a,z=r+lo,r+hi;en=b.decode(raw[lo:hi],d)
  ismenu=lo>=2 and raw[lo-2:lo]==b'\x19\x02'
  if base[a:z]==s[a:z] and any(c.isalpha() for c in en) and not ismenu:
   e=texts.setdefault((a,z),{'offset':f'{a:06X}','end':f'{z:06X}','text':en,'contexts':[]});e['contexts'].append(f'{r:06X}')
 for q,t in parsed['refs']:
  if 0<t<len(base):
   if t not in paths:paths[t]=f'{r:06X}@{q:06X}'
   queue.append(t)
args.out.write_text(json.dumps({'baseline':'v58','source_sha256':b.sha(s),'baseline_sha256':{p:b.sha(v) for p,v in bases.items()},'natural_scene_access_verified':False,'language_classification_verified':False,'excludes_already_modified_spans':True,'excluded_root':'3508F4','seed_count':len(seeds),'visited_roots':len(seen),'unchanged_nonmenu_spans':list(sorted(texts.values(),key=lambda e:e['offset'])),'paths':{f'{k:06X}':v for k,v in paths.items()}},ensure_ascii=False,indent=2))
for e in sorted(texts.values(),key=lambda e:e['offset']):print(e['offset'],e['end'],repr(e['text']),e['contexts'][:2])
