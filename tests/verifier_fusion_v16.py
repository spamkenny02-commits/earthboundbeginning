#!/usr/bin/env python3
"""V16 sans ROM : conservation V15, offsets, encodage et absence de collisions."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "traduction"))
from construire_v11 import encode, parse_ips
from construire_v14 import spans_for_entry

m = json.loads((ROOT / "traduction/v16_dialogues_fr.json").read_text(encoding="utf-8"))
assert len(m["entries"]) == 100
assert len({e["id"] for e in m["entries"]}) == 100
assert len(m["excluded_interior_pointer_segments"]) == 13
spans = []
for e in m["entries"]:
    start, raw, changes = spans_for_entry(e)
    assert start == int(e["id"], 16) and raw
    assert e["pointer_refs"]
    spans.extend(changes)
assert len(spans) == 128, f"128 segments attendus, {len(spans)} reçus"
spans.sort()
for a, b in zip(spans, spans[1:]):
    assert a[0] + len(a[1]) <= b[0], "Segments V16 chevauchants"

for profile in ("accents", "ascii"):
    prior = (ROOT / f"patches/EarthBound_Beginnings_FR_v15_{profile}.ips").read_bytes()
    patch = (ROOT / f"patches/EarthBound_Beginnings_FR_v16_{profile}.ips").read_bytes()
    assert patch.startswith(prior[:-3]), "Préfixe IPS V15 modifié"
    old, new = parse_ips(prior), parse_ips(patch)
    assert len(new) == len(old) + 128
    assert new[:len(old)] == old
    occupied = set()
    for pos, raw in old:
        occupied.update(range(pos, pos+len(raw)))
    for (pos, english, french, ident), (patch_pos, payload) in zip(spans, new[len(old):]):
        assert patch_pos == pos, ident
        translated = encode(french, profile == "accents")
        assert len(translated) <= len(english), ident
        assert payload == translated.ljust(len(english), b"\x50"), ident
        assert all(pos+i not in occupied for i in range(len(payload))), ident
        occupied.update(range(pos, pos+len(payload)))
    print(f"OK {profile}: {len(old)} enregistrements V15 + 128 = {len(new)} V16")
print("OK : 100 scripts audités, 128 nouveaux segments, zéro collision.")
