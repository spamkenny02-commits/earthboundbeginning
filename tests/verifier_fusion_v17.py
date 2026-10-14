#!/usr/bin/env python3
"""V17 sans ROM : 195 traductions, conservation V16 et roundtrip IPS."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "traduction"))
from construire_v11 import encode, parse_ips, apply_ips

c = json.loads((ROOT / "traduction/v17_candidats_controles.json").read_text(encoding="utf-8"))
t = json.loads((ROOT / "traduction/v17_traductions_117.json").read_text(encoding="utf-8"))
by_id = {e["id"]: e for e in c["entries"]}
assert t["base"] == c["base"] == "v16"
assert len(t["entries"]) == len({e["id"] for e in t["entries"]}) == 117
assert sum(len(by_id[e["id"]]["pointer_refs_declared"]) for e in t["entries"]) == 130
spans = []
for e in t["entries"]:
    assert e["status"] == "integre_v17"
    src = by_id[e["id"]]["english"]
    texts = [part for part in re.split(r"(\[[0-9A-Fa-f ]+\]|\n|@)", src)
             if part and part not in ("@", "\n") and not part.startswith("[") and re.search("[A-Za-z]", part)]
    assert len(texts) == len(e["translations"]), e["id"]
    for english, french in zip(texts, e["translations"]):
        if english != french:
            spans.append((int(e["id"], 16), english, french))
spans.sort(key=lambda x: x[0])
assert len(spans) == 195
for profile in ("accents", "ascii"):
    old_ips = (ROOT / f"patches/EarthBound_Beginnings_FR_v16_{profile}.ips").read_bytes()
    new_ips = (ROOT / f"patches/EarthBound_Beginnings_FR_v17_{profile}.ips").read_bytes()
    assert new_ips.startswith(old_ips[:-3])
    old = parse_ips(old_ips)
    merged = parse_ips(new_ips)
    assert merged[:len(old)] == old
    added = merged[len(old):]
    assert len(added) == len(spans) == 195
    occupied = bytearray(4194304)
    for pos, data in old:
        occupied[pos:pos+len(data)] = b"\x01" * len(data)
    for (start, english, french), (pos, raw) in zip(spans, added):
        assert start <= pos < start + 2000
        assert len(raw) == len(english)
        expected = encode(french, profile == "accents").ljust(len(english), b"\x50")
        assert raw == expected, (profile, hex(pos))
        assert not any(occupied[pos:pos+len(raw)]), hex(pos)
        occupied[pos:pos+len(raw)] = b"\x01" * len(raw)
    blank = bytes(4194304)
    result = apply_ips(blank, new_ips)
    expected = bytearray(apply_ips(blank, old_ips))
    for pos, raw in added:
        expected[pos:pos+len(raw)] = raw
    assert result == bytes(expected)
    print(f"OK V17 {profile}: {len(old)} enregistrements V16 + 195, zéro collision, roundtrip")
print("OK : 117 scripts, 195 segments, 130 pointeurs déclarés.")
