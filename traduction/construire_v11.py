#!/usr/bin/env python3
"""Fusion reproductible v09 + add-on v10 + nouveaux dialogues v11.

Entrée : ROM USA 1.2 originale (non redistribuée).
Sortie : DEUX patchs IPS complets v11 à appliquer DIRECTEMENT à l'originale.
La v09 et l'add-on v10 ne sont PAS requis lors de l'application du patch v11.
"""
import argparse
import hashlib
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROM_SHA = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
ACCENTS = 'éèêëàâîïôùûüçÉÀÇ'
MANIFEST = ROOT / 'traduction/v11_nouveaux_dialogues.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(s, accents=True):
    s = s.replace('’', "'").replace('Œ', 'Oe').replace('œ', 'oe').replace('–', '-').replace('…', '...')
    if not accents:
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    result = bytearray()
    for c in s:
        if accents and c in ACCENTS:
            result.append(0xB0 + ACCENTS.index(c))
        elif 32 <= ord(c) <= 122 and c not in '"[\\]^':
            result.append(ord(c) + 48)
        else:
            raise ValueError('Glyphe non défini : ' + repr(c))
    return bytes(result)


def parse_ips(patch):
    if not patch.startswith(b'PATCH'):
        raise ValueError('IPS sans en-tête PATCH')
    i, records = 5, []
    while i < len(patch):
        if patch[i:i+3] == b'EOF':
            if i + 3 != len(patch):
                raise ValueError('IPS avec octets supplémentaires')
            return records
        if i + 5 > len(patch):
            raise ValueError('IPS tronqué')
        pos = int.from_bytes(patch[i:i+3], 'big')
        length = int.from_bytes(patch[i+3:i+5], 'big')
        i += 5
        if length:
            raw = patch[i:i+length]
            i += length
            if len(raw) != length:
                raise ValueError('Données IPS tronquées')
        else:
            if i+3 > len(patch):
                raise ValueError('RLE IPS tronqué')
            count = int.from_bytes(patch[i:i+2], 'big')
            raw = bytes([patch[i+2]]) * count
            i += 3
        records.append((pos, raw))
    raise ValueError('IPS sans marqueur EOF')


def apply_ips(source, patch):
    data = bytearray(source)
    for pos, raw in parse_ips(patch):
        if pos + len(raw) > len(data):
            raise ValueError('IPS hors ROM')
        data[pos:pos+len(raw)] = raw
    return bytes(data)


def diff_ips(original, target):
    if len(original) != len(target):
        raise ValueError('Taille de ROM différente')
    out = bytearray(b'PATCH')
    i = 0
    while i < len(original):
        if original[i] == target[i]:
            i += 1
            continue
        pos = i
        while i < len(original) and original[i] != target[i] and i-pos < 65535:
            i += 1
        if pos == 0x454F46:
            raise ValueError('Offset IPS réservé EOF')
        out.extend(pos.to_bytes(3, 'big'))
        out.extend((i-pos).to_bytes(2, 'big'))
        out.extend(target[pos:i])
    return bytes(out + b'EOF')


def original_block(source, entry):
    pos = int(entry['id'], 16)
    original = entry['english']
    if not original.startswith('@') or not original.endswith('[13][02]'):
        raise ValueError('Bloc non simple : ' + entry['id'])
    expected = encode(original[:-8]) + b'\x13\x02'
    actual = source[pos:pos+len(expected)]
    if actual != expected:
        raise ValueError('Texte source différent : ' + entry['id'])
    return pos, expected


def check_pointers(source, spans):
    starts = {start: name for name, start, end in spans}
    interior = {i: name for name, start, end in spans for i in range(start+1, end)}
    refs = {name: 0 for name, start, end in spans}
    for pos in range(len(source)-3):
        pointer = int.from_bytes(source[pos:pos+4], 'little')
        if 0xC00000 <= pointer <= 0xFFFFFF:
            target = pointer - 0xC00000
            if target in interior:
                raise ValueError('Pointeur littéral intérieur : ' + interior[target])
            if target in starts:
                refs[starts[target]] += 1
    if not all(refs.values()):
        raise ValueError('Dialogue sans pointeur littéral')
    return refs


def build(source, v09, v10, manifest):
    if sha(source) != ROM_SHA:
        raise ValueError('ROM source incorrecte : SHA-256')
    entries = manifest['entries']
    if len(entries) != len({x['id'] for x in entries}):
        raise ValueError('IDs dupliqués')
    spans = []
    for e in entries:
        pos, original = original_block(source, e)
        spans.append((e['id'], pos, pos+len(original)))
        for accents in (True, False):
            if len(encode(e['fr'], accents)) + 3 > len(original):
                raise ValueError('Traduction trop longue : ' + e['id'])
    refs = check_pointers(source, spans)
    result = {}
    for accents, profile in [(True, 'accents'), (False, 'ascii')]:
        a = v09[profile]
        b = v10[profile]
        after09 = apply_ips(source, a)
        after10 = apply_ips(after09, b)
        for name, pos, end in spans:
            if after10[pos:end] != source[pos:end]:
                raise ValueError('Collision v09/v10 avec v11 : ' + name)
        target = bytearray(after10)
        for e in entries:
            pos, old = original_block(source, e)
            replacement = b'\x70' + encode(e['fr'], accents) + b'\x13\x02'
            target[pos:pos+len(old)] = replacement.ljust(len(old), b'\x00')
        target = bytes(target)
        new_records = []
        for e in entries:
            pos, old = original_block(source, e)
            replacement = b'\x70' + encode(e['fr'], accents) + b'\x13\x02'
            new_records.append((pos, replacement.ljust(len(old), b'\x00')))
        new_ips = bytearray(b'PATCH')
        for pos, raw in sorted(new_records):
            new_ips.extend(pos.to_bytes(3, 'big'))
            new_ips.extend(len(raw).to_bytes(2, 'big'))
            new_ips.extend(raw)
        new_ips.extend(b'EOF')
        merged = b'PATCH' + a[5:-3] + b[5:-3] + bytes(new_ips)[5:-3] + b'EOF'
        if apply_ips(source, merged) != target:
            raise AssertionError('Échec vérification aller-retour IPS ' + profile)
        result[profile] = (merged, {
            'sha256': sha(merged),
            'bytes': len(merged),
            'sha256_rom_resultante': sha(target),
            'nb_enregistrements_ips': len(parse_ips(merged)),
            'v09_sha256': sha(a),
            'v10_sha256': sha(b)})
    return result, {'nouveaux_dialogues_v11': len(entries),
                    'pointeurs_vers_debuts': sum(refs.values()),
                    'nouveaux_blocs': [e['id'] for e in entries],
                    'note': 'Validation binaire hors émulateur, pas encore un test de parcours.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom_source', type=Path)
    parser.add_argument('--out', type=Path, default=Path('build_v11'))
    args = parser.parse_args()
    source = args.rom_source.read_bytes()
    if len(source) % 0x8000 == 512:
        source = source[512:]
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    v09 = {p: (ROOT / ('patches/EarthBound_Beginnings_FR_v09_' + p + '.ips')).read_bytes()
           for p in ('accents', 'ascii')}
    v10 = {p: (ROOT / ('patches/EarthBound_Beginnings_FR_v10_addon_' + p + '.ips')).read_bytes()
           for p in ('accents', 'ascii')}
    results, report = build(source, v09, v10, manifest)
    args.out.mkdir(parents=True, exist_ok=True)
    for profile, (patch, info) in results.items():
        filename = 'EarthBound_Beginnings_FR_v11_' + profile + '.ips'
        (args.out / filename).write_bytes(patch)
        report[profile] = {'filename': filename, **info}
    (args.out / 'rapport_v11.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
