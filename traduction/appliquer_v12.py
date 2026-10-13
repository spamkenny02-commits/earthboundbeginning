#!/usr/bin/env python3
"""Applique le patch autonome V12 à une COPIE de la ROM USA 1.2."""
import argparse
import hashlib
from pathlib import Path

from construire_v11 import ROM_SHA, apply_ips


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom_originale', type=Path)
    parser.add_argument('--profil', choices=('accents', 'ascii'), default='accents')
    parser.add_argument('--sortie', type=Path, required=True)
    args = parser.parse_args()
    if args.rom_originale.resolve() == args.sortie.resolve():
        parser.error('Refus : ne pas écraser la ROM originale.')
    if args.sortie.exists():
        parser.error('Refus : le fichier de sortie existe déjà.')
    raw = args.rom_originale.read_bytes()
    header = raw[:512] if len(raw) % 0x8000 == 512 else b''
    source = raw[len(header):]
    if hashlib.sha256(source).hexdigest() != ROM_SHA:
        parser.error('ROM source incorrecte : USA 1.2 originale requise.')
    patch = (Path(__file__).resolve().parents[1] / 'patches' /
             f'EarthBound_Beginnings_FR_v12_{args.profil}.ips').read_bytes()
    target = apply_ips(source, patch)
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_bytes(header + target)
    print('ROM V12 créée localement :', args.sortie)
    print('SHA-256 (sans en-tête) :', hashlib.sha256(target).hexdigest())


if __name__ == '__main__':
    main()
