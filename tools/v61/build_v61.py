"""Translate short confirmation/recipient fragments and three timed boos in place.
Every edit has identical byte length in both profiles. No pointer is rewritten.
"""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v60'))
from build_v60 import ROM_SHA,SIZE,sha,records,apply,append,sprite_digest
from build_v59 import encode,parse,spans_fr,decode,dictionary_from_rom,commands,pointer,pointer_index
CONFIG=[{'context':'34FADF','offset':'34FADF','end':'34FAE2','en':'@A ','fr':'@  ','kind':'confirmation_article'},
 {'context':'37BE28','offset':'37BE28','end':'37BE2C','en':' to ','fr':' à  ','kind':'recipient_preposition'}]
BOOS=[('35041F',0x350423),('3504A9',0x3504AD),('35055D',0x3505D8)]

def config():
 edits=[dict(e) for e in CONFIG]
 for root,start in BOOS:
  # The initial @B and two literal o glyphs are already suitable; preserve them.
  for offset,en,fr in zip([start,*[start+4+3*i for i in range(8)]],['@B',*['o']*7,'o!'],['@B','o','u','h','o','u','u','u','u!']):
   if en!=fr:edits.append({'context':root,'offset':f'{offset:06X}','end':f'{offset+len(en):06X}','en':en,'fr':fr,'kind':'timed_boo_glyph'})
 return edits

def fixtures(source,bases):
 if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
 dic=dictionary_from_rom(source);contexts={};edits=[]
 for c in config():
  a,z=int(c['offset'],16),int(c['end'],16);r=int(c['context'],16);e=dict(c);e['profiles']={};context={}
  for p,data in bases.items():
   parsed=parse(data,r,8192,extra_glyphs=range(0xB0,0xC0))
   if parsed['error'] or not parsed['terminal']:raise ValueError('Contexte non fermé')
   if (a-r,z-r) not in spans_fr(data[r:parsed['end']]):raise ValueError('Frontière textuelle invalide')
   raw=data[a:z]
   if decode(raw,dic)!=c['en']:raise ValueError('Texte source divergent')
   if len(encode(c['fr'],p))!=len(raw):raise ValueError('Taille du fragment modifiée')
   e['profiles'][p]={'baseline_hex':raw.hex()};context[p]={'end':f"{parsed['end']:06X}",'baseline_hex':data[r:parsed['end']].hex()}
  contexts[c['context']]=context;edits.append(e)
 return {'version':'v61','base':'v60','edits':edits,'contexts':contexts,'new_allocations':0,'pointer_operands_rewritten':0}

def additions(f,p):
 if [{k:e[k] for k in ('context','offset','end','en','fr','kind')} for e in f['edits']]!=config():raise ValueError('Inventaire divergent')
 result=[]
 for e in f['edits']:
  a,z=int(e['offset'],16),int(e['end'],16);raw=encode(e['fr'],p)
  if len(raw)!=z-a or len(bytes.fromhex(e['profiles'][p]['baseline_hex']))!=z-a:raise ValueError('Taille du fragment modifiée')
  result.append((a,raw))
 ranges=sorted((a,a+len(v)) for a,v in result)
 if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Chevauchement')
 return result

def build(rom,out):
 source=Path(rom).read_bytes();old=json.loads((ROOT/'tools/v60/validation_v60.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v60_{p}.ips').read_bytes() for p in ('accents','ascii')}
 if any(sha(v)!=old['profiles'][p]['sha256'] for p,v in priors.items()):raise ValueError('IPS V60 divergent')
 bases={p:apply(source,records(v)) for p,v in priors.items()};f=fixtures(source,bases);profiles={};out=Path(out);out.mkdir(exist_ok=True,parents=True)
 for p,base in bases.items():
  changes=additions(f,p);ips=append(priors[p],changes);target=apply(source,records(ips))
  if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
  if sprite_digest(target)!=sprite_digest(base):raise ValueError('Sprites modifiés')
  for root,c in f['contexts'].items():
   a,z=int(root,16),int(c[p]['end'],16)
   if commands(target[a:z])!=commands(bytes.fromhex(c[p]['baseline_hex'])):raise ValueError('Commandes modifiées')
  (out/f'EarthBound_Beginnings_FR_v61_{p}.ips').write_bytes(ips);profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p]))}
 plan={'version':'v61','source_sha256':sha(source),'short_lexical_fragments':2,'timed_boo_scenes':3,'modified_glyph_fragments':len(f['edits']),'contexts_revised':len(f['contexts']),'new_allocations':0,'pointer_operands_rewritten':0,'commands_preserved':True,'natural_branch_access_verified':False,'profiles':profiles}
 for name,value in (('v61_fixtures',f),('validation_v61',plan)):(ROOT/f'tools/v61/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
