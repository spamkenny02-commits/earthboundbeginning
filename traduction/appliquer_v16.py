#!/usr/bin/env python3
"""Applique le patch V16 autonome sur une copie de la ROM originale USA 1.2."""
import argparse
import hashlib
from pathlib import Path
from construire_v11 import ROM_SHA, apply_ips


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom_originale", type=Path)
    p.add_argument("--profil", choices=("accents", "ascii"), default="accents")
    p.add_argument("--sortie", type=Path, required=True)
    args = p.parse_args()
    if args.rom_originale.resolve() == args.sortie.resolve() or args.sortie.exists():
        p.error("Refus d'écraser la ROM source ou un fichier existant.")
    data = args.rom_originale.read_bytes()
    header = data[:512] if len(data) % 0x8000 == 512 else b""
    source = data[len(header):]
    if hashlib.sha256(source).hexdigest() != ROM_SHA:
        p.error("ROM incorrecte : version USA 1.2 originale requise.")
    patch = (Path(__file__).resolve().parents[1] / "patches" /
             f"EarthBound_Beginnings_FR_v16_{args.profil}.ips").read_bytes()
    target = apply_ips(source, patch)
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_bytes(header + target)
    print("ROM V16 créée localement :", args.sortie)
    print("SHA-256 ROM modifiée :", hashlib.sha256(target).hexdigest())


if __name__ == "__main__":
    main()
