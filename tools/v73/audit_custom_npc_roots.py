"""Direct custom NPC roots omitted by the old interval filter; not a coverage proof."""
import argparse,json,re
from pathlib import Path
from build_v73 import ROOT,b
PATTERN=r"\b(you|your|what|please|i'm|don't|we|would|can|yes|no|isn't)\b"
def audit(source,data):
 dic=b.dictionary_from_rom(source);roots={};failed=[];candidates=[]
 for npc in range(1584):
  for field in (9,13):
   q=0x2021A8+17*npc+field;t=int.from_bytes(data[q:q+4],'little')-0xC00000
   if 0x36BB00<=t<0x3F0000:roots.setdefault(t,[]).append({'npc':npc,'field':field,'operand':f'{q:06X}'})
 for root,labels in sorted(roots.items()):
  p=b.parse(data,root,8192,extra_glyphs=range(0xB0,0xC0))
  if p['error'] or not p['terminal']:failed.append({'root':f'{root:06X}','error':p['error'] or 'no terminal'});continue
  text=' | '.join(b.decode(data[root+a:root+z],dic) for a,z in b.spans_fr(data[root:p['end']]))
  if re.search(PATTERN,text,re.I):candidates.append({'root':f'{root:06X}','npc_references':labels,'text':text})
 return {'version':'v73','scope':'direct NPC roots in [36BB00,3F0000), no recursive closure','profile':'accents','custom_roots_examined':len(roots),'natural_access_verified':False,'language_classification_verified':False,'pattern':PATTERN,'candidates':candidates,'unparsed_roots':failed}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'tools/v73/custom_npc_roots_v73.json');a=ap.parse_args();source=a.rom.read_bytes();assert b.sha(source)==b.ROM_SHA;plan=json.loads((ROOT/'tools/v73/validation_v73.json').read_text());ips=(ROOT/'patches/EarthBound_Beginnings_FR_v73_accents.ips').read_bytes();assert b.sha(ips)==plan['profiles']['accents']['sha256'];data=b.apply(source,b.records(ips));assert b.sha(data)==plan['profiles']['accents']['target_rom_sha256'];result=audit(source,data);a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print({'roots':result['custom_roots_examined'],'candidates':len(result['candidates']),'unparsed':len(result['unparsed_roots'])})
