"""Offline checks for the published V35 fixtures and autonomous IPS files."""
import copy, json, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_v35 import *

class OfflineV35(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures=json.loads((ROOT/'tools/v35/v35_dialogues_fr.json').read_text())
        cls.report=json.loads((ROOT/'tools/v35/validation_v35.json').read_text())

    def test_declared_counts_and_profiles(self):
        self.assertEqual(len(self.fixtures['scripts']),31)
        self.assertEqual(sum(len(e['fr']) for e in self.fixtures['scripts']),141)
        self.assertEqual(self.report['newly_translated_fragments'],32)
        self.assertEqual(self.report['already_french_fragments'],99)
        self.assertEqual(self.report['unchanged_names_cries_or_punctuation'],10)
        self.assertEqual(json.loads((ROOT/'tools/v35/translations_v35.json').read_text()),OVERRIDES)
        for e in self.fixtures['scripts']:
            self.assertEqual(len(e['spans']),len(e['fr']))
            for profile in ('accents','ascii'):
                for text in e['fr']: encode(text,profile)

    def test_exact_appended_records_and_hashes(self):
        for profile in ('accents','ascii'):
            prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v34_{profile}.ips').read_bytes()
            current=(ROOT/f'patches/EarthBound_Beginnings_FR_v35_{profile}.ips').read_bytes()
            extra,relocated,rewritten,_=build_from_fixtures(self.fixtures,profile)
            self.assertEqual(records(current),records(prior)+extra)
            self.assertEqual(sha(current),self.report['profiles'][profile]['sha256'])
            self.assertEqual(len(relocated),31);self.assertEqual(len(rewritten),30)

    def test_relocated_scripts_are_closed_and_fit_reserves(self):
        for profile in ('accents','ascii'):
            extra,relocated,_,_=build_from_fixtures(self.fixtures,profile); actual=dict(extra)
            for row in relocated:
                p=int(row['offset'],16); raw=actual[p]
                self.assertTrue(any(a<=p<p+len(raw)<=b for a,b in RESERVES))
                parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xb0,0xc0))
                self.assertEqual(parsed['error'],'');self.assertTrue(parsed['terminal']);self.assertEqual(parsed['end'],len(raw))

    def test_bad_fixtures_fail_closed(self):
        bad=copy.deepcopy(self.fixtures);bad['scripts'][0]['fr'].pop()
        with self.assertRaisesRegex(ValueError,'span count'):build_from_fixtures(bad,'accents')
        bad=copy.deepcopy(self.fixtures);bad['scripts'][0]['fr'][0]='A'*20000
        with self.assertRaisesRegex(ValueError,'Reservation exhausted'):build_from_fixtures(bad,'accents')

if __name__=='__main__':unittest.main()
