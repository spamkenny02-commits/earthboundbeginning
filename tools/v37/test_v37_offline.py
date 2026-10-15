"""Offline checks for V37 source declarations and autonomous IPS files."""
import json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_v37 import *

class OfflineV37(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.report=json.loads((ROOT/'tools/v37/validation_v37.json').read_text())

    def test_scope_counts_are_honest(self):
        self.assertEqual(self.report['graphics_translated'],1)
        self.assertEqual(self.report['new_dialogue_fragments'],0)
        self.assertEqual(self.report['scripts_revised'],0)
        self.assertEqual(self.report['labels'],[{'source':'SMAAAASH!!','french':'COUP CRIT!'}])

    def test_one_controlled_record_is_appended(self):
        for profile in ('accents','ascii'):
            old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v36_{profile}.ips').read_bytes())
            data=(ROOT/f'patches/EarthBound_Beginnings_FR_v37_{profile}.ips').read_bytes();new=records(data)
            self.assertEqual(new[:-1],old);self.assertEqual(new[-1][0],DESTINATION)
            self.assertEqual(sha(new[-1][1]),self.report['compressed_sha256'])
            self.assertEqual(sha(data),self.report['profiles'][profile]['sha256'])

    def test_payload_fits_and_tiles_are_exact(self):
        self.assertLessEqual(DESTINATION+self.report['compressed_length'],RESERVATION_END)
        expected=list(range(352,362))+list(range(368,378))
        self.assertEqual(self.report['tile_indexes'],expected)
        self.assertEqual(self.report['tiles_replaced'],20)
        self.assertEqual(self.report['hp_to_pv_excluded_shared_tiles'],[8,9,24,25])

    def test_glyphs_and_preview(self):
        self.assertEqual(set(GLYPHS),set('COUP RIT!'))
        self.assertTrue(all(len(rows)==7 and all(len(row)==5 for row in rows) for rows in GLYPHS.values()))
        self.assertTrue((ROOT/'tools/v37/v37_preview.png').is_file())

if __name__=='__main__':unittest.main()
