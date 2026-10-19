"""Translate Pippi's introduction, Podunk encounter, secret and morning line."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
ENTRY=0x386B63;NPC=319;NPC_POINTER=0x2021A8+17*NPC+9
CONFIG=[
 (ENTRY,0x386B6D,0x386B76,"@It's me,",'@Moi,'),
 (ENTRY,0x386B8C,0x386B9F,'@We meet once more,','@On se revoit,'),
 (0x386BAD,0x386BAD,0x386BB4,'@I met ','@Ah, '),
 (0x386BAD,0x386BB7,0x386BC7,' back in Podunk!',', de Podunk !'),
 (0x386BAD,0x386BDF,0x386C05," but I didn't tell my mom I came here.",' mais Maman ignore que je suis ici.'),
 (0x386C58,0x386C58,0x386C66,'@Good morning!','@Bonjour !'),
]
CONTEXTS=(ENTRY,0x386BAD,0x386BC9,0x386C58)
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA;dic=b.dictionary_from_rom(source);old=json.loads((ROOT/'tools/v75/validation_v75.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v75_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()}
 for p in bases:assert b.sha(priors[p])==old['profiles'][p]['sha256'] and b.sha(bases[p])==old['profiles'][p]['target_rom_sha256']
 fixtures={'base':'v75','entry':f'{ENTRY:06X}','npc_id':NPC,'npc_pointer_operand':f'{NPC_POINTER:06X}','profiles':{}};profiles={}
 for p,base in bases.items():
  assert base[NPC_POINTER:NPC_POINTER+4]==b.pointer(ENTRY);changes=[];proof=[];ends={}
  for root in CONTEXTS:
   q=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error'];ends[root]=q['end']
  for root,a,z,en,fr in CONFIG:
   assert (a-root,z-root) in b.spans_fr(base[root:ends[root]]);assert b.decode(base[a:z],dic)==en;raw=b.encode(fr,p);assert len(raw)<=z-a,(hex(a),len(raw),z-a);raw+=b.encode(' ',p)*(z-a-len(raw));changes.append((a,raw));proof.append({'context':f'{root:06X}','offset':f'{a:06X}','end':f'{z:06X}','english':en,'french':fr,'baseline_hex':base[a:z].hex(),'replacement_hex':raw.hex()})
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for root,end in ends.items():
   assert b.commands(target[root:end])==b.commands(base[root:end]);q=b.parse(target,root,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error']
  assert target[NPC_POINTER:NPC_POINTER+4]==base[NPC_POINTER:NPC_POINTER+4];assert b.sprite_digest(target)==b.sprite_digest(base);assert target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000]
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v76_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes)};fixtures['profiles'][p]={'edits':proof}
 plan={'version':'v76','input_patch_version':'v75','source_sha256':b.sha(source),'changed_text_spans':6,'new_allocated_bytes':0,'native_commands_preserved':True,'npc_pointers_rewritten':0,'bank25_unchanged':True,'sprites_preserved_against':'v75','natural_scene_access_verified':False,'profiles':profiles}
 for name,value in [('v76_fixtures',fixtures),('validation_v76',plan)]:(ROOT/f'tools/v76/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
