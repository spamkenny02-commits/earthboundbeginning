"""Extend the V78 checkpoint with medical text, using verified text-only bridges.

Dictionary-compressed English often leaves fewer bytes than natural French.
Each overflow keeps its original entry address and returns to the exact next
command; small protected zero-padding blocks are linked without CPU changes.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
from safe_storage import safe_reserves
NO_MENUS=[(0x09128D,0x091315,0x09131A),(0x091ABE,0x091B0E,0x091B13)]
def extend(source,out,plan,fixtures):
 cfg=json.loads((ROOT/'tools/v78/medical_translations.json').read_text());out=Path(out);dic=b.dictionary_from_rom(source);priors={p:(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()};targets=set(b.pointer_index(source))
 for base in bases.values():targets.update(b.pointer_index(base))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);free=[r[:] for r in reserves]
 def take(size):
  free.sort(key=lambda r:(-(r[1]-r[0]),r[0]));region=next((r for r in free if r[1]-r[0]>=size),None)
  if region is None:raise ValueError(f'Protected padding exhausted for {size} bytes')
  dest=region[0];region[0]=(dest+size+3)&~3;return dest
 menus=[(root,no,ret,take(11)) for root,no,ret in NO_MENUS];copies={};bridge_ranges={};blocked=[];eligible=[]
 def selector(e):
  a,z=int(e['offset'],16),int(e['end'],16);return bases['accents'][a-2:a]==b'\x19\x02' and bases['accents'][z]==2
 # A menu label must move with its 19 02 definition, never jump from inside
 # its literal glyphs. Reserve these indivisible definitions first.
 cfg=sorted(cfg,key=lambda e:(not selector(e),-max(map(len,e['fr'].split()),default=0)))
 for e in cfg:
  a,z=int(e['offset'],16),int(e['end'],16);raw=b.encode(e['fr'],'accents')
  assert len(raw)==len(b.encode(e['fr'],'ascii'))
  if len(raw)>z-a:
   # Only the first five bytes are overwritten. Later interior entries keep
   # their original bytes and behavior; they are not certified translated.
   lo,hi=(a-2,z+1) if selector(e) else (a,z);payload=b'\x19\x02'+raw+b'\x02' if selector(e) else raw
   conflicts=sorted(t for t in targets if lo<t<lo+5)
   if z-a<5 or conflicts:
    blocked.append({**e,'reason':'target enters overwritten prefix' if conflicts else 'text span shorter than jump','targets':[f'{t:06X}' for t in conflicts]});continue
   if selector(e):
    copies[a]=[(take(len(payload)+5),len(payload))];bridge_ranges[a]=(lo,hi,True);eligible.append(e);continue
   nodes=[];pos=0
   while pos<len(raw):
    free.sort(key=lambda r:(-(r[1]-r[0]),r[0]));capacity=min(len(raw)-pos,free[0][1]-free[0][0]-5)
    if capacity<1:raise ValueError('Protected padding exhausted for text chain')
    if pos+capacity<len(raw):
     # Jumps interrupt the engine's word look-ahead. End a block at a space,
     # otherwise the renderer can split a word even when it fits on a line.
     cut=raw.rfind(b.encode(' ','accents'),pos,pos+capacity)
     if cut<pos:raise ValueError(f'Padding cannot hold a whole word: {e["offset"]}')
     capacity=cut+1-pos
    dest=take(capacity+5);nodes.append((dest,capacity));pos+=capacity
   copies[a]=nodes;bridge_ranges[a]=(lo,hi,False)
  eligible.append(e)
 cfg=eligible
 profiles={};medical={'entries':cfg,'blocked_entries':blocked,'menus':[{'context':f'{r:06X}','offset':f'{a:06X}','end':f'{z:06X}','destination':f'{d:06X}','size':11} for r,a,z,d in menus],'safe_reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'storage':storage,'profiles':{}}
 for p,base in bases.items():
  changes=[];expansions=[];proof=[];contexts={}
  for e in cfg:
   root,a,z=(int(e[k],16) for k in ('context','offset','end'));q=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error'];contexts[root]=q['end'];assert (a-root,z-root) in b.spans_fr(base[root:q['end']]);assert b.decode(base[a:z],dic)==e['en'];raw=b.encode(e['fr'],p);entry={**e,'baseline_hex':base[a:z].hex()}
   if a not in copies:
    padded=raw+b.encode(' ',p)*(z-a-len(raw));changes.append((a,padded));entry.update(mode='fixed',replacement_hex=padded.hex())
   else:
    nodes=copies[a];lo,hi,is_menu=bridge_ranges[a];payload=b'\x19\x02'+raw+b'\x02' if is_menu else raw;changes.append((lo,b'\x0a'+b.pointer(nodes[0][0])));pos=0;blocks=[]
    for i,(dest,size) in enumerate(nodes):
     ret=nodes[i+1][0] if i+1<len(nodes) else hi;block=payload[pos:pos+size]+b'\x0a'+b.pointer(ret);assert base[dest:dest+len(block)]==bytes(len(block));changes.append((dest,block));blocks.append({'offset':f'{dest:06X}','payload_size':size,'hex':block.hex()});pos+=size
    assert pos==len(payload);expansions.append((lo,hi,payload));entry.update(mode='menu_bridge' if is_menu else 'text_bridge',bridge_start=f'{lo:06X}',bridge_end=f'{hi:06X}',jump_hex=(b'\x0a'+b.pointer(nodes[0][0])).hex(),blocks=blocks)
   proof.append(entry)
  for root,a,z,dest in menus:
   q=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));contexts[root]=q['end'];assert base[a:z]==b'\x19\x02'+b.encode('No',p)+b'\x02';raw=b'\x19\x02'+b.encode('Non',p)+b'\x02';helper=raw+b'\x0a'+b.pointer(z);assert base[dest:dest+11]==bytes(11);changes.extend([(a,b'\x0a'+b.pointer(dest)),(dest,helper)]);expansions.append((a,z,raw))
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for root,end in contexts.items():
   cursor=root;flat=bytearray()
   for a,z,raw in sorted(expansions):
    if root<=a and z<=end:flat.extend(target[cursor:a]);flat.extend(raw);cursor=z
    elif a<root<z or a<end<z:raise ValueError('Context enters replaced text interior')
   flat.extend(target[cursor:end]);assert b.commands(bytes(flat))==b.commands(base[root:end]),hex(root)
  for _,raw in changes:
   assert raw
  for a,_ in changes:
   if 0x328A70<=a<0x331000:
    q=b.parse(target,a,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error'],hex(a)
  assert target[0x2021A8:0x2021A8+1584*17]==base[0x2021A8:0x2021A8+1584*17];assert b.sprite_digest(target)==b.sprite_digest(base);assert target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)};medical['profiles'][p]={'input_stage_patch_sha256':b.sha(priors[p]),'edits':proof,'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]}
 fixtures['medical']=medical;plan.update(profiles=profiles,changed_text_spans=plan['changed_text_spans']+len(cfg)+len(menus),distinct_new_translations=len(set([e['english'] for e in fixtures['profiles']['accents']['edits']]+['No']+[e['en'] for e in cfg])),medical_entries=len(cfg),medical_no_menus=len(menus),medical_text_bridges=len(copies),medical_allocated_bytes=22+sum(size+5 for nodes in copies.values() for _,size in nodes),medical_commands_preserved_after_expansion=True)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
