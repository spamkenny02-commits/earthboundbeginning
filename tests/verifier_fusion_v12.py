#!/usr/bin/env python3
"""Régression V12 sans ROM : préserve V11 et contrôle les 18 nouveaux blocs."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from construire_v11 import parse_ips, encode

MANIFEST = ROOT / 'traduction/v12_nouveaux_dialogues.json'
PATCHES = ROOT / 'patches'


def verify():
    entries = json.loads(MANIFEST.read_text(encoding='utf-8'))['entries']
    assert len(entries) == 18 and len({e['id'] for e in entries}) == 18
    for profile in ('accents', 'ascii'):
        previous = (PATCHES / f'EarthBound_Beginnings_FR_v11_{profile}.ips').read_bytes()
        merged = (PATCHES / f'EarthBound_Beginnings_FR_v12_{profile}.ips').read_bytes()
        assert merged[:len(previous)-3] == previous[:-3], 'Octets V11 modifiés'
        old_records = parse_ips(previous)
        records = parse_ips(merged)
        assert records[:len(old_records)] == old_records
        assert len(records) == len(old_records) + len(entries)
        occupied = set()
        for pos, raw in old_records:
            for i in range(len(raw)):
                occupied.add(pos+i)
        expected = {int(e['id'], 16): e for e in entries}
        for pos, raw in records[len(old_records):]:
            assert pos in expected, f'Bloc non prévu : {pos:06X}'
            entry = expected.pop(pos)
            original_size = len(encode(entry['english'][:-8])) + 2
            replacement = b'\x70' + encode(entry['fr'], profile == 'accents') + b'\x13\x02'
            assert len(replacement) <= original_size
            assert raw == replacement.ljust(original_size, b'\x00')
            for p in range(pos, pos+len(raw)):
                assert p not in occupied, f'Collision IPS {p:06X}'
                occupied.add(p)
        assert not expected, f'Dialogues manquants : {expected}'
        print(f'OK {profile}: {len(old_records)} blocs V11 + 18 = {len(records)} blocs V12')
    print('V12 : conservation V11, cohérence des blocs et absence de collision vérifiées.')


if __name__ == '__main__':
    verify()
