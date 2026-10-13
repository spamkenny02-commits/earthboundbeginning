#!/usr/bin/env python3
"""V13 autonome : V12 + 141 blocs français, sans toucher aux commandes.

Usage :
 python traduction/construire_v13.py "EarthBound Beginnings (USA) 1.2.sfc"
La ROM est vérifiée par SHA-256. Les patchs produits n'incluent pas la ROM.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from construire_v11 import ROM_SHA, encode, parse_ips, apply_ips

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'traduction/v13_dialogues_fr.json'
PREFIX = re.compile(r'^((?:\[[0-9A-F ]+\])*)@([^@\[\]\n]+)((?:\[[0-9A-F ]+\])*)$')
TOKEN = re.compile(r'\[([0-9A-F ]+)\]')


def controls(text):
    tokens = TOKEN.findall(text)
    if ''.join('[' + t + ']' for t in tokens) != text:
        raise ValueError('Commandes ou caractères inattendus : ' + text)
    return b''.join(bytes.fromhex(t) for t in tokens)


def ascii_game(text):
    return bytes(ord(c) + 0x30 for c in text)


def verify_original(source, entry):
    m = PREFIX.fullmatch(entry['english'])
    if not m or m.group(2) != entry['english_text']:
        raise ValueError('Texte anglais non conforme : ' + entry['id'])
    prefix, english, suffix = m.groups()
    pos = int(entry['id'], 16)
    raw = controls(prefix) + b'\x70' + ascii_game(english) + controls(suffix)
    if source[pos:pos + len(raw)] != raw:
        raise ValueError('ROM source différente : ' + entry['id'])
    return pos + len(controls(prefix)) + 1, ascii_game(english)


def build(source, old_patches, manifest):
    if hashlib.sha256(source).hexdigest() != ROM_SHA:
        raise ValueError('SHA-256 ROM USA 1.2 incorrect')
    entries = manifest['entries']
    if len(entries) != len({x['id'] for x in entries}):
        raise ValueError('Identifiants dupliqués')
    original_spans = {}
    for e in entries:
        p, old = verify_original(source, e)
        if not e['pointer_refs']:
            raise ValueError('Dialogue sans référence explicite : ' + e['id'])
        ptr = (0xC00000 + int(e['id'], 16)).to_bytes(4, 'little')
        for address in e['pointer_refs']:
            at = int(address, 16)
            if source[at:at + 4] != ptr:
                raise ValueError('Référence HiROM invalide : ' + e['id'])
        for accents in (True, False):
            if len(encode(e['fr'], accents)) > len(old):
                raise ValueError('Traduction trop longue : ' + e['id'])
        original_spans[e['id']] = (p, old)
    spans = sorted((p, p + len(old), key) for key, (p, old) in original_spans.items())
    if any(left[1] > right[0] for left, right in zip(spans, spans[1:])):
        raise ValueError('Chevauchement entre traductions V13')
    result = {}
    for profile in ('accents', 'ascii'):
        previous = old_patches[profile]
        previous_rom = apply_ips(source, previous)
        for p, end, key in spans:
            if previous_rom[p:end] != source[p:end]:
                raise ValueError('Collision avec V12 : ' + key)
        target = bytearray(previous_rom)
        extra = bytearray()
        for p, end, key in spans:
            e = next(x for x in entries if x['id'] == key)
            fr = encode(e['fr'], profile == 'accents').ljust(end - p, b'\x50')
            target[p:end] = fr
            extra.extend(p.to_bytes(3, 'big'))
            extra.extend(len(fr).to_bytes(2, 'big'))
            extra.extend(fr)
        merged = previous[:-3] + bytes(extra) + b'EOF'
        if apply_ips(source, merged) != bytes(target):
            raise AssertionError('Aller-retour IPS V13 invalide')
        if parse_ips(merged)[:len(parse_ips(previous))] != parse_ips(previous):
            raise AssertionError('Régression V12')
        result[profile] = (merged, {
            'patch_sha256': hashlib.sha256(merged).hexdigest(),
            'rom_modifiee_sha256': hashlib.sha256(target).hexdigest(),
            'enregistrements_ips': len(parse_ips(merged)),
            'taille_ips': len(merged)})
    return result, {'version': 'v13', 'nouveaux_blocs': len(entries),
                    'pointeurs_source_verifies': sum(len(e['pointer_refs']) for e in entries),
                    'tests': 'ROM source, commandes, pointeurs, longueurs, collisions, IPS',
                    'emulation': 'non effectuee'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('rom_originale', type=Path)
    p.add_argument('--sortie', type=Path, default=Path('build_v13'))
    args = p.parse_args()
    source = args.rom_originale.read_bytes()
    if len(source) % 0x8000 == 512:
        source = source[512:]
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    previous = {profile: (ROOT / f'patches/EarthBound_Beginnings_FR_v12_{profile}.ips').read_bytes()
                for profile in ('accents', 'ascii')}
    results, report = build(source, previous, manifest)
    args.sortie.mkdir(parents=True, exist_ok=True)
    for profile, (patch, info) in results.items():
        filename = f'EarthBound_Beginnings_FR_v13_{profile}.ips'
        (args.sortie / filename).write_bytes(patch)
        report[profile] = {'file': filename, **info}
    (args.sortie / 'rapport_v13.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
