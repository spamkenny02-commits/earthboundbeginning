import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v46'))
import build_v46 as b

class V46Offline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=json.loads((ROOT/'tools/v46/v46_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v46/validation_v46.json').read_text())

    def test_patch_hashes_and_exact_added_records(self):
        for p in ('accents','ascii'):
            prior=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v45_{p}.ips').read_bytes())
            patch=(ROOT/f'patches/EarthBound_Beginnings_FR_v46_{p}.ips').read_bytes();rec=b.records(patch)
            self.assertEqual(b.sha(patch),self.plan['profiles'][p]['sha256']);self.assertEqual(rec[:len(prior)],prior)
            changes,food,refs=b.additions_from_fixtures(self.f,p)
            self.assertEqual(rec[len(prior):],changes);self.assertEqual(len(changes),17)
            self.assertEqual(food,self.plan['profiles'][p]['foods']);self.assertEqual(refs,self.plan['profiles'][p]['references_rewritten'])

    def test_preparation_counts_are_not_new_translations(self):
        a=self.f['audit_preparation'];self.assertEqual((a['selected'],a['already_modified'],a['identical_drafts']),(100,98,2))
        self.assertEqual(a['new_integrations_from_preparation'],0)
        self.assertEqual(self.plan['preparation_entries_newly_integrated'],0)
        self.assertEqual(self.plan['newly_translated_food_messages'],2)

    def test_context_inventory_and_capacity(self):
        for p,data in self.f['profiles'].items():
            self.assertEqual(len(data['contexts']),7);self.assertEqual(sum(e['replacement'] is not None for e in data['contexts']),5)
            self.assertEqual(len({e['id'] for e in data['contexts']}),7)
            for e in data['contexts']:
                if e['replacement'] is not None:self.assertLessEqual(len(b.encode(e['replacement'],p)),e['text_capacity'])

    def test_reuses_the_existing_french_helper(self):
        plan=json.loads((ROOT/'tools/v45/validation_v45.json').read_text())
        for p in ('accents','ascii'):
            e=next(e for e in plan['profiles'][p]['relocated'] if e['id']=='07E6D7')
            self.assertEqual(self.f['helper'],e['offset'])

    def test_changes_are_disjoint_and_menu_labels_are_not_selected(self):
        for p in ('accents','ascii'):
            changes,_,_=b.additions_from_fixtures(self.f,p);ranges=sorted((a,a+len(raw)) for a,raw in changes)
            self.assertTrue(all(z<=c for (_,z),(c,_) in zip(ranges,ranges[1:])))
            self.assertEqual(sum(len(e['references']) for e in self.f['profiles'][p]['foods']),3)
            self.assertTrue(all(e['replacement'] not in ('Yes','No','Throw away') for e in self.f['profiles'][p]['contexts']))

    def test_reject_exhausted_reserve(self):
        f=copy.deepcopy(self.f);f['reserve'][1]=f['reserve'][0]
        with self.assertRaises(ValueError):b.additions_from_fixtures(f,'accents')

if __name__=='__main__':unittest.main()
