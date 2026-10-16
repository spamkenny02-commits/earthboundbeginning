import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class V46Prep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads((ROOT/"tools/v46/v46_selection.json").read_text(encoding="utf-8"))
    def test_count_unique(self):
        self.assertEqual(self.d["count"],100)
        ids=[e["id"] for e in self.d["entries"]]
        self.assertEqual(len(ids),len(set(ids)))
    def test_french_segments_nonempty_and_fit_source(self):
        for e in self.d["entries"]:
            for s in e["text_fr_segments"]:
                self.assertTrue(s["french"].strip(),e["id"])
                self.assertLessEqual(len(s["french"].replace("Œ","Oe").replace("œ","oe")),len(s["original"]),e["id"])
    def test_metadata_present(self):
        for e in self.d["entries"]:
            self.assertIn("raw_hex",e)
            self.assertIsInstance(e["literal_pointer_offsets"],list)
            self.assertEqual(e["integration_status"],"not_integrated_not_validated")
if __name__=="__main__": unittest.main()
