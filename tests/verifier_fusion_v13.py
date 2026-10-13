#!/usr/bin/env python3
"""V13 : tests de non-régression sans ROM originale, utilisables en CI."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from construire_v11 import encode, parse_ips
from construire_v13 import PREFIX, controls

PATCHES = ROOT / 'patches'
MANIFEST = ROOT / 'traduction/v13_dialogues_fr.json'


def test():
    entries = json.loads(MANIFEST.read_text(encoding='utf-8'))['entries']
    assert len(entries) == 141, 'Lot V13 incomplet'
    assert len({e['id'] for e in entries}) == len(entries), 'IDs dupliqués'
    expected = {}
    for e in entries:
        match = PREFIX.fullmatch(e['english'])
        assert match and match.group(2) == e['english_text'], e['id']
        assert e['pointer_refs'], e['id']
        prefix, english, suffix = match.groups()
        assert controls(prefix) is not None and controls(suffix) is not None
        offset = int(e['id'], 16) + len(controls(prefix)) + 1
        assert offset not in expected, e['id']
        expected[offset] = e
        for accented in (True, False):
            assert len(encode(e['fr'], accented)) <= len(english), e['id']
    for profile in ('accents', 'ascii'):
        previous = (PATCHES / f'EarthBound_Beginnings_FR_v12_{profile}.ips').read_bytes()
        current = (PATCHES / f'EarthBound_Beginnings_FR_v13_{profile}.ips').read_bytes()
        assert current[:len(previous) - 3] == previous[:-3], 'Régression binaire V12'
        old = parse_ips(previous)
        new = parse_ips(current)
        assert len(new) == len(old) + len(entries)
        assert new[:len(old)] == old
        occupied = set()
        for p, raw in old:
            occupied.update(range(p, p+len(raw)))
        remaining = dict(expected)
        for p, raw in new[len(old):]:
            assert p in remaining, f'Patch hors manifeste : {p:06X}'
            entry = remaining.pop(p)
            fr = encode(entry['fr'], profile == 'accents')
            assert raw == fr.ljust(len(entry['english_text']), b'\x50'), entry['id']
            assert not any(x in occupied for x in range(p, p+len(raw))), entry['id']
            occupied.update(range(p, p+len(raw)))
        assert not remaining, f'Blocs absents : {remaining}'
        print(f'OK {profile}: {len(old)} enregistrements V12 conservés + {len(entries)} V13 = {len(new)}')
    print('V13 : 141 blocs, commandes inchangées, tailles, collisions et conservation V12 validés.')


if __name__ == '__main__':
    test()
