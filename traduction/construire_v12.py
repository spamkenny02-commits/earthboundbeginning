#!/usr/bin/env python3
"""Construit V12 : patch IPS autonome = V11 fusionnée + 18 dialogues.

Vérifie la ROM USA 1.2, les blocs originaux, les références HiROM, les tailles,
les collisions et l'équivalence binaire du patch final. Ne publie pas de ROM.
"""
import argparse
import hashlib
import json
from pathlib import Path

from construire_v11 import ROM_SHA, encode, parse_ips, apply_ips, original_block, check_pointers

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'traduction/v12_nouveaux_dialogues.json'


def build(source, previous, manifest):
    if hashlib.sha256(source).hexdigest() != ROM_SHA:
        raise ValueError('ROM source incorrecte : SHA-256')
    entries = manifest['entries']
    if len(entries) != len({e['id'] for e in entries}):
        raise ValueError('Identifiants dupliqués')
    spans = []
    for e in entries:
        pos, old = original_block(source, e)
        spans.append((e['id'], pos, pos+len(old)))
        for accents in (True, False):
            if 1+len(encode(e['fr'], accents))+2 > len(old):
                raise ValueError('Texte trop long : ' + e['id'])
    spans.sort(key=lambda r: r[1])
    for left, right in zip(spans, spans[1:]):
        if left[2] > right[1]:
            raise ValueError('Chevauchement interne : ' + left[0])
    pointers = check_pointers(source, spans)
    results = {}
    for profile in ('accents', 'ascii'):
        previous_ips = previous[profile]
        previous_rom = apply_ips(source, previous_ips)
        for id, start, end in spans:
            if previous_rom[start:end] != source[start:end]:
                raise ValueError('Bloc déjà modifié dans V11 : ' + id)
        records = []
        target = bytearray(previous_rom)
        for e in entries:
            pos, old = original_block(source, e)
            raw = b'\x70' + encode(e['fr'], profile == 'accents') + b'\x13\x02'
            raw = raw.ljust(len(old), b'\x00')
            records.append((pos, raw))
            target[pos:pos+len(old)] = raw
        # Conserver tous les enregistrements de V11, y compris leurs métadonnées
        # de découpage, puis ajouter les 18 nouveaux blocs sans collision.
        addition = bytearray()
        for pos, raw in sorted(records):
            addition.extend(pos.to_bytes(3, 'big'))
            addition.extend(len(raw).to_bytes(2, 'big'))
            addition.extend(raw)
        final_ips = previous_ips[:-3] + bytes(addition) + b'EOF'
        if apply_ips(source, final_ips) != bytes(target):
            raise AssertionError('IPS fusionné différent de la ROM attendue : ' + profile)
        if parse_ips(final_ips)[:len(parse_ips(previous_ips))] != parse_ips(previous_ips):
            raise AssertionError('Régression V11')
        results[profile] = (final_ips, {
            'bytes': len(final_ips),
            'sha256': hashlib.sha256(final_ips).hexdigest(),
            'rom_resultante_sha256': hashlib.sha256(target).hexdigest(),
            'enregistrements_ips': len(parse_ips(final_ips))})
    return results, {
        'source': 'ROM USA 1.2',
        'version': 'v12',
        'base': 'v11 autonome',
        'nouveaux_dialogues': len(entries),
        'pointeurs_vers_debuts': sum(pointers.values()),
        'limitations': 'Tests binaires uniquement ; test sous émulateur à réaliser.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom_originale', type=Path)
    parser.add_argument('--sortie', type=Path, default=Path('build_v12'))
    args = parser.parse_args()
    data = args.rom_originale.read_bytes()
    if len(data) % 0x8000 == 512:
        data = data[512:]
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    previous = {
        profile: (ROOT / f'patches/EarthBound_Beginnings_FR_v11_{profile}.ips').read_bytes()
        for profile in ('accents', 'ascii')}
    results, report = build(data, previous, manifest)
    args.sortie.mkdir(parents=True, exist_ok=True)
    for profile, (ips, info) in results.items():
        name = f'EarthBound_Beginnings_FR_v12_{profile}.ips'
        (args.sortie / name).write_bytes(ips)
        report[profile] = {'file': name, **info}
    (args.sortie / 'rapport_v12.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
