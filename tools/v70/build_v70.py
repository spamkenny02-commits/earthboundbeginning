"""Translate courier delivery messages in place, preserving native delivery commands."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
CONFIG=[
 (0x642A3,0x642AB,0x642BE,"@I'm from Escargo Express!!",'@Escargo Express !'),
 (0x642A3,0x642C0,0x642CF,"@I'm here to deliver your",'@Vos objets :'),
 (0x642A3,0x642F6,0x642F9,'  and ','et '),
 (0x642A3,0x64306,0x64314,'@Your charge is $18.','@Frais : 18 $.'),
 (0x642A3,0x64315,0x64326,'  You can pay for this, right?',' Tu peux payer ?'),
 (0x642A3,0x64339,0x6434F,'@Well, I need to take these things back then.','@Je ramène ces objets.'),
 (0x642A3,0x64351,0x64358,'@Is that OK?','@Ça va?'),
 (0x642A3,0x6436A,0x6437A,'@Hmmm, what should I do?','@Que faire ?'),
 (0x642A3,0x6437C,0x64390,"@You actually don't have any money, right?",'@Tu es sans argent ?'),
 (0x643A7,0x643A7,0x643AC,'@Okay.','@OK.'),
 (0x643A7,0x643AD,0x643BB,'  Call us again later.',' Rappelle-nous'),
 (0x6442F,0x6442F,0x6443A,'@Oh, you have too many things.','@Sac plein.'),
 (0x6442F,0x6443B,0x6444C,'  Please call us again later.',' Rappelle-nous.'),
 (0x6445F,0x6445F,0x6446D,"@I don't think you can carry everything.",'@Trop chargé.'),
 (0x6445F,0x64473,0x6447D,"@Well,  I'll leave just",'@Je livre'),
 (0x6445F,0x6447E,0x64480,'  the ','  '),
 (0x644A0,0x644A0,0x644AE,"@I don't think you can carry everything.",'@Trop chargé.'),
 (0x644A0,0x644B4,0x644C0,"@Well, I'll leave just",'@Je livre'),
 (0x644A0,0x644C1,0x644C3,'  the ','  '),
 (0x644A0,0x644C7,0x644CA,'  and',' et'),
 (0x644A0,0x644CE,0x644D0,' the ','  '),
 (0x644E3,0x644E3,0x64502,"@Ah, I see...  You don't have enough money.  Call us again later.","@Pas assez d'argent. Rappelle."),
 (0x64600,0x6460F,0x6461A,'@OK, here we are.','@Tiens.'),
 (0x64600,0x6461B,0x64620,'  Thank you!','Merci'),
]
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA;dic=b.dictionary_from_rom(source);prior_plan=json.loads((ROOT/'tools/v67/validation_v67.json').read_text());profiles={};fixtures={'base':'v67','profiles':{}}
 for p in ('accents','ascii'):
  prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes();assert b.sha(prior)==prior_plan['profiles'][p]['sha256'];base=b.apply(source,b.records(prior));assert b.sha(base)==prior_plan['profiles'][p]['target_rom_sha256'];changes=[];proof=[];contexts={}
  for root,a,z,en,fr in CONFIG:
   parsed=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert parsed['terminal'] and not parsed['error'];contexts[root]=parsed['end'];assert (a-root,z-root) in b.spans_fr(base[root:parsed['end']]);raw=base[a:z];assert b.decode(raw,dic)==en,(hex(a),b.decode(raw,dic));replacement=b.encode(fr,p);assert len(replacement)<=z-a,(hex(a),fr,len(replacement),z-a);replacement+=b.encode(' ',p)*(z-a-len(replacement));changes.append((a,replacement));proof.append({'context':f'{root:06X}','offset':f'{a:06X}','end':f'{z:06X}','english':en,'french':fr,'baseline_hex':raw.hex(),'replacement_hex':replacement.hex()})
  ips=b.append(prior,changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for root,z in contexts.items():assert b.commands(base[root:z])==b.commands(target[root:z])
  assert b.sprite_digest(base)==b.sprite_digest(target);assert base[0x250000:0x260000]==target[0x250000:0x260000]
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v70_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes)};fixtures['profiles'][p]=proof
 plan={'version':'v70','input_patch_version':'v67','source_sha256':b.sha(source),'changed_text_spans':len(CONFIG),'commands_preserved':True,'pointers_rewritten':0,'new_allocations':0,'sprite_digest_preserved_against':'v67','bank25_unchanged':True,'natural_initial_phone_access_verified':False,'profiles':profiles}
 for name,value in [('v70_fixtures',fixtures),('validation_v70',plan)]:(ROOT/f'tools/v70/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
