"""Translate desert mines, ticket/tank messages and camel selectors."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
from safe_storage import safe_reserves
ENTRY=0x374307;NPC=894;NPC_POINTER=0x2021A8+17*NPC+9
MENUS=[(ENTRY,0x374353,0x374356,0x374357,0x37435C,0x374370)]
CONFIG=[
 (0x3738F8,0x373919,0x37392E,'@During the last war,','@Lors de la guerre,'),
 (0x3738F8,0x373930,0x37394D,' I laid mines in this desert.'," j'ai miné ce désert."),
 (0x3738F8,0x37394F,0x373973,'@Je les ai tous ôtés sauf un...     ','@Je les ai toutes ôtées sauf une...'),
 (0x3738F8,0x373975,0x37398D,' better watch your step!',' fais attention à toi !'),
 (0x373C34,0x373C39,0x373C42,'@(You got','@(Reçu :'),
 (0x373C34,0x373C43,0x373C49,'  the ',' '),
 (0x373C34,0x373C72,0x373C89,' you can ride the tank!',' monte dans le char !'),
 (0x373C34,0x373CD8,0x373CDE,'@Well,','@Bon,'),
 (0x373C34,0x373CE0,0x373CF9,' it is quite expensive...', " c'est assez cher..."),
 (0x373C34,0x373CFA,0x373D0E,"  I don't blame you.",' Je te comprends.'),
 (ENTRY,0x374323,0x374350,'@Want to know how to walk when in the desert?','@Veux-tu apprendre à marcher dans le désert ?'),
 (ENTRY,0x374353,0x374356,'Yes','Oui'),
 (0x374409,0x37442B,0x374446,"@Wouldn't you like to know?",'@Tu ne veux pas savoir ?'),
]
CONTEXTS=(0x3738F8,0x373C34,0x373CD8,0x374409)
def flattened(data,menu,dest):
 root,yes,endyes,no,ret,end=menu
 return data[root:no]+data[dest:dest+6]+data[ret:end]
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA;dic=b.dictionary_from_rom(source);old=json.loads((ROOT/'tools/v76/validation_v76.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v76_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()}
 for p in bases:assert b.sha(priors[p])==old['profiles'][p]['sha256'] and b.sha(bases[p])==old['profiles'][p]['target_rom_sha256']
 targets=set(b.pointer_index(source))
 for base in bases.values():targets.update(b.pointer_index(base))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);free=[r[:] for r in reserves];destinations=[]
 for menu in MENUS:
  free.sort(key=lambda r:(-(r[1]-r[0]),r[0]));region=next(r for r in free if r[1]-r[0]>=11);destinations.append(region[0]);region[0]=(region[0]+14)&~3
 fixtures={'base':'v76','entry':f'{ENTRY:06X}','npc_id':NPC,'npc_pointer_operand':f'{NPC_POINTER:06X}','storage':storage,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'menus':[{'context':f'{root:06X}','yes_start':f'{yes:06X}','yes_end':f'{endyes:06X}','no_definition':f'{no:06X}','continuation':f'{ret:06X}','context_end':f'{end:06X}','destination':f'{dest:06X}','size':11} for (root,yes,endyes,no,ret,end),dest in zip(MENUS,destinations)],'profiles':{}};profiles={}
 for p,base in bases.items():
  assert base[NPC_POINTER:NPC_POINTER+4]==b.pointer(ENTRY);changes=[];proof=[]
  for root,a,z,en,fr in CONFIG:
   parsed=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert parsed['terminal'] and not parsed['error'];assert (a-root,z-root) in b.spans_fr(base[root:parsed['end']]);assert b.decode(base[a:z],dic)==b.decode(b.encode(en,p),dic);raw=b.encode(fr,p);assert len(raw)<=z-a;raw+=b.encode(' ',p)*(z-a-len(raw));changes.append((a,raw));proof.append({'context':f'{root:06X}','offset':f'{a:06X}','end':f'{z:06X}','baseline_text':en,'french':fr,'baseline_hex':base[a:z].hex(),'replacement_hex':raw.hex()})
  for menu,dest in zip(MENUS,destinations):
   root,yes,endyes,no,ret,end=menu;assert base[no:ret]==b'\x19\x02'+b.encode('No',p)+b'\x02';assert base[dest:dest+11]==bytes(11);helper=b'\x19\x02'+b.encode('Non',p)+b'\x02\x0a'+b.pointer(ret);changes.extend([(no,b'\x0a'+b.pointer(dest)),(dest,helper)])
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for menu,dest in zip(MENUS,destinations):
   root,yes,endyes,no,ret,end=menu;assert b.commands(flattened(target,menu,dest))==b.commands(base[root:end])
   for address in (root,dest,ret):
    q=b.parse(target,address,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error']
  for root in CONTEXTS:
   end=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0))['end'];assert b.commands(target[root:end])==b.commands(base[root:end])
  assert b.commands(flattened(target,(0x374351,*MENUS[0][1:]),destinations[0]))==b.commands(base[0x374351:0x374370])
  assert target[NPC_POINTER:NPC_POINTER+4]==base[NPC_POINTER:NPC_POINTER+4];assert b.sprite_digest(target)==b.sprite_digest(base);assert target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000]
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v77_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes)};fixtures['profiles'][p]={'edits':proof,'bridge_records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes[len(CONFIG):]]}
 plan={'version':'v77','input_patch_version':'v76','source_sha256':b.sha(source),'changed_text_spans':14,'english_text_spans_translated':13,'existing_french_spans_polished':1,'native_commands_preserved_after_expanding_menu_bridges':True,'npc_pointers_rewritten':0,'menu_bridges':1,'new_allocated_bytes':11,'bank25_unchanged':True,'sprites_preserved_against':'v76','natural_scene_access_verified':False,'profiles':profiles}
 for name,value in [('v77_fixtures',fixtures),('validation_v77',plan)]:(ROOT/f'tools/v77/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
