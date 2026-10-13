#!/usr/bin/env python3
"""Tests V14 sans ROM : IPS autonomes, tailles, codes et régression V13."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "traduction"))
from construire_v11 import encode, parse_ips
from construire_v14 import spans_for_entry

manifest = json.loads((ROOT / "traduction/v14_multisegments_fr.json").read_text(encoding="utf-8"))
assert len(manifest["entries"]) == 44
spans = []
for entry in manifest["entries"]:
    start, raw, changes = spans_for_entry(entry)
    assert raw and start == int(entry["id"], 16)
    assert entry["pointer_refs"]
    spans.extend(changes)
assert len(spans) == 130, f"Lot V14 incomplet : {len(spans)} segments"
spans.sort()
for a, b in zip(spans, spans[1:]):
    assert a[0] + len(a[1]) <= b[0], "Chevauchement V14"
for profile in ("accents", "ascii"):
    p13 = (ROOT / f"patches/EarthBound_Beginnings_FR_v13_{profile}.ips").read_bytes()
    p14 = (ROOT / f"patches/EarthBound_Beginnings_FR_v14_{profile}.ips").read_bytes()
    assert p14[:len(p13)-3] == p13[:-3], "V13 modifiée"
    old, new = parse_ips(p13), parse_ips(p14)
    assert len(new) == len(old) + 130
    assert new[:len(old)] == old
    occupied = set()
    for pos, raw in old:
        occupied.update(range(pos, pos+len(raw)))
    for (pos, english, french, ident), (new_pos, payload) in zip(spans, new[len(old):]):
        assert pos == new_pos, ident
        expected = encode(french, profile == "accents").ljust(len(english), b"\x50")
        assert payload == expected, ident
        assert not any(p in occupied for p in range(pos, pos+len(payload))), ident
        occupied.update(range(pos, pos+len(payload)))
    print(f"OK {profile}: {len(old)} enregistrements V13 + 130 = {len(new)} V14")
print("V14 : 44 scripts, 130 segments, non-régression et intégrité IPS validées.")
