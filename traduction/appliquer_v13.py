#!/usr/bin/env python3
"""Applique UN patch V13 complet à une copie de la ROM USA 1.2."""
import argparse
import hashlib
from pathlib import Path

from construire_v11 import ROM_SHA, apply_ips


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('rom_originale', type=Path)
    p.add_argument('--profil', choices=('accents', 'ascii'), default='accents')
    p.add_argument('--sortie', type=Path, required=True)
    args = p.parse_args()
    if args.rom_originale.resolve() == args.sortie.resolve():
        p.error('Refus d’écraser la ROM originale.')
    if args.sortie.exists():
        p.error('Le fichier de sortie existe déjà.')
    data = args.rom_originale.read_bytes()
    header = data[:512] if len(data) % 0x8000 == 512 else b''
    source = data[len(header):]
    if hashlib.sha256(source).hexdigest() != ROM_SHA:
        p.error('ROM incorrecte : USA 1.2 originale requise.')
    patch = (Path(__file__).resolve().parents[1] / 'patches' /
             f'EarthBound_Beginnings_FR_v13_{args.profil}.ips').read_bytes()
    result = apply_ips(source, patch)
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_bytes(header + result)
    print('ROM française V13 créée localement :', args.sortie)
    print('SHA-256 :', hashlib.sha256(result).hexdigest())


if __name__ == '__main__':
    main()
