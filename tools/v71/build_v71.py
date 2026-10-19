"""Translate the native Escargo pickup graph without changing its commands."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v62'))
import runtime as b
CONFIG=[
 (0x63EB0,0x63ED0,0x63EE4,'@Hello, this is Escargo Express!','@Escargo Express !'),
 (0x63EB0,0x63EE6,0x63EFA,'@Your delivery charge is $18.','@Frais : 18 $.'),
 (0x63EB0,0x63EFC,0x63F0D,'@You can cover the bill, right?','@Tu peux payer ?'),
 (0x63EB0,0x63F1F,0x63F25,'@Oh, I see.','@Ah.'),
 (0x63EB0,0x63F26,0x63F34,'  Please try us again.',' Rappelle.'),
 (0x63F74,0x63F80,0x63F8C,'@What do you want me to take?','@Quel objet?'),
 (0x63F74,0x63F8E,0x63F9F,'@I can take up to three things.','@Trois au plus.'),
 (0x63F74,0x63FDB,0x63FE6,'  Will there be anything else?',' Autre ?'),
 (0x640A1,0x640A1,0x640C1,'@Let me just confirm your request.  You want me to take','@Je prends ces objets :'),
 (0x640A1,0x640C7,0x640CA,'@the ','@'),
 (0x640A1,0x640D8,0x640DA,'  the ','  '),
 (0x640A1,0x640E8,0x640ED,'  and the ',' et '),
 (0x640A1,0x640F3,0x640FF,'@Is this correct?',"@C'est bon ?"),
 (0x64155,0x64179,0x6418C,"@Well, let's start again, shall we?",'@On recommence ?'),
 (0x63FFD,0x63FFD,0x64009,'@What do you want me to take?','@Quel objet?'),
 (0x63FFD,0x64044,0x6404F,'  Will there be anything else?',' Autre ?'),
 (0x64066,0x64066,0x64077,'@Which one do you want me to take?','@Quel objet ?'),
 (0x64116,0x6412E,0x6413D,'@All right, certainly,',"@D'accord,"),
 (0x64116,0x6413E,0x64147,'  thanks a lot!',' merci !'),
 (0x64633,0x64633,0x6463E,'@I think you should keep it.','@Garde-le.'),
 (0x64633,0x64640,0x6464E,'@Do you have anything else you want me to take?','@Autre objet ?'),
 (0x64240,0x64242,0x64260,"@We're sorry, we cannot carry more than three items.",'@Trois objets au maximum.'),
 (0x64240,0x64262,0x64275,"@Please understand that it's our policy.","@C'est notre règle."),
 (0x6427C,0x6427C,0x64284,"@You don't have enough money.",'@Sans $.'),
 (0x6427C,0x64286,0x64295,'@Call us at another time.','@Rappelle-nous.'),
 (0x63F42,0x63F42,0x63F58,"@Hi, I'm from Escargo Express.",'@Escargo Express !'),
 (0x63F42,0x63F5A,0x63F6D,"@I'm here to pick up your stuff.",'@Pour tes objets.'),
 (0x641B0,0x641B0,0x641B9,'@Excuse me.','@Pardon.'),
 (0x641B0,0x641BB,0x641D1,'@We checked your records and found','@Après vérification,'),
 (0x641B0,0x641D3,0x641EE,'@that we are already storing too many of your items.','@ta réserve est pleine.'),
 (0x641B0,0x641F0,0x6420E,'@We cannot accept any more goods from you at this time.',"@Impossible d'en prendre plus."),
 (0x641B0,0x64210,0x64232,'@Please contact us later when we may have space for your items.',"@Fais de la place et rappelle."),
]
def build(rom,out):
 source=Path(rom).read_bytes();assert b.sha(source)==b.ROM_SHA;dic=b.dictionary_from_rom(source);prior_plan=json.loads((ROOT/'tools/v70/validation_v70.json').read_text());profiles={};fixtures={'base':'v70','profiles':{}}
 for p in ('accents','ascii'):
  prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v70_{p}.ips').read_bytes();assert b.sha(prior)==prior_plan['profiles'][p]['sha256'];base=b.apply(source,b.records(prior));assert b.sha(base)==prior_plan['profiles'][p]['target_rom_sha256'];changes=[];proof=[];contexts={}
  for root,a,z,en,fr in CONFIG:
   parsed=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0));assert parsed['terminal'] and not parsed['error'];contexts[root]=parsed['end'];assert (a-root,z-root) in b.spans_fr(base[root:parsed['end']]);raw=base[a:z];assert b.decode(raw,dic)==en,(hex(a),b.decode(raw,dic));replacement=b.encode(fr,p);assert len(replacement)<=z-a,(hex(a),fr,len(replacement),z-a);replacement+=b.encode(' ',p)*(z-a-len(replacement));changes.append((a,replacement));proof.append({'context':f'{root:06X}','offset':f'{a:06X}','end':f'{z:06X}','english':en,'french':fr,'baseline_hex':raw.hex(),'replacement_hex':replacement.hex()})
  ips=b.append(prior,changes);target=b.apply(source,b.records(ips));assert target==b.apply(base,changes)
  for root,z in contexts.items():assert b.commands(base[root:z])==b.commands(target[root:z])
  assert b.sprite_digest(base)==b.sprite_digest(target);assert base[0x250000:0x260000]==target[0x250000:0x260000]
  Path(out).mkdir(parents=True,exist_ok=True);(Path(out)/f'EarthBound_Beginnings_FR_v71_{p}.ips').write_bytes(ips);profiles[p]={'sha256':b.sha(ips),'target_rom_sha256':b.sha(target),'records_added':len(changes)};fixtures['profiles'][p]=proof
 plan={'version':'v71','input_patch_version':'v70','source_sha256':b.sha(source),'changed_text_spans':len(CONFIG),'commands_preserved':True,'pointers_rewritten':0,'new_allocations':0,'sprite_digest_preserved_against':'v70','bank25_unchanged':True,'natural_initial_phone_access_verified':False,'profiles':profiles}
 for name,value in [('v71_fixtures',fixtures),('validation_v71',plan)]:(ROOT/f'tools/v71/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
