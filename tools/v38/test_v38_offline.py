import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def records(data):
    if data[:5] != b"PATCH":
        raise ValueError("En-tête IPS invalide")
    out, p = [], 5
    while data[p:p + 3] != b"EOF":
        offset = int.from_bytes(data[p:p + 3], "big")
        size = int.from_bytes(data[p + 3:p + 5], "big")
        p += 5
        if not size:
            raise ValueError("RLE inattendu")
        out.append((offset, data[p:p + size]))
        p += size
    if p + 3 != len(data):
        raise ValueError("Fin IPS invalide")
    return out


class V38OfflineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads((ROOT / "tools/v38/validation_v38.json").read_text())
        cls.fixtures = json.loads((ROOT / "tools/v38/v38_descriptions_fr.json").read_text())

    def test_manifest_counts(self):
        self.assertEqual(self.plan["base"], "V37")
        self.assertEqual(self.plan["scripts_revised"], 114)
        self.assertEqual(self.plan["newly_translated_descriptions"], 114)
        self.assertEqual(self.plan["newly_translated_fragments"], 126)
        self.assertEqual(len(self.fixtures["scripts"]), 114)

    def test_source_ids_are_unique_and_ordered(self):
        ids = [e["id"] for e in self.fixtures["scripts"]]
        self.assertEqual(ids, sorted(set(ids)))
        self.assertTrue(all(e["fr"] and len(e["fr"]) == len(e["spans"])
                            for e in self.fixtures["scripts"]))

    def test_ips_hashes_and_record_prefixes(self):
        for profile in ("accents", "ascii"):
            old = records((ROOT / f"patches/EarthBound_Beginnings_FR_v37_{profile}.ips").read_bytes())
            raw = (ROOT / f"patches/EarthBound_Beginnings_FR_v38_{profile}.ips").read_bytes()
            new = records(raw)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),
                             self.plan["profiles"][profile]["sha256"])
            self.assertEqual(new[:len(old)], old)
            self.assertEqual(len(new) - len(old), 245)

    def test_declared_rewrites_match_fixture_refs(self):
        fixtures = {e["id"]: e for e in self.fixtures["scripts"]}
        for profile in ("accents", "ascii"):
            moved = self.plan["profiles"][profile]["relocated"]
            rewritten = self.plan["profiles"][profile]["entry_refs_rewritten"]
            self.assertEqual(len(moved), 114)
            self.assertEqual(len(rewritten), 131)
            expected = sorted(ref for e in fixtures.values() for ref in e["entry_refs"])
            self.assertEqual(sorted(x["offset"] for x in rewritten), expected)


if __name__ == "__main__":
    unittest.main()
