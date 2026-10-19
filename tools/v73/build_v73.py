"""Translate NPC 898's lodging service, keeping its native rest and branches."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
from safe_storage import safe_reserves
ENTRY=0x37899B;NO=0x378A32;RETURN=0x378A37;NPC=898;NPC_POINTER=0x2021A8+17*NPC+9
CONFIG=[
 (ENTRY,0x3789A2,0x3789A8,'@Well,','@Bon,'),
 (ENTRY,0x3789AA,0x3789BA," Dad isn't home.",' Papa est sorti.'),
 (ENTRY,0x3789BC,0x3789D6,"@I don't understand money.","@Je ne gère pas l'argent."),
 (ENTRY,0x3789D7,0x378A02,"  But I can do other stuff, so don't worry.",' Mais pour le reste, compte sur moi.'),
 (ENTRY,0x378A04,0x378A2B,'@You can stay here tonight if you want.','@Tu peux dormir ici cette nuit.'),
 (ENTRY,0x378A2E,0x378A31,'Yes','Oui'),
 (0x378AEE,0x378AEE,0x378AF2,'@Oh?','@Ah?'),
]
def flattened(data,destination):
 return data[ENTRY:NO]+data[destination:destination+6]+data[RETURN:0x378A4B]
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA;dic=b.dictionary_from_rom(source);old=json.loads((ROOT/'tools/v71/validation_v71.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v71_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()}
 for p in bases:assert b.sha(priors[p])==old['profiles'][p]['sha256'] and b.sha(bases[p])==old['profiles'][p]['target_rom_sha256']
 targets=set(b.pointer_index(source))
 for base in bases.values():targets.update(b.pointer_index(base))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);destination=next(a for a,z in reserves if z-a>=11)
 fixtures={'base':'v71','entry':f'{ENTRY:06X}','npc_id':NPC,'npc_pointer_operand':f'{NPC_POINTER:06X}','original_no_definition':f'{NO:06X}','continuation':f'{RETURN:06X}','copy_offset':f'{destination:06X}','copy_size':11,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'storage':storage,'profiles':{}};profiles={}
 for p,base in bases.items():
  assert base[NPC_POINTER:NPC_POINTER+4]==b.pointer(ENTRY);assert base[NO:RETURN]==b'\x19\x02'+b.encode('No',p)+b'\x02';assert base[destination:destination+11]==bytes(11);changes=[];proof=[];contexts={}
  for root,a,z,en,fr in CONFIG:
   parsed=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert parsed['terminal'] and not parsed['error'];contexts[root]=parsed['end'];assert (a-root,z-root) in b.spans_fr(base[root:parsed['end']]);assert b.decode(base[a:z],dic)==en;raw=b.encode(fr,p);assert len(raw)<=z-a,(hex(a),len(raw),z-a);raw+=b.encode(' ',p)*(z-a-len(raw));changes.append((a,raw));proof.append({'context':f'{root:06X}','offset':f'{a:06X}','end':f'{z:06X}','english':en,'french':fr,'baseline_hex':base[a:z].hex(),'replacement_hex':raw.hex()})
  helper=b'\x19\x02'+b.encode('Non',p)+b'\x02\x0a'+b.pointer(RETURN);assert len(helper)==11;changes.extend([(NO,b'\x0a'+b.pointer(destination)),(destination,helper)])
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  assert b.commands(flattened(target,destination))==b.commands(base[ENTRY:0x378A4B]);assert b.commands(target[0x378AEE:0x378B2F])==b.commands(base[0x378AEE:0x378B2F]);assert target[NPC_POINTER:NPC_POINTER+4]==base[NPC_POINTER:NPC_POINTER+4];assert b.sprite_digest(target)==b.sprite_digest(base);assert target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000]
  for root in (ENTRY,destination,RETURN):
   q=b.parse(target,root,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error']
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v73_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes)};fixtures['profiles'][p]={'edits':proof,'original_menu_hex':base[NO:RETURN].hex(),'helper_hex':helper.hex(),'jump_hex':target[NO:RETURN].hex()}
 plan={'version':'v73','input_patch_version':'v71','source_sha256':b.sha(source),'changed_text_spans':8,'native_commands_preserved_after_expanding_menu_bridge':True,'npc_pointers_rewritten':0,'menu_definition_bridge_bytes':5,'new_allocated_bytes':11,'bank25_unchanged':True,'sprites_preserved_against':'v71','natural_scene_access_verified':False,'profiles':profiles}
 for name,value in [('v73_fixtures',fixtures),('validation_v73',plan)]:(ROOT/f'tools/v73/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
