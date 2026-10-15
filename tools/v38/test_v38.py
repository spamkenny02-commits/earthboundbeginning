import hashlib
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools/v38"), str(ROOT / "tools/v19"),
                str(ROOT / "tools/v33"), str(ROOT / "atelier/outils")]
import build_v38
from build_v19 import ROM_SHA, SIZE, apply, pointer_index, records, sha
from build_v33 import transform
from extraire import parse


def independent_records(data):
    assert data[:5] == b"PATCH"
    out, p = [], 5
    while data[p:p + 3] != b"EOF":
        offset = int.from_bytes(data[p:p + 3], "big")
        size = int.from_bytes(data[p + 3:p + 5], "big")
        p += 5
        if size:
            payload = data[p:p + size]
            p += size
        else:
            count = int.from_bytes(data[p:p + 2], "big")
            payload = data[p + 2:p + 3] * count
            p += 3
        out.append((offset, payload))
    assert p + 3 == len(data)
    return out


def independent_apply(source, patch):
    out = bytearray(source)
    for offset, payload in independent_records(patch):
        out[offset:offset + len(payload)] = payload
    return bytes(out)


class V38Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = Path(os.environ["ROM_PATH"]).read_bytes()
        cls.plan = json.loads((ROOT / "tools/v38/validation_v38.json").read_text())
        cls.fixtures = json.loads((ROOT / "tools/v38/v38_descriptions_fr.json").read_text())
        cls.data = {}
        for profile in ("accents", "ascii"):
            prior = (ROOT / f"patches/EarthBound_Beginnings_FR_v37_{profile}.ips").read_bytes()
            current = (ROOT / f"patches/EarthBound_Beginnings_FR_v38_{profile}.ips").read_bytes()
            cls.data[profile] = {
                "prior": prior, "current": current,
                "old": records(prior), "new": records(current),
                "baseline": apply(cls.original, records(prior)),
                "target": independent_apply(cls.original, current),
            }

    def test_01_source_and_inventory(self):
        self.assertEqual(len(self.original), SIZE)
        self.assertEqual(sha(self.original), ROM_SHA)
        self.assertEqual(self.plan["newly_translated_descriptions"], 114)
        self.assertEqual(self.plan["newly_translated_fragments"], 126)
        self.assertEqual(len(self.fixtures["scripts"]), 114)

    def test_02_v37_is_exact_base(self):
        for profile, expected in build_v38.BASE_SHA.items():
            self.assertEqual(sha(self.data[profile]["prior"]), expected)

    def test_03_reservations_are_safe(self):
        original_refs = pointer_index(self.original)
        for profile, data in self.data.items():
            refs = pointer_index(data["baseline"])
            for a, b in build_v38.RESERVES:
                self.assertEqual(self.original[a:b], bytes(b - a))
                self.assertEqual(data["baseline"][a:b], bytes(b - a))
                self.assertFalse(any(a <= x < b for x in original_refs))
                self.assertFalse(any(a <= x < b for x in refs))
                self.assertFalse(any(p < b and p + len(raw) > a for p, raw in data["old"]))

    def test_04_all_reference_operands_are_proven(self):
        for entry in self.fixtures["scripts"]:
            target = int(entry["id"], 16)
            self.assertTrue(entry["table_refs"])
            self.assertEqual(sorted(entry["entry_refs"]),
                             sorted(entry["table_refs"] + entry["parser_proven_alias_refs"]))
            for ref in entry["table_refs"]:
                q = int(ref, 16)
                self.assertGreaterEqual(q, build_v38.TABLE_START)
                self.assertLess(q, build_v38.TABLE_END)
                self.assertEqual((q - build_v38.TABLE_START) % 4, 0)
            for ref in entry["parser_proven_alias_refs"]:
                q = int(ref, 16)
                for profile in ("accents", "ascii"):
                    self.assertTrue(build_v38.command_operand_proof(
                        self.data[profile]["baseline"], q, target))

    def test_05_previous_records_are_preserved(self):
        for data in self.data.values():
            self.assertEqual(data["new"][:len(data["old"])], data["old"])
            self.assertEqual(len(data["new"]) - len(data["old"]), 245)

    def test_06_independent_ips_application(self):
        for profile, data in self.data.items():
            self.assertEqual(hashlib.sha256(data["current"]).hexdigest(),
                             self.plan["profiles"][profile]["sha256"])
            self.assertEqual(hashlib.sha256(data["target"]).hexdigest(),
                             self.plan["profiles"][profile]["target_rom_sha256"])
            self.assertEqual(data["target"], apply(self.original, data["new"]))

    def test_07_relocated_scripts_match_sources(self):
        fixtures = {e["id"]: e for e in self.fixtures["scripts"]}
        for profile, data in self.data.items():
            for moved in self.plan["profiles"][profile]["relocated"]:
                entry = fixtures[moved["id"]]
                old = bytes.fromhex(entry["baseline_hex"][profile])
                expected, _ = transform(old, entry["spans"], entry["fr"],
                                        int(moved["offset"], 16), profile)
                start = int(moved["offset"], 16)
                actual = data["target"][start:start + moved["new_length"]]
                self.assertEqual(actual, bytes(expected))
                parsed = parse(actual, 0, len(actual) + 1, extra_glyphs=range(0xB0, 0xC0))
                self.assertFalse(parsed["error"])
                self.assertTrue(parsed["terminal"])
                self.assertEqual(parsed["end"], len(actual))

    def test_08_every_live_reference_targets_its_copy(self):
        fixtures = {e["id"]: e for e in self.fixtures["scripts"]}
        for profile, data in self.data.items():
            moved = {e["id"]: int(e["offset"], 16)
                     for e in self.plan["profiles"][profile]["relocated"]}
            for ident, destination in moved.items():
                for ref in fixtures[ident]["entry_refs"]:
                    q = int(ref, 16)
                    self.assertEqual(data["target"][q:q + 4],
                                     (destination + 0xC00000).to_bytes(4, "little"))

    def test_09_sources_and_all_unmarked_bytes_are_unchanged(self):
        for profile, data in self.data.items():
            additions = data["new"][len(data["old"]):]
            mask = bytearray(SIZE)
            for p, raw in additions:
                mask[p:p + len(raw)] = b"\1" * len(raw)
            self.assertTrue(all(a == b for a, b, m in
                                zip(data["baseline"], data["target"], mask) if not m))
            for entry in self.fixtures["scripts"]:
                a, b = int(entry["id"], 16), int(entry["end"], 16)
                self.assertEqual(data["target"][a:b], data["baseline"][a:b])

    def test_10_profiles_share_layout_and_prior_fixes(self):
        a = self.plan["profiles"]["accents"]["relocated"]
        b = self.plan["profiles"]["ascii"]["relocated"]
        self.assertEqual([(x["id"], x["offset"], x["new_length"]) for x in a],
                         [(x["id"], x["offset"], x["new_length"]) for x in b])
        for profile, data in self.data.items():
            for p, raw in data["old"]:
                self.assertEqual(data["target"][p:p + len(raw)],
                                 data["baseline"][p:p + len(raw)])


if __name__ == "__main__":
    unittest.main()
