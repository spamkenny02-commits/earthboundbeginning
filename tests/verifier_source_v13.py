#!/usr/bin/env python3
"""Test V13 complet avec ROM USA 1.2 personnelle (non fournie dans le dépôt).

Exemple :
 python tests/verifier_source_v13.py "EarthBound Beginnings (USA) 1.2.sfc"

Vérifie la source, chaque script, les pointeurs, les codes, les deux profils
et la reproduction exacte des IPS publiés. Aucun émulateur n'est lancé.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from construire_v13 import MANIFEST, build


def verify(rom):
    data = rom.read_bytes()
    if len(data) % 0x8000 == 512:
        data = data[512:]
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    previous = {p: (ROOT / f'patches/EarthBound_Beginnings_FR_v12_{p}.ips').read_bytes()
                for p in ('accents', 'ascii')}
    results, report = build(data, previous, manifest)
    for profile, (generated, info) in results.items():
        path = ROOT / f'patches/EarthBound_Beginnings_FR_v13_{profile}.ips'
        published = path.read_bytes()
        if generated != published:
            raise AssertionError('IPS publié différent du résultat reproductible : ' + profile)
        print(f"OK {profile}: {len(published)} octets, SHA256 {hashlib.sha256(published).hexdigest()}")
    print('OK source :', report['nouveaux_blocs'], 'blocs et',
          report['pointeurs_source_verifies'], 'références HiROM explicites')
    print('Test binaire réussi ; tests de rendu et de progression en émulateur distincts.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('rom_originale', type=Path)
    args = p.parse_args()
    verify(args.rom_originale)
