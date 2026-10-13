#!/usr/bin/env python3
"""V15 sans ROM : intégrité des deux IPS et non-régression V14."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "traduction"))
from construire_v11 import encode, parse_ips
from construire_v14 import spans_for_entry

manifest = json.loads((ROOT / "traduction/v15_dialogues_fr.json").read_text(encoding="utf-8"))
assert len(manifest["entries"]) == 32
assert len({e["id"] for e in manifest["entries"]}) == 32
spans = []
for e in manifest["entries"]:
    start, raw, changes = spans_for_entry(e)
    assert start == int(e["id"], 16) and raw
    assert e["pointer_refs"]
    spans.extend(changes)
assert len(spans) == 77, f"77 segments attendus, {len(spans)} reçus"
spans.sort()
for a, b in zip(spans, spans[1:]):
    assert a[0] + len(a[1]) <= b[0], "Segments V15 chevauchants"

for profile in ("accents", "ascii"):
    old_bytes = (ROOT / f"patches/EarthBound_Beginnings_FR_v14_{profile}.ips").read_bytes()
    new_bytes = (ROOT / f"patches/EarthBound_Beginnings_FR_v15_{profile}.ips").read_bytes()
    assert new_bytes.startswith(old_bytes[:-3]), "Préfixe V14 modifié"
    old, new = parse_ips(old_bytes), parse_ips(new_bytes)
    assert len(new) == len(old) + 77
    assert new[:len(old)] == old, "Régression IPS V14"
    occupied = set()
    for pos, data in old:
        occupied.update(range(pos, pos+len(data)))
    for (pos, english, french, ident), (patch_pos, payload) in zip(spans, new[len(old):]):
        assert pos == patch_pos, ident
        encoded = encode(french, profile == "accents")
        assert len(encoded) <= len(english), ident
        assert payload == encoded.ljust(len(english), b"\x50"), ident
        assert all(pos+i not in occupied for i in range(len(payload))), ident
        occupied.update(range(pos, pos+len(payload)))
    print(f"OK {profile} : {len(old)} enregistrements V14 + 77 = {len(new)} V15")
print("OK : 32 scripts, 77 segments, 2 IPS et aucune collision V14.")
