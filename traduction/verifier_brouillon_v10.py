#!/usr/bin/env python3
"""Audit indépendant du brouillon v10, sans modifier la ROM ni intégrer du texte.

Usage :
 python traduction/verifier_brouillon_v10.py traduction/brouillon_v10_a_valider.json catalogue/catalogue.json --rom "EarthBound Beginnings (USA) 1.2.sfc"
Sans --rom : contrôles textuels seulement. Le statut "vérifié" ne signifie
pas que les branches, capacités de texte ou conditions de scénario sont validées.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

EXPECTED_SHA256 = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
COMMAND = re.compile(r'\[[0-9A-Fa-f ]+\]')
ACCENTS = 'éèêëàâîïôùûüçÉÀÇ'


def tokens(s):
    return COMMAND.findall(s)


def encoded_text(s):
    # Même jeu de caractères que traduction/integrer.py, sans coder les commandes.
    s = COMMAND.sub('', s).replace('\n', '').replace('\r', '')
    s = s.replace('Œ', 'Oe').replace('œ', 'oe').replace('’', "'").replace('–', '-').replace('…', '...')
    for c in s:
        if c in ACCENTS:
            continue
        if not (0x20 <= ord(c) <= 0x7a and c not in '"[\\]^'):
            raise ValueError('Caractère non représentable : ' + repr(c))
    return len(s)


def audit(draft, catalogue, rom=None):
    data = json.loads(Path(draft).read_text(encoding='utf-8-sig'))
    catalog = json.loads(Path(catalogue).read_text(encoding='utf-8-sig'))
    entries = {r['id']: r for r in catalog['entries']}
    ids = set()
    results = []
    b = None
    if rom:
        raw = Path(rom).read_bytes()
        b = raw[512:] if len(raw) % 0x8000 == 512 else raw
        if hashlib.sha256(b).hexdigest() != EXPECTED_SHA256:
            raise ValueError('ROM source non reconnue : SHA-256 incorrect.')
    for row in data['blocks']:
        id = row['id']
        if id in ids:
            raise ValueError('Identifiant dupliqué : ' + id)
        ids.add(id)
        src = entries.get(id)
        if src is None or src['category'] != 'script' or src['status'] != 'a_examiner':
            raise ValueError('Candidat absent ou déjà intégré : ' + id)
        english, french = row['english'], row['francais_propose']
        if english != src['english']:
            raise ValueError('Original modifié : ' + id)
        if tokens(english) != tokens(french):
            raise ValueError('Commandes différentes : ' + id)
        if english.count('@') != french.count('@') or english.count('\n') != french.count('\n'):
            raise ValueError('Marqueurs ou retours à la ligne différents : ' + id)
        en_size, fr_size = encoded_text(english), encoded_text(french)
        references = src.get('incoming_literal_candidates') or []
        if b is not None:
            pos = int(id, 16)
            if pos >= len(b):
                raise ValueError('Position hors ROM : ' + id)
            pointer = (0xc00000 + pos).to_bytes(4, 'little')
            for ref in references:
                rp = int(ref, 16)
                if b[rp:rp+4] != pointer:
                    raise ValueError('Référence littérale incorrecte : ' + id + ' @' + ref)
            # Au moins une séquence lisible doit être présente près du candidat.
            # Ceci ne prouve PAS que les frontières du script sont correctes.
            plain = COMMAND.sub(' ', english)
            phrases = re.findall(r'[A-Za-z][A-Za-z ]{6,}', plain)
            phrases = [p.strip() for p in phrases if len(p.strip()) >= 8]
            if phrases:
                needle = bytes(ord(c) + 48 for c in phrases[0][:8])
                if needle not in b[pos:pos+512]:
                    raise ValueError('Texte anglais introuvable dans la ROM : ' + id)
        results.append({'id': id, 'caracteres_source': en_size, 'caracteres_fr': fr_size,
                        'pointeurs_litteraux': len(references),
                        'rom_controlee': b is not None,
                        'necessite_relocalisation_possible': fr_size > en_size,
                        'statut': 'brouillon_non_integre'})
    return {'source': catalog.get('summary', {}).get('artifact_stem'),
            'blocs_controles': len(results),
            'rom_sha256_verifie': b is not None,
            'allongements_a_examiner': sum(r['necessite_relocalisation_possible'] for r in results),
            'avertissement': 'Vérification de cohérence seulement : pas de preuve de bon fonctionnement en jeu.',
            'details': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brouillon', type=Path)
    parser.add_argument('catalogue', type=Path)
    parser.add_argument('--rom', type=Path)
    parser.add_argument('--rapport', type=Path)
    args = parser.parse_args()
    report = audit(args.brouillon, args.catalogue, args.rom)
    if args.rapport:
        args.rapport.parent.mkdir(parents=True, exist_ok=True)
        args.rapport.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
