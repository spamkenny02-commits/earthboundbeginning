"""Remaining custom dialogue and sprite-backed train/name selectors.

The five bank-25 scripts overlap sprite pixels. Copy only their executable
contexts to protected padding, then redirect their sole explicit callers.
Neither their original bytes nor the NPC table are changed.
"""
import json
from pathlib import Path
from build_v78 import ROOT,b,safe_reserves
from parser_v62 import length
CONFIG=[
 ('36DCD5','36DD0A','36DD2A',' but, you need a ticket to ride.',' mais il te faut un billet.'),
 ('36DCD5','36DD2C','36DD3D','@Care to buy one?','@Tu en veux un ?'),
 ('36E573','36E5EB','36E61D',"@First let's go see what's happening in Youngtown.","@Voyons d'abord ce qui se passe à Youngtown."),
 ('36E573','36E628','36E631','@Daddy...','@Papa...'),
 ('36E573','36E66C','36E67B','@Believe in us!','@Crois en nous!'),
 ('36E81C','36E832','36E84B',"@I'm concerned about you,","@Je m'inquiète pour toi,"),
 ('377419','377426','377435','@(Hubba hubba.)','@(Quel charme.)'),
 ('380B42','380B42','380B58','@Have you ever tasted ','@Tu as déjà goûté : '),
 ('384C00','384C44','384C56','@Your balance is $','@Ton solde est : $'),
 ('384C00','384CA6','384CC1','@Here...  Take it with you.',"@Tiens... Prends l'argent."),
 ('384D6E','384D94','384DB0','@Go think things over again.','@Va donc y réfléchir encore.'),
 ('386D23','386D46','386D66','@Please make sure it is correct.',"@Vérifie bien que c'est correct."),
 ('38BA92','38BADB','38BAF1','@The monkey stole the ','@Le singe a volé : '),
 ('054789','054792','0547AE','@This is the best thing to take when you get poisoned.','@Idéal contre le poison.'),
 ('378989','378992','378997',' and ',' et '),
 ('384DB6','384DB7','384DBC','@Bye!','@Ciao'),
 *[(r,a,z,'@Welcome!','@Bonjour!') for r,a,z in [
 ('37959C','3795A3','3795AC'),('3796CB','3796D2','3796DB'),
 ('37984E','379855','37985E'),('3799D1','3799D8','3799E1'),
 ('379B54','379B5B','379B64'),('379CD7','379CDE','379CE7'),
 ('379E55','379E5C','379E65')]],
]
LABELS=[('37B994','37B99E','37B9A1','Buy','Acheter'),('37B994','37B9A4','37B9A8','Sell','Vendre')]
# root, Yes literal, No definition, continuation; all direct callers are guarded.
MOVED=[(0x251A50,0x251ABF,0x251AC3,0x251AC8,0x386C8F),
 (0x25B08C,0x25B0B7,0x25B0BB,0x25B0C0,0x36DD97),
 (0x25B0D4,0x25B0FF,0x25B103,0x25B108,0x36DD9B),
 (0x25B11C,0x25B147,0x25B14B,0x25B150,0x36DD9F),
 (0x25B164,0x25B18F,0x25B193,0x25B198,0x36DDA3)]
MENUS=[(0x32E120,0x32E139,0x32E13D,0x32E142),
 (0x380B42,0x380B5F,0x380B63,0x380B68),
 (0x384B8B,0x384BA8,0x384BAC,0x384BB1),
 (0x384BC5,0x384BE3,0x384BE7,0x384BEC)]
def atoms(raw):
 """Indivisible commands/menu definitions, and words including their spaces."""
 result=[];p=0
 while p<len(raw):
  if raw[p:p+2]==b'\x19\x02':
   end=raw.index(2,p+2)+1;result.append(raw[p:end]);p=end
  elif 0x50<=raw[p]<0xC0 or raw[p] in (0xC8,0xC9,0xCA,0xCB,0x15,0x16,0x17):
   start=p
   while p<len(raw) and (0x50<=raw[p]<0xC0 or raw[p] in (0xC8,0xC9,0xCA,0xCB,0x15,0x16,0x17)):
    c=raw[p];p+=2 if c in (0x15,0x16,0x17) else 1
    if c==0x50:break
   result.append(raw[start:p])
  else:n=length(raw,p);result.append(raw[p:p+n]);p+=n
 return result
def extend(source,out,plan,fixtures):
 out=Path(out);priors={p:(out/f'EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()};targets=set(b.pointer_index(source))
 for data in bases.values():targets.update(b.pointer_index(data))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);free=[r[:] for r in reserves]
 def take(size):
  free.sort(key=lambda r:((r[1]-r[0]),r[0]));r=next((r for r in free if r[1]-r[0]>=size),None)
  if r is None:raise ValueError(f'Protected reserve exhausted: {size}')
  a=r[0];r[0]=(a+size+3)&~3;return a
 # One common definition can be called from each external selector, but each
 # continuation differs; keep separate return helpers and deduplicate counting.
 moved=[];prepared=[]
 labels=[(*e,take(len(b.encode(e[4],'accents'))+8)) for e in LABELS]
 for root,yes,no,ret,caller in MOVED:
  base=bases['accents'];q=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error'];assert b.pointer_index(base)[root]==[caller]
  assert base[caller:caller+4]==b.pointer(root);assert base[yes:yes+3]==b.encode('Yes','accents');assert base[no:ret]==b'\x19\x02'+b.encode('No','accents')+b'\x02'
  body=base[root:yes]+b.encode('Oui','accents')+base[yes+3:no]+b'\x19\x02'+b.encode('Non','accents')+b'\x02'+base[ret:q['end']]
  prepared.append((root,yes,no,ret,caller,q,atoms(body)))
 # Reserve the scarce 13..16-byte blocks for indivisible long words and
 # branch commands before short pieces consume them.
 reserved={}
 large=sorted(((len(raw),i,j) for i,row in enumerate(prepared) for j,raw in enumerate(row[-1]) if len(raw)>7),reverse=True)
 for size,i,j in large:reserved[i,j]=take(size+5)
 menus=[(*e,take(11)) for e in MENUS]
 for i,(root,yes,no,ret,caller,q,original_pieces) in enumerate(prepared):
  pieces=list(enumerate(original_pieces));chunks=[]
  while pieces:
   j,raw=pieces[0]
   if (i,j) in reserved:dest=reserved[i,j];payload=raw;pieces.pop(0)
   else:
    free.sort(key=lambda r:(-(r[1]-r[0]),r[0]));limit=free[0][1]-free[0][0]-5;payload=bytearray()
    while pieces and (i,pieces[0][0]) not in reserved and len(payload)+len(pieces[0][1])<=limit:payload.extend(pieces.pop(0)[1])
    if not payload:raise ValueError(f'No complete command/word fits padding: root {root:06X}, limit {limit}')
    dest=take(len(payload)+5)
   chunks.append({'destination':f'{dest:06X}','payload_size':len(payload),'payload_accents_hex':payload.hex()})
  moved.append({'root':f'{root:06X}','end':f'{q["end"]:06X}','yes':f'{yes:06X}','no_definition':f'{no:06X}','continuation':f'{ret:06X}','caller':f'{caller:06X}','chunks':chunks})
 f={'entries':[dict(zip(('context','offset','end','en','fr'),e)) for e in CONFIG], 'menus':[{'context':f'{r:06X}','yes':f'{y:06X}','no_definition':f'{n:06X}','continuation':f'{z:06X}','destination':f'{d:06X}'} for r,y,n,z,d in menus],'moved_scripts':moved,'storage':storage,'safe_reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'profiles':{}}
 f['labels']=[{**dict(zip(('context','offset','end','en','fr'),e[:5])),'destination':f'{e[5]:06X}'} for e in labels]
 profiles={};dic=b.dictionary_from_rom(source)
 for p,base in bases.items():
  changes=[]
  for e in f['entries']:
   root,a,z=(int(e[k],16) for k in ('context','offset','end'));q=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error'];assert (a-root,z-root) in b.spans_fr(base[root:q['end']]);assert b.decode(base[a:z],dic)==e['en'];raw=b.encode(e['fr'],p);assert len(raw)<=z-a,(e['offset'],len(raw),z-a);changes.append((a,raw+b.encode(' ',p)*(z-a-len(raw))))
  for root,a,z,en,fr,dest in labels:
   a,z=int(a,16),int(z,16);assert base[a-2:z+1]==b'\x19\x02'+b.encode(en,p)+b'\x02';assert not any(a-2<t<a+3 for t in targets)
   changes.extend([(a-2,b'\x0a'+b.pointer(dest)),(dest,b'\x19\x02'+b.encode(fr,p)+b'\x02\x0a'+b.pointer(z+1))])
  for root,yes,no,ret,dest in menus:
   assert base[yes:yes+3]==b.encode('Yes',p) and base[no:ret]==b'\x19\x02'+b.encode('No',p)+b'\x02';assert not any(no<t<no+5 for t in targets)
   changes.extend([(yes,b.encode('Oui',p)),(no,b'\x0a'+b.pointer(dest)),(dest,b'\x19\x02'+b.encode('Non',p)+b'\x02\x0a'+b.pointer(ret))])
  for node in moved:
   # The two profiles have the same command layout and glyph count. Rebuild
   # each copied payload from its accents glyphs without touching commands.
   chunks=node['chunks'];root=int(node['root'],16);end=int(node['end'],16);yes=int(node['yes'],16);no=int(node['no_definition'],16);ret=int(node['continuation'],16)
   body=base[root:yes]+b.encode('Oui',p)+base[yes+3:no]+b'\x19\x02'+b.encode('Non',p)+b'\x02'+base[ret:end];pos=0
   for i,c in enumerate(chunks):
    size=c['payload_size'];d=int(c['destination'],16);payload=body[pos:pos+size];pos+=size
    # Final continuation is already the original native terminator. The
    # extra zero bytes are padding, not an executed synthetic return.
    raw=payload+(b'\x0a'+b.pointer(int(chunks[i+1]['destination'],16)) if i+1<len(chunks) else bytes(5));changes.append((d,raw))
   assert pos==len(body);assert b.commands(body)==b.commands(base[root:end]);changes.append((int(node['caller'],16),b.pointer(int(chunks[0]['destination'],16))))
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  assert target[0x250000:0x260000]==base[0x250000:0x260000];assert b.sprite_digest(target)==b.sprite_digest(base);assert target[0x2021A8:0x2021A8+1584*17]==base[0x2021A8:0x2021A8+1584*17];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000]
  allocations={d for *_,d in menus}|{d for *_,d in labels}|{int(c['destination'],16) for n in moved for c in n['chunks']}
  for d,raw in changes:
   if d in allocations:assert base[d:d+len(raw)]==bytes(len(raw))
  (out/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':plan['profiles'][p]['records_added']+len(changes)};f['profiles'][p]={'input_patch_sha256':b.sha(priors[p]),'input_rom_sha256':b.sha(base),'records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes]}
 existing={e['english'] for e in fixtures['profiles']['accents']['edits']}|{'No'}|{e['en'] for e in fixtures['medical']['entries']}
 new_count=len({e[3] for e in CONFIG+LABELS}-existing);fixtures['remaining']=f;plan.update(profiles=profiles,changed_text_spans=plan['changed_text_spans']+len(CONFIG)+len(LABELS)+2*(len(MENUS)+len(MOVED)),distinct_new_translations=plan['distinct_new_translations']+new_count,remaining_new_distinct=new_count,sprite_backed_scripts_copied=len(MOVED),remaining_allocated_bytes=44+sum(len(b.encode(e[4],'accents'))+8 for e in LABELS)+sum(c['payload_size']+5 for n in moved for c in n['chunks']))
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
