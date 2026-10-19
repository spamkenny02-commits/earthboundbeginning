"""Translate the canary conversation, melody selectors and song response."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
from safe_storage import safe_reserves
ENTRY=0x3861D3;NPC=291;NPC_POINTER=0x2021A8+17*NPC+9
MENUS=[(ENTRY,0x386236,0x386239,0x38623A,0x38623F,0x386253),(0x32CC90,0x32CCE6,0x32CCE9,0x32CCEA,0x32CCEF,0x32CD03)]
CONFIG=[
 (ENTRY,0x3861E4,0x386213,"@Wow! That canary is Laura the songbird's baby.",'@Oh ! Ce canari est le petit de Laura.'),
 (ENTRY,0x386215,0x386233,'@Will you give it back to her?','@Vas-tu le lui rendre ?'),
 *[(r,a,z,'Yes','Oui') for r,a,z,no,ret,end in MENUS],
 (0x38636E,0x386380,0x386397,"@There's power in song.",'@Le chant a du pouvoir.'),
]
def flattened(data,menu,dest):
 root,yes,endyes,no,ret,end=menu
 return data[root:no]+data[dest:dest+6]+data[ret:end]
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA;dic=b.dictionary_from_rom(source);old=json.loads((ROOT/'tools/v74/validation_v74.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v74_{p}.ips').read_bytes() for p in ('accents','ascii')};bases={p:b.apply(source,b.records(v)) for p,v in priors.items()}
 for p in bases:assert b.sha(priors[p])==old['profiles'][p]['sha256'] and b.sha(bases[p])==old['profiles'][p]['target_rom_sha256']
 targets=set(b.pointer_index(source))
 for base in bases.values():targets.update(b.pointer_index(base))
 targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(source,bases,priors,targets,b.records);free=[r[:] for r in reserves];destinations=[]
 for menu in MENUS:
  free.sort(key=lambda r:(-(r[1]-r[0]),r[0]));region=next(r for r in free if r[1]-r[0]>=11);destinations.append(region[0]);region[0]=(region[0]+14)&~3
 fixtures={'base':'v74','entry':f'{ENTRY:06X}','npc_id':NPC,'npc_pointer_operand':f'{NPC_POINTER:06X}','storage':storage,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves],'menus':[{'context':f'{root:06X}','yes_start':f'{yes:06X}','yes_end':f'{endyes:06X}','no_definition':f'{no:06X}','continuation':f'{ret:06X}','context_end':f'{end:06X}','destination':f'{dest:06X}','size':11} for (root,yes,endyes,no,ret,end),dest in zip(MENUS,destinations)],'profiles':{}};profiles={}
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
  end=b.parse(base,0x38636E,8192,extra_glyphs=range(0xB0,0xC0))['end'];assert b.commands(target[0x38636E:end])==b.commands(base[0x38636E:end])
  assert target[NPC_POINTER:NPC_POINTER+4]==base[NPC_POINTER:NPC_POINTER+4];assert b.sprite_digest(target)==b.sprite_digest(base);assert target[0x250000:0x260000]==base[0x250000:0x260000];assert target[0x330FC0:0x331000]==base[0x330FC0:0x331000]
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v75_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes)};fixtures['profiles'][p]={'edits':proof,'bridge_records':[{'offset':f'{a:06X}','hex':raw.hex()} for a,raw in changes[len(CONFIG):]]}
 plan={'version':'v75','input_patch_version':'v74','source_sha256':b.sha(source),'changed_text_spans':7,'native_commands_preserved_after_expanding_menu_bridges':True,'npc_pointers_rewritten':0,'menu_bridges':2,'new_allocated_bytes':22,'bank25_unchanged':True,'sprites_preserved_against':'v74','natural_scene_access_verified':False,'profiles':profiles}
 for name,value in [('v75_fixtures',fixtures),('validation_v75',plan)]:(ROOT/f'tools/v75/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
