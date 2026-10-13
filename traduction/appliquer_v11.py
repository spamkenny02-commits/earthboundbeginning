#!/usr/bin/env python3
"""Applique UN patch V11 autonome sur une copie de la ROM USA 1.2.

Ne distribue pas de ROM ; vérifie l'empreinte source et refuse l'écrasement.
"""
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
        parser.error('La sortie ne doit pas écraser la ROM originale.')
    if args.sortie.exists():
        parser.error('Le fichier de sortie existe déjà : refus d’écraser.')
    source = args.rom_originale.read_bytes()
    header = source[:512] if len(source) % 0x8000 == 512 else b''
    body = source[len(header):]
    if hashlib.sha256(body).hexdigest() != ROM_SHA:
        parser.error('ROM incorrecte : il faut la version USA 1.2 non modifiée.')
    patch = (Path(__file__).resolve().parents[1] / 'patches' /
             f'EarthBound_Beginnings_FR_v11_{args.profil}.ips').read_bytes()
    target = apply_ips(body, patch)
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_bytes(header + target)
    print('ROM locale créée :', args.sortie)
    print('SHA-256 de la ROM modifiée :', hashlib.sha256(target).hexdigest())


if __name__ == '__main__':
    main()
