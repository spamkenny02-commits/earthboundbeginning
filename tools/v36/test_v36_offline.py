"""Offline validation of V36 autonomous IPS files."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_v36 import *


class OfflineV36(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "tools/v36/validation_v36.json").read_text())

    def test_scope_is_reported_without_inflating_text_counts(self):
        self.assertEqual(self.report["graphics_translated"], 1)
        self.assertEqual(self.report["new_dialogue_fragments"], 0)
        self.assertEqual(self.report["scripts_revised"], 0)
        self.assertEqual(self.report["source_label"], "YOU WON!")
        self.assertEqual(self.report["french_label"], "VICTOIRE")

    def test_exact_three_appended_records(self):
        for profile in ("accents", "ascii"):
            prior = (ROOT / f"patches/EarthBound_Beginnings_FR_v35_{profile}.ips").read_bytes()
            current = (ROOT / f"patches/EarthBound_Beginnings_FR_v36_{profile}.ips").read_bytes()
            old, new = records(prior), records(current)
            self.assertEqual(new[:len(old)], old)
            self.assertEqual(len(new) - len(old), 3)
            self.assertEqual(new[-3][0], DESTINATION)
            self.assertEqual(sha(new[-3][1]), self.report["compressed_sha256"])
            self.assertEqual(new[-2:], [(POINTER_OFFSET + 1, b"\x00\x78"), (POINTER_OFFSET + 6, b"\xd7\x00")])
            self.assertEqual(sha(current), self.report["profiles"][profile]["sha256"])

    def test_payload_fits_declared_null_reserve(self):
        self.assertEqual(self.report["compressed_length"], len(records((ROOT / "patches/EarthBound_Beginnings_FR_v36_accents.ips").read_bytes())[-3][1]))
        self.assertLessEqual(DESTINATION + self.report["compressed_length"], RESERVATION_END)
        self.assertEqual(self.report["tiles_replaced"], 16)

    def test_glyph_source_is_complete(self):
        self.assertEqual(set(GLYPHS), set("VICTOIRE"))
        self.assertTrue(all(len(rows) == 7 and all(len(row) == 5 for row in rows) for rows in GLYPHS.values()))
        self.assertTrue((ROOT / "tools/v36/victoire_preview.png").is_file())


if __name__ == "__main__":
    unittest.main()
