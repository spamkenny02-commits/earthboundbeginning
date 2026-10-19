"""Scope a neutral article helper to storage, retaining its classifier/dispatch."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
from safe_storage import safe_reserves
CALL,HELPER,EMPTY=0x34B577,0x38B587,0x38B550
TEXT,END=0x34B580,0x34B5A1
FRENCH='  Cet objet sera bien au chaud. '

def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA
 prior_plan=json.loads((ROOT/'tools/v64/validation_v64.json').read_text())
 priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v64_{p}.ips').read_bytes() for p in ('accents','ascii')}
 bases={p:b.apply(source,b.records(ips)) for p,ips in priors.items()}
 for p in bases:assert b.sha(priors[p])==prior_plan['profiles'][p]['sha256'] and b.sha(bases[p])==prior_plan['profiles'][p]['target_rom_sha256']
 targets=set(b.pointer_index(source))
 for data in bases.values():targets.update(b.pointer_index(data))
 # Leave the final 64 bytes available for documented private display probes.
 targets.update(range(0x330FC0,0x331000))
 reserves,storage=safe_reserves(source,bases,priors,targets,b.records)
 size=0x38B5A2-HELPER;destination=next((a for a,z in reserves if z-a>=size),None)
 if destination is None:raise ValueError('No safe storage for scoped helper')
 profiles={};fixtures={'version':'v65','base':'v64','copy_offset':f'{destination:06X}','copy_size':size,'source_helper':f'{HELPER:06X}','call_operand':f'{CALL:06X}','text_offset':f'{TEXT:06X}','text_end':f'{END:06X}','french':FRENCH,'storage':storage,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'profiles':{}}
 for p,base in bases.items():
  assert base[CALL-1:CALL+4]==b'\x08'+b.pointer(HELPER)
  assert base[EMPTY:EMPTY+1]==b'\x02'
  parsed=b.parse(base,HELPER,8192,extra_glyphs=range(0xB0,0xC0));assert parsed['end']==0x38B5A2 and not parsed['error']
  assert parsed['refs']==[(HELPER+q,0x38B54B) for q in (6,10,14,18)]+[(HELPER+22,EMPTY)]
  payload=bytearray(base[HELPER:parsed['end']])
  for q in (6,10,14,18):payload[q:q+4]=b.pointer(EMPTY)
  assert payload[:6]==base[HELPER:HELPER+6] and payload[-1:]==b'\x02'
  root=0x34B517;context=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert (TEXT-root,END-root) in b.spans_fr(base[root:context['end']])
  assert b.decode(base[TEXT:END],b.dictionary_from_rom(source))=='  Je le garderai bien au chaud.  '
  text=b.encode(FRENCH,p);assert len(text)<=END-TEXT;text+=b.encode(' ',p)*(END-TEXT-len(text))
  changes=[(CALL,b.pointer(destination)),(destination,bytes(payload)),(TEXT,text)]
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  normalized=bytearray(target[root:context['end']]);normalized[CALL-root:CALL-root+4]=b.pointer(HELPER)
  assert b.commands(bytes(normalized))==b.commands(base[root:context['end']])
  assert target[HELPER:0x38B5A2]==base[HELPER:0x38B5A2] and b.sprite_digest(target)==b.sprite_digest(base)
  out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/f'EarthBound_Beginnings_FR_v65_{p}.ips').write_bytes(ips)
  profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':3,'prior_records_preserved':len(b.records(priors[p]))}
  fixtures['profiles'][p]={'original_helper_hex':base[HELPER:0x38B5A2].hex(),'scoped_helper_hex':bytes(payload).hex(),'original_text_hex':base[TEXT:END].hex(),'replacement_text_hex':text.hex()}
 plan={'version':'v65','base':'v64','source_sha256':b.sha(source),'english_article_removed_in_storage':True,'gender_neutral_confirmation':True,'shared_helper_modified':False,'scoped_call_operands_changed':1,'scoped_dispatch_targets_changed':4,'new_allocation_bytes':size,'classifier_and_dispatch_opcodes_preserved':True,'sprites_preserved_against':'v64','natural_scene_access_verified':False,'profiles':profiles}
 for name,value in [('v65_fixtures',fixtures),('validation_v65',plan)]:
  (ROOT/f'tools/v65/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');args=ap.parse_args();print(json.dumps(build(args.rom,args.out),indent=2))
