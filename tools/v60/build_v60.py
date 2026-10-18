"""Translate credit roles in place, preserving names, controls and scroll height.
Format: CoilSnake StaffModule / eb_staff_chars.yml at pinned commit
346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a. No graphics are modified.
"""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v59'))
from build_v59 import ROM_SHA,SIZE,sha,records,apply,append,sprite_digest
START=0x17FBE8
CAPACITY=1026
POINTER_SITE=0x4F252
POINTER_HEX='a9e8fb8de7b4a9d7008de9b4'
HEIGHT_SITES=(0x4F583,0x4F58C,0x4F66F)
TITLES={
 'STAFF':'EQUIPE',
 'PRODUCED AND DIRECTED BY':'PRODUCTION ET REALISATION',
 'GAME DESIGNERS':'CONCEPTION',
 'MUSIC PRODUCERS':'PRODUCTION MUSICALE',
 'MUSICAL EFFECTS':'EFFETS MUSICAUX',
 'PROGRAM DIRECTOR':'DIRECTION TECHNIQUE',
 'CHARACTER DESIGNERS':'PERSONNAGES',
 'FIGURE MODELING':'MODELAGE',
 'PROGRAMMERS':'PROGRAMMATION',
 'SCENARIO ASSISTANTS':'AIDE AU SCENARIO',
 'COORDINATORS':'COORDINATION',
 'ENGLISH SCRIPT WRITER':'TEXTE ANGLAIS',
 'TRANSLATORS':'TRADUCTION',
 'PRODUCER':'PRODUCTION',
 'EXECUTIVE PRODUCER':'PRODUCTION EXECUTIVE',
 'SPECIAL THANKS TO':'REMERCIEMENTS',
 'PRESENTED BY':'PRESENTE PAR',
 'IN ASSOCIATION WITH':'EN ASSOCIATION AVEC',
 'AND':'ET','AND...':'ET...','PLAYER':'JOUEUR'
}
MAPS=json.loads((ROOT/'tools/v60/staff_chars.json').read_text())

def decode_staff(raw):
 entries=[];i=0;height=0
 while i<len(raw):
  c=raw[i];start=i;i+=1
  if c==255:return entries,height,i
  if c in (1,2):
   kind='small' if c==1 else 'big';z=raw.find(b'\0',i)
   if z<0:raise ValueError('Ligne sans terminateur')
   inverse={v:k for k,v in MAPS[kind].items()}
   try:text=''.join(inverse[b] for b in raw[i:z])
   except KeyError as e:raise ValueError('Glyphe inconnu') from e
   if len(text)>32:raise ValueError('Ligne trop longue')
   i=z+1;height+=8 if c==1 else 16
   entries.append({'type':kind,'text':text,'raw_hex':raw[start:i].hex()})
  elif c==3:
   if i>=len(raw):raise ValueError('Espacement tronqué')
   height+=8*raw[i];entries.append({'type':'space','rows':raw[i],'raw_hex':raw[start:i+1].hex()});i+=1
  elif c==4:height+=16;entries.append({'type':'player_name','raw_hex':'04'})
  else:raise ValueError('Commande de générique inconnue')
 raise ValueError('Générique sans fin')

def translate(raw):
 entries,height,size=decode_staff(raw)
 if size!=len(raw):raise ValueError('Octets après le générique source')
 result=bytearray();titles=[];names=[]
 for i,e in enumerate(entries):
  text=e.get('text')
  if text in TITLES:
   fr=TITLES[text]
   if len(fr)>32:raise ValueError('Intitulé trop long')
   try:encoded=bytes(MAPS[e['type']][c] for c in fr)
   except KeyError as err:raise ValueError('Glyphe français absent') from err
   result.extend(bytes([1 if e['type']=='small' else 2])+encoded+b'\0');titles.append({'entry_index':i,'en':text,'fr':fr})
  else:
   result.extend(bytes.fromhex(e['raw_hex']))
   if e['type']=='big' and text.strip('_ '):names.append(text)
 result.append(255)
 if len(titles)!=len(TITLES) or len({e['en'] for e in titles})!=len(TITLES):raise ValueError('Inventaire des intitulés divergent')
 if len(result)>CAPACITY:raise ValueError('Capacité du générique dépassée')
 translated,h,n=decode_staff(bytes(result))
 if h!=height or [(e['type'],e.get('rows')) for e in entries]!=[(e['type'],e.get('rows')) for e in translated]:raise ValueError('Défilement modifié')
 return bytes(result),{'titles':titles,'names_preserved':names,'height_pixels':height,'source_length':size,'translated_length':len(result)}

def fixtures(source,bases):
 if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
 raw=source[START:START+CAPACITY];new,report=translate(raw)
 for p,data in bases.items():
  if data[START:START+CAPACITY]!=raw:raise ValueError('Générique antérieur modifié')
  if data[POINTER_SITE:POINTER_SITE+12]!=bytes.fromhex(POINTER_HEX):raise ValueError('Chargeur de générique divergent')
  if any(int.from_bytes(data[a:a+2],'little')!=report['height_pixels'] for a in HEIGHT_SITES):raise ValueError('Hauteur moteur divergente')
 return {'version':'v60','base':'v59','offset':f'{START:06X}','capacity':CAPACITY,'source_hex':raw.hex(),'translated_hex':new.hex(),'pointer_site':f'{POINTER_SITE:06X}','pointer_hex':POINTER_HEX,'height_sites':[f'{a:06X}' for a in HEIGHT_SITES],**report}

def additions(f):
 raw=bytes.fromhex(f['source_hex']);new,report=translate(raw)
 if f['offset']!=f'{START:06X}' or f['capacity']!=CAPACITY or new.hex()!=f['translated_hex']:raise ValueError('Fixture de générique divergente')
 for key,value in report.items():
  if f[key]!=value:raise ValueError('Rapport de générique divergent')
 return [(START,new)]

def build(rom,out):
 source=Path(rom).read_bytes();old=json.loads((ROOT/'tools/v59/validation_v59.json').read_text());priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v59_{p}.ips').read_bytes() for p in ('accents','ascii')}
 if any(sha(v)!=old['profiles'][p]['sha256'] for p,v in priors.items()):raise ValueError('IPS V59 divergent')
 bases={p:apply(source,records(v)) for p,v in priors.items()};f=fixtures(source,bases);changes=additions(f);out=Path(out);out.mkdir(exist_ok=True,parents=True);profiles={}
 for p,base in bases.items():
  ips=append(priors[p],changes);target=apply(source,records(ips))
  if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
  if sprite_digest(target)!=sprite_digest(base):raise ValueError('Sprites modifiés')
  (out/f'EarthBound_Beginnings_FR_v60_{p}.ips').write_bytes(ips);profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':1,'prior_records_preserved':len(records(priors[p]))}
 plan={'version':'v60','source_sha256':sha(source),'credit_titles_translated':len(f['titles']),'credit_names_preserved':len(f['names_preserved']),'credit_height_unchanged':True,'graphics_modified':False,'menus_modified':False,'natural_credits_access_verified':False,'profiles':profiles}
 for name,value in (('v60_fixtures',f),('validation_v60',plan)):(ROOT/f'tools/v60/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 return plan
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
