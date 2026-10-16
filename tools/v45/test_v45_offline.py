import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v45'))
import build_v45 as build
from build_v19 import sha,records

class V45Offline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures=json.loads((ROOT/'tools/v45/v45_dialogues_fr.json').read_text())
        cls.plan=json.loads((ROOT/'tools/v45/validation_v45.json').read_text())

    def test_inventory_and_honest_counts(self):
        entries=self.fixtures['scripts'];self.assertEqual(len(entries),13)
        self.assertEqual(self.plan['newly_translated_fragments'],20)
        self.assertEqual(self.plan['nonlexical_fragments_adjusted'],6)
        self.assertEqual(self.plan['onomatopoeia_characters_adjusted'],0)
        self.assertEqual(self.plan['distinct_new_english_fragments'],18)
        self.assertEqual(sum(t in ('Yes','No') for e in entries for t in e['fr']),4)
        changed=[(en,fr) for e in entries for en,fr in zip(e['english'],e['fr']) if en!=fr]
        self.assertEqual(sum(sum(c.isalpha() for c in fr)>1 for _,fr in changed),20)
        self.assertTrue(all(any(a!=b for a,b in zip(e['english'],e['fr'])) for e in entries if not e['private_helper']))

    def test_sources_unique_and_nonoverlapping(self):
        entries=self.fixtures['scripts'];self.assertEqual([e['id'] for e in entries],sorted({e['id'] for e in entries}))
        ranges=[(int(e['id'],16),int(e['end'],16)) for e in entries]
        self.assertTrue(all(b<=c for (_,b),(c,_) in zip(ranges,ranges[1:])))

    def test_published_patch_hashes_and_exact_record_inventory(self):
        for p in ('accents','ascii'):
            old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v44_{p}.ips').read_bytes())
            patch=(ROOT/f'patches/EarthBound_Beginnings_FR_v45_{p}.ips').read_bytes();new=records(patch)
            self.assertEqual(sha(patch),self.plan['profiles'][p]['sha256'])
            self.assertEqual(new[:len(old)],old);self.assertEqual(len(new)-len(old),19)
            changes,moved,rewritten=build.additions_from_fixtures(self.fixtures,p)
            self.assertEqual(new[len(old):],changes)
            self.assertEqual(moved,self.plan['profiles'][p]['relocated'])
            self.assertEqual(rewritten,self.plan['profiles'][p]['external_refs_rewritten'])

    def test_reference_inventory(self):
        self.assertEqual(sum(len(e['references']) for e in self.fixtures['scripts']),16)
        for p,r in self.plan['profiles'].items():
            self.assertEqual(len(r['external_refs_rewritten']),6)
            self.assertEqual(sum(len(e['internal_refs']) for e in r['relocated']),24)

    def test_reject_wrong_pointer_proof(self):
        with self.assertRaises(ValueError):build.reference_proof(bytes(64),16,0x366A3C)


    def test_contiguous_scripts_do_not_steal_each_others_entry(self):
        # The longer second source is allocated first. The first source's
        # exclusive end is the second source's entry and must not overwrite it.
        fixture={'scripts':[
            {'id':'002000','end':'002002','original_hex':'7102','spans':[[0,1]],'fr':['A'],'references':[]},
            {'id':'002002','end':'002005','original_hex':'727302','spans':[[0,2]],'fr':['Une copie bien plus longue'],
             'references':[{'offset':'001000','target':'002002','proof':{}}]},
        ]}
        for p in ('accents','ascii'):
            changes,moved,refs=build.additions_from_fixtures(fixture,p)
            destination=next(int(e['offset'],16) for e in moved if e['id']=='002002')
            self.assertEqual(dict(changes)[0x1000],(destination+0xC00000).to_bytes(4,'little'))
            self.assertEqual(int(refs[0]['new_target'],16),destination)

if __name__=='__main__':unittest.main()
