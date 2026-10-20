"""Clone two qualified text paths while preserving unqualified interior aliases.

Only the water item record and the already proved medical bridge return are
redirected. Original scripts and every raw interior occurrence stay untouched.
Copies use protected padding and whole command/word atoms, including spaces.
"""
import json
from pathlib import Path
from build_v78 import ROOT,b,safe_reserves
from remaining_stage import atoms
from item_help_stage import qualify,help_path

CONFIG=[
 dict(context='054733',offset='05473C',end='054758',
      en='@When you drink it, your PP slightly increases.',
      fr='@Bois pour gagner un peu de PP.',caller='1560E5',kind='item_help',
      aliases=['054743']),
 dict(context='0911EB',offset='0911ED',end='091212',
      en="@the best thing to do is to call home and hear your mom's voice.",
      fr='@Passe un coup de fil à maman : sa voix te fera du bien.',
      caller='329025',kind='medical_continuation',aliases=['0911F0']),
]

def extend(source,out,plan,fixtures):
 out=Path(out);priors={p:(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()}
 targets=set(b.pointer_index(source))
 for base in bases.values():targets.update(b.pointer_index(base))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);free=[r[:] for r in reserves]
 def take(size):
  free.sort(key=lambda r:(r[1]-r[0],r[0]));r=next((r for r in free if r[1]-r[0]>=size),None)
  if r is None:raise ValueError(f'No protected reserve for {size} bytes')
  a=r[0];r[0]=(a+size+3)&~3;return a
 entries=[];prepared=[];dic=b.dictionary_from_rom(source)
 for cfg in CONFIG:
  e=dict(cfg);root,a,z,caller=(int(e[k],16) for k in ('context','offset','end','caller'));base=bases['accents'];q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));assert q['terminal'] and not q['error'];assert b.decode(base[a:z],dic)==e['en'];assert (a-root,z-root) in b.spans_fr(base[root:q['end']]);assert base[caller:caller+4]==b.pointer(root)
  if e['kind']=='item_help':
   item=next(i for i in qualify(base,source)['items'] if i['id']=='6E');assert int(item['help_root'],16)==root;assert caller==0x155000+39*0x6E+35;e['qualified_path']=help_path(base,root,root)
  else:
   previous=next(v for v in fixtures['medical']['profiles']['accents']['edits'] if v['offset']=='0911E2');last=previous['blocks'][-1];assert int(last['offset'],16)+last['payload_size']+1==caller;assert int(previous['bridge_end'],16)==root;assert base[caller-1]==0x0a;e['qualified_path']=['0911E2',last['offset'],e['context']]
  rawrefs=b.pointer_index(base);e['preserved_interior_occurrences']={t:[f'{v:06X}' for v in rawrefs[int(t,16)]] for t in e['aliases']}
  body=base[root:a]+b.encode(e['fr'],'accents')+base[z:q['end']];prepared.append(atoms(body))
  e.update(context_end=f'{q["end"]:06X}');entries.append(e)
 # Reserve the scarce larger blocks before small commands consume them.
 allocated={}
 for size,i,j in sorted(((len(raw),i,j) for i,pieces in enumerate(prepared) for j,raw in enumerate(pieces)),reverse=True):allocated[i,j]=take(size+5)
 for i,e in enumerate(entries):e['chunks']=[{'destination':f'{allocated[i,j]:06X}','payload_size':len(raw)} for j,raw in enumerate(prepared[i])]
 f={'entries':entries,'storage':storage,'safe_reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'profiles':{}};profiles={}
 for p,base in bases.items():
  changes=[]
  for e in entries:
   root,a,z,end,caller=(int(e[k],16) for k in ('context','offset','end','context_end','caller'));body=base[root:a]+b.encode(e['fr'],p)+base[z:end];assert b.commands(body)==b.commands(base[root:end]);pos=0
   for i,c in enumerate(e['chunks']):
    d=int(c['destination'],16);size=c['payload_size'];tail=b'\x0a'+b.pointer(int(e['chunks'][i+1]['destination'],16)) if i+1<len(e['chunks']) else bytes(5);raw=body[pos:pos+size]+tail;pos+=size;assert base[d:d+len(raw)]==bytes(len(raw));changes.append((d,raw))
   assert pos==len(body);changes.append((caller,b.pointer(int(e['chunks'][0]['destination'],16))))
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for e in entries:
   root,end=int(e['context'],16),int(e['context_end'],16);assert target[root:end]==base[root:end]
   for t,occurrences in e['preserved_interior_occurrences'].items():
    for v in occurrences:
     a=int(v,16);assert target[a:a+4]==base[a:a+4]==b.pointer(int(t,16))
  assert b.sprite_digest(target)==b.sprite_digest(base) and target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000];assert target[0x2021A8:0x2021A8+1584*17]==base[0x2021A8:0x2021A8+1584*17]
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)};f['profiles'][p]={'input_patch_sha256':b.sha(priors[p]),'input_rom_sha256':b.sha(base),'input_records_added':plan['profiles'][p]['records_added'],'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]}
 fixtures['scoped_help']=f;plan.update(profiles=profiles,distinct_new_translations=plan['distinct_new_translations']+2,changed_text_spans=plan['changed_text_spans']+2,scoped_help_allocated_bytes=sum(c['payload_size']+5 for e in entries for c in e['chunks']),scoped_help_original_aliases_preserved=True)
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
