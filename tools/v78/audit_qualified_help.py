"""Inspect original literal residues in the qualified shop-item help closure.

Original bytes and a length threshold identify candidates; they do not prove
language or global completion. Keep item provenance for manual classification.
"""
import argparse,collections,json
from pathlib import Path
from build_v78 import ROOT,b
def audit(source,data,items):
 dic=b.dictionary_from_rom(source);found={};nodes=set();errors=[]
 for item in items:
  todo=collections.deque([int(item['help_root'],16)]);seen=set()
  while todo:
   root=todo.popleft()
   if root in seen:continue
   seen.add(root);nodes.add(root);q=b.parse(data,root,8192,extra_glyphs=range(0xb0,0xc0))
   if q['error'] or not q['terminal']:errors.append({'item':item['id'],'root':f'{root:06X}','error':q['error'] or 'not terminal'});continue
   for lo,hi in b.spans_fr(data[root:q['end']]):
    a,z=root+lo,root+hi;text=b.decode(data[a:z],dic)
    if data[a:z]==source[a:z] and len(text)>9 and any(c.isalpha() for c in text):
     entry=found.setdefault((a,z),{'context':f'{root:06X}','offset':f'{a:06X}','end':f'{z:06X}','text':text,'item_ids':[]})
     if item['id'] not in entry['item_ids']:entry['item_ids'].append(item['id'])
   todo.extend(t for _,t in q['refs'] if 0<t<len(data))
 return {'scope':'help closure of 82 custom-shop item IDs; original literal spans longer than nine decoded characters only','natural_access_verified':False,'global_language_completion_verified':False,'item_count':len(items),'visited_roots':len(nodes),'candidates':[found[k] for k in sorted(found)],'unparsed':errors}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);a=ap.parse_args();source=a.rom.read_bytes();assert b.sha(source)==b.ROM_SHA;data=b.apply(source,b.records((ROOT/'patches/EarthBound_Beginnings_FR_v78_accents.ips').read_bytes()));items=json.loads((ROOT/'tools/v78/v78_fixtures.json').read_text())['item_help']['qualification']['items'];r=audit(source,data,items);(ROOT/'tools/v78/qualified_help_remaining.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False))
