"""Audit the ATM graph from both real NPC fields, including old engine entries."""
import argparse,collections,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'v62'))
import runtime as b
ROOT=b.ROOT

def audit(source,data,profile):
 roots=(0x0680A6,0x0680C2);bindings=[]
 for row in range(1584):
  q=0x2021A8+17*row
  values=[int.from_bytes(data[q+f:q+f+4],'little')-0xC00000 for f in (9,13)]
  if values[0]==roots[0]:
   assert values[1]==roots[1];bindings.append({'npc_row':row,'talk_operand':f'{q+9:06X}','check_operand':f'{q+13:06X}'})
 assert len(bindings)==17
 queue=collections.deque(roots);seen=set();nodes=[];edges=[];dic=b.dictionary_from_rom(source)
 prior=json.loads((ROOT/'tools/v62/alias_audit_v62.json').read_text())['paths']
 while queue:
  a=queue.popleft()
  if a in seen:continue
  seen.add(a);p=b.parse(data,a,8192,extra_glyphs=range(0xB0,0xC0));assert not p['error'] and p['terminal'],(hex(a),p['error'])
  raw=data[a:p['end']];spans=[{'offset':f'{a+lo:06X}','end':f'{a+hi:06X}','text':b.decode(raw[lo:hi],dic)} for lo,hi in b.spans_fr(raw)]
  nodes.append({'root':f'{a:06X}','end':f'{p["end"]:06X}','in_v62_graph':f'{a:06X}' in prior,'spans':spans})
  for q,t in p['refs']:
   assert 0<t<len(data);edges.append({'context':f'{a:06X}','operand':f'{q:06X}','target':f'{t:06X}'});queue.append(t)
 return {'version':'v64','profile':profile,'rom_sha256':b.sha(data),'npc_bindings':bindings,'roots':[f'{a:06X}' for a in roots],'nodes':nodes,'edges':edges,'unparsed_roots':[],'assembly_or_computed_callers_exhaustively_covered':False,'natural_access_verified':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA;data=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v64_{args.profile}.ips').read_bytes()))
 result=audit(source,data,args.profile);args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(args.profile,len(result['npc_bindings']),'NPC bindings',len(result['nodes']),'roots',len(result['edges']),'references')
