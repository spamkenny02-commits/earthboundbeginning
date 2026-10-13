#!/usr/bin/env python3
"""Prévalidation V15, aucun patch créé."""
import copy
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "traduction"))
from construire_v11 import encode, parse_ips
from construire_v14 import spans_for_entry, SPLIT

draft = json.loads((ROOT / "traduction/v15_candidats_a_valider.json").read_text())
base = json.loads((ROOT / "traduction/v14_multisegments_fr.json").read_text())
assert len(draft["candidates"]) == 8 and len(base["entries"]) == 44
by_id = {e["id"]: e for e in base["entries"]}
def texts(e):
    return [p for p in filter(None, SPLIT.split(e["english"]))
            if p not in ("@", "\n") and not p.startswith("[") and re.search("[A-Za-z]", p)]
prior = [s for e in base["entries"] for s in spans_for_entry(e)[2]]
assert len(prior) == 130
occupied = []
for profile in ("accents", "ascii"):
    data = (ROOT / f"patches/EarthBound_Beginnings_FR_v14_{profile}.ips").read_bytes()
    occupied.append([(p, p+len(raw)) for p, raw in parse_ips(data)])
seen = set()
new = []
for c in draft["candidates"]:
    key = (c["id"], c["segment_index"])
    assert key not in seen
    seen.add(key)
    entry = by_id[c["id"]]
    assert entry["translations"][key[1]] == texts(entry)[key[1]]
    changed = copy.deepcopy(entry)
    changed["translations"][key[1]] = c["fr"]
    original_positions = {p for p, _, _, _ in spans_for_entry(entry)[2]}
    added = [x for x in spans_for_entry(changed)[2] if x[0] not in original_positions]
    assert len(added) == 1
    pos, old, french, _ = added[0]
    for accented in (True, False):
        assert len(encode(french, accented)) <= len(old)
    for ranges in occupied:
        assert all(pos+len(old) <= a or b <= pos for a,b in ranges)
    new.append((pos,pos+len(old)))
new.sort()
assert all(a[1] <= b[0] for a,b in zip(new,new[1:]))
print("OK: 8 brouillons V15, longueurs et encodage, sans collision IPS V14.")
print("Non vérifié: pointeurs intérieurs sur ROM, IPS V15 et émulation.")
