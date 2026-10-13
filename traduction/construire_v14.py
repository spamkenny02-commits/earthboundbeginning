#!/usr/bin/env python3
"""Construit les patchs autonomes V14 depuis V13 et la ROM USA 1.2.

Les 44 scripts multisegments sont contrôlés octet par octet, y compris les
sauts de ligne 00 ou 03 00. Les 138 segments sont remplacés en place,
sans déplacer les commandes ni les marqueurs de dialogue.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from construire_v11 import ROM_SHA, encode, apply_ips, parse_ips

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "traduction/v14_multisegments_fr.json"
SPLIT = re.compile(r"(\[[0-9A-F ]+\]|\n|@)")


def spans_for_entry(entry):
    pos = int(entry["id"], 16)
    original = bytearray()
    spans = []
    ix = 0
    newline_ix = 0
    for part in filter(None, SPLIT.split(entry["english"])):
        if re.fullmatch(r"\[[0-9A-F ]+\]", part):
            data = bytes.fromhex(part[1:-1])
        elif part == "\n":
            short = (entry["newline_one_byte_mask"] >> newline_ix) & 1
            data = b"\x00" if short else b"\x03\x00"
            newline_ix += 1
        elif part == "@":
            data = b"\x70"
        else:
            data = bytes(ord(c) + 48 for c in part)
            if any(not 0x50 <= b <= 0xAA for b in data):
                raise ValueError("Caractère source non pris en charge : " + entry["id"])
            if re.search("[A-Za-z]", part):
                if ix >= len(entry["translations"]):
                    raise ValueError("Traduction manquante : " + entry["id"])
                french = entry["translations"][ix]
                ix += 1
                if french != part:
                    spans.append((pos, data, french, entry["id"]))
        original.extend(data)
        pos += len(data)
    if ix != len(entry["translations"]):
        raise ValueError("Nombre de segments incorrect : " + entry["id"])
    return int(entry["id"], 16), bytes(original), spans


def build(source, previous, manifest):
    if hashlib.sha256(source).hexdigest() != ROM_SHA:
        raise ValueError("ROM originale USA 1.2 requise")
    if len(manifest["entries"]) != 44:
        raise ValueError("Nombre de scripts V14 inattendu")
    if len({e["id"] for e in manifest["entries"]}) != 44:
        raise ValueError("Scripts V14 dupliqués")
    spans = []
    for entry in manifest["entries"]:
        start, original, edits = spans_for_entry(entry)
        if source[start:start + len(original)] != original:
            raise ValueError("Script original différent : " + entry["id"])
        if not entry["pointer_refs"]:
            raise ValueError("Script sans pointeur littéral : " + entry["id"])
        pointer = (0xC00000 + start).to_bytes(4, "little")
        for ref in entry["pointer_refs"]:
            p = int(ref, 16)
            if source[p:p+4] != pointer:
                raise ValueError("Pointeur de script incorrect : " + entry["id"])
        spans.extend(edits)
    if len(spans) != 130:
        raise ValueError("Nombre de segments traduits incorrect")
    spans.sort()
    for left, right in zip(spans, spans[1:]):
        if left[0] + len(left[1]) > right[0]:
            raise ValueError("Chevauchement interne : " + left[3])
    # Éviter de changer le sens d'un saut vers le milieu d'une phrase.
    interiors = {p + j for p, raw, _, _ in spans for j in range(1, len(raw))}
    for at in range(len(source) - 3):
        if 0xC0 <= source[at + 2] <= 0xFF and source[at + 3] == 0:
            target = int.from_bytes(source[at:at + 4], "little") - 0xC00000
            if target in interiors:
                raise ValueError(f"Pointeur littéral au milieu d'une traduction : {target:06X}")
    results = {}
    for profile in ("accents", "ascii"):
        prior = previous[profile]
        old = apply_ips(source, prior)
        target = bytearray(old)
        extra = bytearray()
        for pos, english, french, ident in spans:
            if old[pos:pos + len(english)] != english:
                raise ValueError("Collision avec V13 : " + ident)
            translated = encode(french, profile == "accents")
            if len(translated) > len(english):
                raise ValueError("Texte français trop long : " + ident)
            raw = translated.ljust(len(english), b"\x50")
            target[pos:pos+len(raw)] = raw
            extra.extend(pos.to_bytes(3, "big"))
            extra.extend(len(raw).to_bytes(2, "big"))
            extra.extend(raw)
        merged = prior[:-3] + bytes(extra) + b"EOF"
        if apply_ips(source, merged) != bytes(target):
            raise AssertionError("IPS V14 non reproductible")
        if parse_ips(merged)[:len(parse_ips(prior))] != parse_ips(prior):
            raise AssertionError("Régression V13")
        results[profile] = (merged, hashlib.sha256(target).hexdigest())
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom_originale", type=Path)
    p.add_argument("--sortie", type=Path, default=Path("build_v14"))
    p.add_argument("--comparer-publication", action="store_true")
    args = p.parse_args()
    source = args.rom_originale.read_bytes()
    if len(source) % 0x8000 == 512:
        source = source[512:]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    previous = {p: (ROOT / f"patches/EarthBound_Beginnings_FR_v13_{p}.ips").read_bytes()
                for p in ("accents", "ascii")}
    results = build(source, previous, manifest)
    args.sortie.mkdir(parents=True, exist_ok=True)
    for profile, (patch, target_sha) in results.items():
        name = f"EarthBound_Beginnings_FR_v14_{profile}.ips"
        if args.comparer_publication:
            if patch != (ROOT / "patches" / name).read_bytes():
                raise AssertionError("Le patch publié diffère du patch reconstruit : " + profile)
        (args.sortie / name).write_bytes(patch)
        print(profile, len(patch), "octets, ROM cible SHA-256", target_sha)
    print("V14 : 44 scripts, 130 segments, contrôle source et IPS réussi.")


if __name__ == "__main__":
    main()
