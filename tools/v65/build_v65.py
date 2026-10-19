"""Scope a neutral article helper to storage, retaining its classifier/dispatch."""
import argparse,collections,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
from safe_storage import safe_reserves
CALL,HELPER,EMPTY=0x34B577,0x38B587,0x38B550
RETURN_CALL=0x259B27
CALLS=(CALL,RETURN_CALL)
TEXT,END=0x34B580,0x34B5A1
FRENCH='  Cet objet sera bien au chaud. '

def graph(data):
 queue=collections.deque([0x34B490]);nodes={}
 while queue:
  a=queue.popleft()
  if a in nodes:continue
  p=b.parse(data,a,8192,extra_glyphs=range(0xB0,0xC0));assert not p['error'] and p['terminal'];nodes[a]=p;queue.extend(t for _,t in p['refs'])
 return nodes

def token_ends(raw):
 pos=0;ends=[]
 while pos<len(raw):
  c=raw[pos];n=1 if c>=0x20 else 2 if c in (0x15,0x16,0x17) else b.length(raw,pos)
  assert n>0 and pos+n<=len(raw);pos+=n
  # Do not insert a jump inside a word: the engine's look-ahead must see it
  # intact. A complete command, space, or transition into a command is safe.
  if pos==len(raw) or c==0x50 or c<0x20 and c not in (0x15,0x16,0x17) or raw[pos]<0x20 and raw[pos] not in (0x15,0x16,0x17):ends.append(pos)
 return ends

def location(fixtures,address):
 for node in fixtures['moved_scripts']:
  for c in node['chunks']:
   a,z=int(c['source_start'],16),int(c['source_end'],16)
   if a<=address<z:return int(c['destination'],16)+address-a
 return address

def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA
 prior_plan=json.loads((ROOT/'tools/v64/validation_v64.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v64_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(ips)) for p,ips in priors.items()}
 for p in bases:assert b.sha(priors[p])==prior_plan['profiles'][p]['sha256'] and b.sha(bases[p])==prior_plan['profiles'][p]['target_rom_sha256']
 targets=set(b.pointer_index(source))
 for data in bases.values():targets.update(b.pointer_index(data))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);free=[r[:] for r in reserves]
 def allocate(size):
  free.sort(key=lambda r:(-(r[1]-r[0]),r[0]))
  for region in free:
   if region[1]-region[0]>=size:
    dest=region[0];region[0]=(dest+size+3)&~3;return dest
  raise ValueError('Safe storage exhausted')
 destination=allocate(27);graphs={p:graph(data) for p,data in bases.items()};nodes=graphs['accents'];moved=[]
 # Legacy translated copies overlap sprite footprints. Keep bank 25 intact;
 # move the whole bank-25 closure of this service, splitting only at tokens.
 for a,p in sorted(nodes.items()):
  if not 0x250000<=a<0x260000:continue
  raw=bases['accents'][a:p['end']];bounds=token_ends(raw);pos=0;chunks=[]
  while pos<len(raw):
   free.sort(key=lambda r:(-(r[1]-r[0]),r[0]));capacity=free[0][1]-free[0][0]
   limit=capacity if len(raw)-pos<=capacity else capacity-5
   stop=max((q for q in bounds if pos<q<=pos+limit),default=None)
   if stop is None:raise ValueError('No room for complete command')
   size=stop-pos+(5 if stop<len(raw) else 0);dest=allocate(size);chunks.append({'source_start':f'{a+pos:06X}','source_end':f'{a+stop:06X}','destination':f'{dest:06X}','continuation':None});pos=stop
  for c,nxt in zip(chunks,chunks[1:]):c['continuation']=nxt['destination']
  moved.append({'root':f'{a:06X}','end':f'{p["end"]:06X}','chunks':chunks})
 mapping={int(n['root'],16):int(n['chunks'][0]['destination'],16) for n in moved}
 fixtures={'version':'v65','base':'v64','copy_offset':f'{destination:06X}','copy_size':27,'source_helper':f'{HELPER:06X}','call_operands':[f'{a:06X}' for a in CALLS],'text_offset':f'{TEXT:06X}','text_end':f'{END:06X}','french':FRENCH,'storage':storage,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'moved_scripts':moved,'profiles':{}};profiles={}
 for profile,base in bases.items():
  for call in CALLS:assert base[call-1:call+4]==b'\x08'+b.pointer(HELPER)
  assert base[EMPTY:EMPTY+1]==b'\x02';p=b.parse(base,HELPER,8192,extra_glyphs=range(0xB0,0xC0));assert p['end']==HELPER+27 and p['refs']==[(HELPER+q,0x38B54B) for q in (6,10,14,18)]+[(HELPER+22,EMPTY)]
  helper=bytearray(base[HELPER:HELPER+27])
  for q in (6,10,14,18):helper[q:q+4]=b.pointer(EMPTY)
  edits={};modified_bodies={};relocated=[]
  for a,p in graphs[profile].items():
   raw=bytearray(base[a:p['end']])
   for q,t in p['refs']:
    new=destination if q in CALLS else mapping.get(t,t)
    if new==t:continue
    raw[q-a:q-a+4]=b.pointer(new)
    if a not in mapping:
     assert not 0x250000<=q<0x260000
     if q in edits:assert edits[q]==b.pointer(new)
     edits[q]=b.pointer(new)
   modified_bodies[a]=bytes(raw)
  for node in moved:
   a=int(node['root'],16);body=modified_bodies[a]
   for c in node['chunks']:
    lo,hi=int(c['source_start'],16)-a,int(c['source_end'],16)-a;raw=body[lo:hi]
    if c['continuation']:raw+=b'\x0a'+b.pointer(int(c['continuation'],16))
    relocated.append((int(c['destination'],16),raw))
  root=0x34B517;context=graphs[profile][root];assert (TEXT-root,END-root) in b.spans_fr(base[root:context['end']]);assert b.decode(base[TEXT:END],b.dictionary_from_rom(source))=='  Je le garderai bien au chaud.  '
  text=b.encode(FRENCH,profile);assert len(text)<=END-TEXT;text+=b.encode(' ',profile)*(END-TEXT-len(text))
  changes=[*sorted(edits.items()),(destination,bytes(helper)),*relocated,(TEXT,text)];ips=b.append(priors[profile],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  assert target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x38B54B:0x38B5A2]==base[0x38B54B:0x38B5A2];assert b.sprite_digest(target)==b.sprite_digest(base)
  for a,p in graphs[profile].items():
   if a in mapping:
    node=next(n for n in moved if int(n['root'],16)==a);raw=b''.join(target[int(c['destination'],16):int(c['destination'],16)+int(c['source_end'],16)-int(c['source_start'],16)] for c in node['chunks'])
   else:raw=target[a:p['end']]
   normalized=bytearray(raw)
   for q,t in p['refs']:normalized[q-a:q-a+4]=b.pointer(t)
   assert b.commands(bytes(normalized))==b.commands(base[a:p['end']])
  out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/f'EarthBound_Beginnings_FR_v65_{profile}.ips').write_bytes(ips)
  profiles[profile]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes),'prior_records_preserved':len(b.records(priors[profile]))}
  fixtures['profiles'][profile]={'original_helper_hex':base[HELPER:HELPER+27].hex(),'scoped_helper_hex':bytes(helper).hex(),'original_text_hex':base[TEXT:END].hex(),'replacement_text_hex':text.hex(),'safe_pointer_edits':[{'offset':f'{q:06X}','target':f'{int.from_bytes(v,"little")-0xC00000:06X}'} for q,v in sorted(edits.items())]}
 plan={'version':'v65','base':'v64','source_sha256':b.sha(source),'english_confirmation_contexts_corrected':2,'gender_neutral_confirmation':True,'shared_helper_modified':False,'scoped_dispatch_targets_changed':4,'legacy_service_scripts_relocated':len(moved),'bank25_unchanged':True,'classifier_and_dispatch_opcodes_preserved':True,'sprites_preserved_against':'v64','natural_scene_access_verified':False,'profiles':profiles}
 for name,value in [('v65_fixtures',fixtures),('validation_v65',plan)]:(ROOT/f'tools/v65/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');args=ap.parse_args();print(json.dumps(build(args.rom,args.out),indent=2))
