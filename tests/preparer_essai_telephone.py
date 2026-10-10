#!/usr/bin/env python3
"""Créer une ROM de test isolé ; jamais un patch destiné au joueur.

Le texte « À qui ? » saute vers un dialogue du père. Six octets au maximum
diffèrent de la ROM intégrée, dont l'empreinte est vérifiée par son rapport.
Le parcours familial, les sommes en banque et les conditions de quête ne sont
pas validés par cette entrée directe. Aucun octet de la ROM n'est distribué.
"""
import argparse,hashlib,json
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('rom',type=Path);p.add_argument('rapport',type=Path);p.add_argument('sortie',type=Path)
p.add_argument('--entree',choices=['conversation','virement'],default='conversation')
a=p.parse_args();source=a.rom.read_bytes();report=json.loads(a.rapport.read_text(encoding='utf-8'))
assert hashlib.sha256(source).hexdigest()==report['target_sha256']
target=0x35c5d9 if a.entree=='conversation' else 0x35c5fe
out=bytearray(source);offset=0x07c588
out[offset:offset+6]=b'\x0a'+(0xc00000+target).to_bytes(4,'little')+b'\x02'
assert all(x==y for i,(x,y) in enumerate(zip(source,out)) if not offset<=i<offset+6)
a.sortie.parent.mkdir(parents=True,exist_ok=True);a.sortie.write_bytes(out)
metadata={'scope':'Entrée directe de test ; parcours et finances non validés',
          'base_rom_sha256':report['target_sha256'],'test_rom_sha256':hashlib.sha256(out).hexdigest(),
          'entry':a.entree,'entry_offset':f'{target:06X}','changed_interval':['07C588','07C58E']}
a.sortie.with_suffix('.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metadata,ensure_ascii=False))
