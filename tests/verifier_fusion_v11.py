#!/usr/bin/env python3
"""Vérifie la fusion IPS v11 sans exiger de ROM commerciale."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from construire_v11 import parse_ips, encode

PATCH = ROOT / 'patches'
MANIFEST = ROOT / 'traduction/v11_nouveaux_dialogues.json'


def verify():
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    entries = manifest['entries']
    assert len(entries) == 27 and len({e['id'] for e in entries}) == 27
    for profile in ('accents', 'ascii'):
        original = (PATCH / f'EarthBound_Beginnings_FR_v09_{profile}.ips').read_bytes()
        addon = (PATCH / f'EarthBound_Beginnings_FR_v10_addon_{profile}.ips').read_bytes()
        final = (PATCH / f'EarthBound_Beginnings_FR_v11_{profile}.ips').read_bytes()
        r09, r10, r11 = map(parse_ips, (original, addon, final))
        assert len(r11) == len(r09) + len(r10) + 27
        assert r11[:len(r09)] == r09, 'Régression v09'
        assert r11[len(r09):len(r09)+len(r10)] == r10, 'Régression v10'
        changed = set()
        for pos, raw in r09 + r10:
            for p in range(pos, pos+len(raw)):
                changed.add(p)
        new = {int(e['id'], 16): e for e in entries}
        assert len(r11[-27:]) == len(new)
        for pos, raw in r11[-27:]:
            assert pos in new
            e = new.pop(pos)
            expected = b'\x70' + encode(e['fr'], profile == 'accents') + b'\x13\x02'
            old_size = len(encode(e['english'][:-8])) + 2
            assert len(raw) == old_size
            assert raw == expected.ljust(old_size, b'\x00')
            assert all(p not in changed for p in range(pos, pos+len(raw)))
        assert not new
        print(f'OK {profile}: {len(r09)} v09 + {len(r10)} v10 + 27 v11 = {len(r11)} enregistrements')
    print('Fusion IPS vérifiée ; test de jeu sur émulateur restant à faire.')


if __name__ == '__main__':
    verify()
