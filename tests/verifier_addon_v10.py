#!/usr/bin/env python3
"""Tests du patch v10 additionnel sur ROM USA 1.2 ; aucune ROM distribuée."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from construire_addon_v10 import MANIFEST, encode, source_block, run


def apply_ips(source, patch):
    assert patch.startswith(b'PATCH') and patch.endswith(b'EOF')
    data = bytearray(source)
    i = 5
    while patch[i:i+3] != b'EOF':
        pos = int.from_bytes(patch[i:i+3], 'big')
        size = int.from_bytes(patch[i+3:i+5], 'big')
        i += 5
        assert 0 < size <= 65535 and pos+size <= len(data)
        data[pos:pos+size] = patch[i:i+size]
        i += size
    assert i == len(patch)-3
    return bytes(data)


def verify(source, directory):
    report = run(source, source, directory)
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert report['translated_blocks'] == 50
    assert report['source_literal_pointers'] == 70
    for profile, accents in [('accents', True), ('ascii', False)]:
        patch = (directory / report['patches'][profile]['file']).read_bytes()
        assert hashlib.sha256(patch).hexdigest() == report['patches'][profile]['sha256']
        result = apply_ips(source, patch)
        covered = bytearray(len(source))
        for entry in manifest['entries']:
            pos = int(entry['id'], 16)
            old = source_block(source, pos)
            translated = b'\x70' + encode(entry['fr'], accents) + b'\x13\x02'
            assert result[pos:pos+len(old)] == translated.ljust(len(old), b'\x00')
            covered[pos:pos+len(old)] = b'\x01'*len(old)
        assert all(a == b for a,b,used in zip(source,result,covered) if not used)
    print('OK : 50 dialogues, 70 pointeurs, 2 IPS, aucun octet extérieur modifié')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--out', type=Path, default=Path('build_v10'))
    args = parser.parse_args()
    verify(args.source.read_bytes(), args.out)
