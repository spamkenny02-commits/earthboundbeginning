#!/usr/bin/env python3
"""Génère deux IPS additionnels à appliquer APRÈS les patchs v09.

Aucune ROM n'est publiée. Vérifie les blocs, pointeurs HiROM et tailles
sur la ROM originale ; refuse une ROM v09 dont les blocs ciblés diffèrent.
Sans --base-v09, génère des IPS structurels sur la source uniquement.
"""
import argparse
import hashlib
import json
import unicodedata
from pathlib import Path

ACCENTS = 'éèêëàâîïôùûüçÉÀÇ'
CODES = {c: 0xB0 + i for i, c in enumerate(ACCENTS)}
MANIFEST = Path(__file__).with_name('v10_inplace_fr.json')


def encode(text, accents):
    text = text.replace('’', "'").replace('œ', 'oe').replace('Œ', 'Oe')
    if not accents:
        text = ''.join(c for c in unicodedata.normalize('NFD', text)
                       if not unicodedata.combining(c))
    out = bytearray()
    for char in text:
        if accents and char in CODES:
            out.append(CODES[char])
        elif 32 <= ord(char) <= 122 and char not in '"[\\]^':
            out.append(ord(char) + 48)
        else:
            raise ValueError('Glyphe non encodable : ' + repr(char))
    return bytes(out)


def source_block(source, pos):
    assert source[pos] == 0x70, f'{pos:06X} : début non reconnu'
    end = pos + 1
    while end < pos + 512 and 0x50 <= source[end] <= 0xAA:
        end += 1
    assert source[end:end + 2] == b'\x13\x02', f'{pos:06X} : commandes inattendues'
    return source[pos:end + 2]


def make_ips(records):
    out = bytearray(b'PATCH')
    for pos, raw in sorted(records):
        assert len(raw) <= 65535
        out.extend(pos.to_bytes(3, 'big'))
        out.extend(len(raw).to_bytes(2, 'big'))
        out.extend(raw)
    return bytes(out + b'EOF')


def run(original, base, output):
    config = json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert hashlib.sha256(original).hexdigest() == config['source_sha256'], 'Mauvaise ROM source'
    assert len(original) == len(base), 'Taille ROM différente'
    blocks = {}
    interior = {}
    start_to_id = {}
    for entry in config['entries']:
        key, french = entry['id'], entry['fr']
        assert key not in blocks, 'ID dupliqué'
        pos = int(key, 16)
        old = source_block(original, pos)
        assert base[pos:pos + len(old)] == old, f'Bloc v09 différent : {key}'
        for accented in (True, False):
            assert len(encode(french, accented)) + 3 <= len(old), f'Trop long : {key}'
        blocks[key] = (pos, old, french)
        start_to_id[pos] = key
        for address in range(pos + 1, pos + len(old)):
            assert address not in interior, 'Blocs chevauchants'
            interior[address] = key
    incoming = {key: 0 for key in blocks}
    for ref in range(len(original) - 3):
        value = int.from_bytes(original[ref:ref + 4], 'little')
        if 0xC00000 <= value <= 0xFFFFFF:
            target = value - 0xC00000
            assert target not in interior, f'Pointeur intérieur vers {interior.get(target)}'
            if target in start_to_id:
                incoming[start_to_id[target]] += 1
    assert all(incoming.values()), 'Bloc sans référence littérale'
    output.mkdir(parents=True, exist_ok=True)
    patches = {}
    for accented, profile in ((True, 'accents'), (False, 'ascii')):
        records = []
        for key, (pos, old, french) in blocks.items():
            raw = b'\x70' + encode(french, accented) + b'\x13\x02'
            records.append((pos, raw.ljust(len(old), b'\x00')))
        patch = make_ips(records)
        name = f'EarthBound_Beginnings_FR_v10_addon_{profile}.ips'
        (output / name).write_bytes(patch)
        patches[profile] = {'file': name, 'sha256': hashlib.sha256(patch).hexdigest(),
                            'bytes': len(patch)}
    report = {'translated_blocks': len(blocks),
              'source_literal_pointers': sum(incoming.values()),
              'patches': patches,
              'note': 'Vérification structurelle sur ROM source. Pas de test émulateur v09/v10.'}
    (output / 'rapport_v10_addon.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom_source', type=Path)
    parser.add_argument('--base-v09', type=Path)
    parser.add_argument('--out', type=Path, default=Path('build_v10'))
    args = parser.parse_args()
    source = args.rom_source.read_bytes()
    base = args.base_v09.read_bytes() if args.base_v09 else source
    print(json.dumps(run(source, base, args.out), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
