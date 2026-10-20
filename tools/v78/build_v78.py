"""V78 batch checkpoint: remaining custom NPC text; release target 150 distinct texts."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
from safe_storage import safe_reserves
ENTRY=0x36EB50;NPC=411;NPC_POINTER=0x2021A8+17*NPC+9
MENUS=[
 (0x36EB50,0x36EB83,0x36EB86,0x36EB87,0x36EB8C,0x36EBA0),
 (0x376ABE,0x376B0B,0x376B0E,0x376B0F,0x376B14,0x376B28),
 (0x376BB7,0x376C0D,0x376C10,0x376C11,0x376C16,0x376C2A),
 (0x377108,0x37715F,0x377162,0x377163,0x377168,0x37717C),
 (0x380A2A,0x380A46,0x380A49,0x380A4A,0x380A4F,0x380A63),
]
CONFIG=[
 (0x376ABE,0x376ACE,0x376AD4,'@(Huh,','@(Hein'),
 (0x376ABE,0x376AD6,0x376ADD,' what?)',' quoi?)'),
 (0x376ABE,0x376AED,0x376B08,'@(Do I look like a monkey?)','@(Je ressemble à un singe?)'),
 (0x376BB7,0x376BC3,0x376BD6,'@(Cool down, dude.)','@(Du calme, mec.)'),
 (0x376BB7,0x376BE7,0x376C0A,'@(Are you so serious all the time?)','@(Es-tu toujours aussi sérieux?)'),
 (0x377108,0x377122,0x377147,"@(I've got a good story to tell you.)",'@(Je connais une bonne histoire.)'),
 (0x377108,0x377149,0x37715C,'@(Want to hear it?)','@(Tu veux savoir?)'),
 (0x37D45C,0x37D47F,0x37D48B,'  Watch out!','  Attention!'),
 (0x37D45C,0x37D494,0x37D4BE,"@(Incredibly enough, you found somebody's ",'@(Tiens ! Tu trouves un objet perdu : '),
 (0x37D45C,0x37D4C1,0x37D4D8,' right under the sign!)',' sous ce panneau !)'),
 (0x380A2A,0x380A2A,0x380A43,'@(Climb into the rocket?)','@(Monter dans la fusée ?)'),
 *[(root,yes,endyes,'Yes','Oui') for root,yes,endyes,no,ret,end in MENUS],
]
def flattened(data,menu,dest):
 root,yes,endyes,no,ret,end=menu
 return data[root:no]+data[dest:dest+6]+data[ret:end]
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA;dic=b.dictionary_from_rom(source);old=json.loads((ROOT/'tools/v77/validation_v77.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()}
 for p in bases:assert b.sha(priors[p])==old['profiles'][p]['sha256'] and b.sha(bases[p])==old['profiles'][p]['target_rom_sha256']
 targets=set(b.pointer_index(source))
 for base in bases.values():targets.update(b.pointer_index(base))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);free=[r[:] for r in reserves];destinations=[]
 for menu in MENUS:
  free.sort(key=lambda r:(-(r[1]-r[0]),r[0]));region=next(r for r in free if r[1]-r[0]>=11);destinations.append(region[0]);region[0]=(region[0]+14)&~3
 fixtures={'base':'v77','entry':f'{ENTRY:06X}','npc_id':NPC,'npc_pointer_operand':f'{NPC_POINTER:06X}','storage':storage,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'menus':[{'context':f'{root:06X}','yes_start':f'{yes:06X}','yes_end':f'{endyes:06X}','no_definition':f'{no:06X}','continuation':f'{ret:06X}','context_end':f'{end:06X}','destination':f'{dest:06X}','size':11} for (root,yes,endyes,no,ret,end),dest in zip(MENUS,destinations)],'profiles':{}};profiles={}
 for p,base in bases.items():
  assert base[NPC_POINTER:NPC_POINTER+4]==b.pointer(ENTRY);changes=[];proof=[]
  for root,a,z,en,fr in CONFIG:
   parsed=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert parsed['terminal'] and not parsed['error'];assert (a-root,z-root) in b.spans_fr(base[root:parsed['end']]);assert b.decode(base[a:z],dic)==en;raw=b.encode(fr,p);assert len(raw)<=z-a;raw+=b.encode(' ',p)*(z-a-len(raw));changes.append((a,raw));proof.append({'context':f'{root:06X}','offset':f'{a:06X}','end':f'{z:06X}','english':en,'french':fr,'baseline_hex':base[a:z].hex(),'replacement_hex':raw.hex()})
  for menu,dest in zip(MENUS,destinations):
   root,yes,endyes,no,ret,end=menu;assert base[no:ret]==b'\x19\x02'+b.encode('No',p)+b'\x02';assert base[dest:dest+11]==bytes(11);helper=b'\x19\x02'+b.encode('Non',p)+b'\x02\x0a'+b.pointer(ret);changes.extend([(no,b'\x0a'+b.pointer(dest)),(dest,helper)])
  ips=b.append(priors[p],changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for menu,dest in zip(MENUS,destinations):
   root,yes,endyes,no,ret,end=menu;assert b.commands(flattened(target,menu,dest))==b.commands(base[root:end])
   for address in (root,dest,ret):
    q=b.parse(target,address,8192,extra_glyphs=range(0xB0,0xC0));assert q['terminal'] and not q['error']
  end=b.parse(base,0x37D45C,8192,extra_glyphs=range(0xB0,0xC0))['end'];assert b.commands(target[0x37D45C:end])==b.commands(base[0x37D45C:end])
  assert target[0x2021A8:0x2021A8+1584*17]==base[0x2021A8:0x2021A8+1584*17]
  assert target[NPC_POINTER:NPC_POINTER+4]==base[NPC_POINTER:NPC_POINTER+4];assert b.sprite_digest(target)==b.sprite_digest(base);assert target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000]
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v78_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes)};fixtures['profiles'][p]={'edits':proof,'bridge_records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes[len(CONFIG):]]}
 plan={'version':'v78','input_patch_version':'v77','source_sha256':b.sha(source),'changed_text_spans':21,'distinct_new_translations':13,'batch_target_distinct_texts':150,'release_pending':True,'native_commands_preserved_after_expanding_menu_bridges':True,'npc_pointers_rewritten':0,'menu_bridges':5,'new_allocated_bytes':55,'bank25_unchanged':True,'sprites_preserved_against':'v77','natural_scene_access_verified':False,'profiles':profiles}
 for name,value in [('v78_fixtures',fixtures),('validation_v78',plan)]:(ROOT/f'tools/v78/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 from medical_stage import extend
 plan=extend(source,out,plan,fixtures)
 from remaining_stage import extend as extend_remaining
 plan=extend_remaining(source,out,plan,fixtures)
 from item_help_stage import extend as extend_help
 plan=extend_help(source,out,plan,fixtures)
 from scoped_help_stage import extend as extend_scoped
 return extend_scoped(source,out,plan,fixtures)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
