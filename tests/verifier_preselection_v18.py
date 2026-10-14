#!/usr/bin/env python3
"""Préselection V18 reproductible, sans ROM ni traduction intégrée."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "traduction"))
from construire_v11 import parse_ips

pre = json.loads((ROOT / "traduction/v18_preselection.json").read_text())
catalogue = json.loads((ROOT / "traduction/v17_priorites_non_verifiees.json").read_text())
v17 = json.loads((ROOT / "traduction/v17_traductions_117.json").read_text())
used = {e["id"] for e in v17["entries"]}
occupied = bytearray(4194304)
for profile in ("accents", "ascii"):
    patch = (ROOT / f"patches/EarthBound_Beginnings_FR_v17_{profile}.ips").read_bytes()
    for pos, raw in parse_ips(patch):
        occupied[pos:pos+len(raw)] = b"\x01" * len(raw)
ids, already, collisions = [], 0, 0
for e in catalogue["entries"]:
    if e["id"] in used:
        already += 1
        continue
    start = int(e["id"], 16)
    end = start + len(e["english"]) + e["english"].count("\n") + 11
    if any(occupied[start:end]):
        collisions += 1
        continue
    ids.append(e["id"])
assert pre["base"] == "v17"
assert pre["status"] == "NON_VERIFIE_ROM_NON_TRADUIT"
assert len(catalogue["entries"]) == 150
assert (already, collisions, len(ids)) == (15, 40, 95)
assert ids == pre["ids"]
print("OK : 95 candidats V18 présélectionnés ; aucune traduction V18 intégrée.")
