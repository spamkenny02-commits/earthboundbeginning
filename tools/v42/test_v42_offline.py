import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v42'))
import build_v42 as build
from build_v19 import sha,records

class V42Offline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures=json.loads((ROOT/'tools/v42/v42_dialogues_fr.json').read_text())
        cls.plan=json.loads((ROOT/'tools/v42/validation_v42.json').read_text())

    def test_inventory_and_honest_counts(self):
        entries=self.fixtures['scripts'];self.assertEqual(len(entries),100)
        self.assertEqual(self.plan['newly_translated_fragments'],187)
        self.assertEqual(self.plan['grammatical_fragments_removed'],4)
        self.assertEqual(self.plan['distinct_new_english_fragments'],169)
        self.assertEqual(sum(t in ('Yes','No') for e in entries for t in e['fr']),0)
        changed=[(en,fr) for e in entries for en,fr in zip(e['english'],e['fr']) if en!=fr]
        self.assertEqual(sum(any(c.isalpha() for c in fr) for _,fr in changed),187)
        self.assertTrue(all(any(a!=b for a,b in zip(e['english'],e['fr'])) for e in entries))

    def test_sources_unique_and_nonoverlapping(self):
        entries=self.fixtures['scripts'];self.assertEqual([e['id'] for e in entries],sorted({e['id'] for e in entries}))
        ranges=[(int(e['id'],16),int(e['end'],16)) for e in entries]
        self.assertTrue(all(b<=c for (_,b),(c,_) in zip(ranges,ranges[1:])))

    def test_published_patch_hashes_and_exact_record_inventory(self):
        for p in ('accents','ascii'):
            old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v41_{p}.ips').read_bytes())
            patch=(ROOT/f'patches/EarthBound_Beginnings_FR_v42_{p}.ips').read_bytes();new=records(patch)
            self.assertEqual(sha(patch),self.plan['profiles'][p]['sha256'])
            self.assertEqual(new[:len(old)],old);self.assertEqual(len(new)-len(old),329)
            changes,moved,rewritten=build.additions_from_fixtures(self.fixtures,p)
            self.assertEqual(new[len(old):],changes)
            self.assertEqual(moved,self.plan['profiles'][p]['relocated'])
            self.assertEqual(rewritten,self.plan['profiles'][p]['external_refs_rewritten'])

    def test_reference_inventory(self):
        self.assertEqual(sum(len(e['references']) for e in self.fixtures['scripts']),229)
        for p,r in self.plan['profiles'].items():
            self.assertEqual(len(r['external_refs_rewritten']),229)
            self.assertEqual(sum(len(e['internal_refs']) for e in r['relocated']),0)

    def test_reject_wrong_pointer_proof(self):
        with self.assertRaises(ValueError):build.reference_proof(bytes(64),16,0x366A3C)

if __name__=='__main__':unittest.main()
