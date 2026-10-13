#!/usr/bin/env python3
"""V15 : patch autonome V14 + 77 segments de 32 scripts narratifs.

Vérifie les scripts et pointeurs contre la ROM USA 1.2, la présence
d'éventuels pointeurs intérieurs, l'encodage, les longueurs et les
collisions avec la V14. Aucun fichier ROM n'est distribué.
"""
import argparse
import hashlib
import json
from pathlib import Path

from construire_v11 import ROM_SHA, apply_ips, encode, parse_ips
from construire_v14 import spans_for_entry

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "traduction/v15_dialogues_fr.json"


def build(source, previous, manifest):
    if hashlib.sha256(source).hexdigest() != ROM_SHA:
        raise ValueError("La ROM doit être la version USA 1.2 originale.")
    entries = manifest["entries"]
    if len(entries) != 32 or len({e["id"] for e in entries}) != 32:
        raise ValueError("Manifeste V15 incomplet ou dupliqué")
    spans = []
    for entry in entries:
        pos, raw, edits = spans_for_entry(entry)
        if source[pos:pos+len(raw)] != raw:
            raise ValueError("Source ROM incompatible : " + entry["id"])
        ptr = (0xC00000 + pos).to_bytes(4, "little")
        if not entry["pointer_refs"]:
            raise ValueError("Pointeur manquant : " + entry["id"])
        for ref in entry["pointer_refs"]:
            at = int(ref, 16)
            if source[at:at+4] != ptr:
                raise ValueError("Pointeur littéral erroné : " + entry["id"])
        spans.extend(edits)
    spans.sort()
    if len(spans) != 77:
        raise ValueError(f"77 segments attendus, {len(spans)} reçus")
    for a, b in zip(spans, spans[1:]):
        if a[0] + len(a[1]) > b[0]:
            raise ValueError("Chevauchement de segments V15")
    # Les adresses intérieures des chaînes traduites ne doivent jamais
    # être utilisées comme entrées de texte, même si le bloc principal
    # a une référence HiROM correcte.
    interiors = {p+i for p, english, _, _ in spans
                 for i in range(1, len(english))}
    for at in range(len(source)-3):
        if 0xC0 <= source[at+2] <= 0xFF and source[at+3] == 0:
            target = int.from_bytes(source[at:at+4], "little") - 0xC00000
            if target in interiors:
                raise ValueError(f"Pointeur intérieur dangereux {at:06X} -> {target:06X}")
    results = {}
    for profile in ("accents", "ascii"):
        prior = previous[profile]
        if not prior.startswith(b"PATCH") or not prior.endswith(b"EOF"):
            raise ValueError("Patch V14 invalide")
        old = apply_ips(source, prior)
        target = bytearray(old)
        added = bytearray()
        for pos, english, french, ident in spans:
            if old[pos:pos+len(english)] != english:
                raise ValueError("Collision avec V14 : " + ident)
            fr = encode(french, profile == "accents")
            if len(fr) > len(english):
                raise ValueError("Texte trop long : " + ident)
            raw = fr.ljust(len(english), b"\x50")
            target[pos:pos+len(raw)] = raw
            added.extend(pos.to_bytes(3, "big"))
            added.extend(len(raw).to_bytes(2, "big"))
            added.extend(raw)
        merged = prior[:-3] + bytes(added) + b"EOF"
        if apply_ips(source, merged) != bytes(target):
            raise AssertionError("Reconstruction IPS incorrecte")
        if parse_ips(merged)[:len(parse_ips(prior))] != parse_ips(prior):
            raise AssertionError("V14 altérée")
        results[profile] = (merged, hashlib.sha256(target).hexdigest())
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom_originale", type=Path)
    p.add_argument("--sortie", type=Path, default=Path("build_v15"))
    p.add_argument("--comparer-publication", action="store_true")
    args = p.parse_args()
    rom = args.rom_originale.read_bytes()
    if len(rom) % 0x8000 == 512:
        rom = rom[512:]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    old = {profile: (ROOT / f"patches/EarthBound_Beginnings_FR_v14_{profile}.ips").read_bytes()
           for profile in ("accents", "ascii")}
    results = build(rom, old, manifest)
    args.sortie.mkdir(parents=True, exist_ok=True)
    for profile, (ips, sha) in results.items():
        name = f"EarthBound_Beginnings_FR_v15_{profile}.ips"
        if args.comparer_publication:
            assert ips == (ROOT / "patches" / name).read_bytes(), name
        (args.sortie / name).write_bytes(ips)
        print(profile, len(ips), "octets; SHA-256 ROM cible :", sha)
    print("V15 : 32 scripts, 77 segments, pointeurs et IPS contrôlés.")


if __name__ == "__main__":
    main()
