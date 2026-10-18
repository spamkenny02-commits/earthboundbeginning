import copy,json,unittest
import build_v61 as b
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.f=json.loads((b.ROOT/'tools/v61/v61_fixtures.json').read_text());cls.plan=json.loads((b.ROOT/'tools/v61/validation_v61.json').read_text())
 def test_exact_patch_rebuild_and_unchanged_prior_records(self):
  for p in ('accents','ascii'):
   old=(b.ROOT/f'patches/EarthBound_Beginnings_FR_v60_{p}.ips').read_bytes();new=(b.ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes();self.assertEqual(new,b.append(old,b.additions(self.f,p)));self.assertEqual(b.records(new),b.records(old)+b.additions(self.f,p));self.assertEqual(b.sha(new),self.plan['profiles'][p]['sha256'])
 def test_inventory_counts_scenes_separately_from_glyphs(self):
  self.assertEqual((len(self.f['edits']),len(self.f['contexts'])),(20,5));self.assertEqual(self.plan['short_lexical_fragments'],2);self.assertEqual(self.plan['timed_boo_scenes'],3);self.assertEqual(self.plan['new_allocations'],0)
 def test_reject_changed_text_length_or_inventory(self):
  for key,value in (('end','34FAE3'),('fr','@Objet: ')):
   f=copy.deepcopy(self.f);f['edits'][0][key]=value
   with self.assertRaises(ValueError):b.additions(f,'accents')
 def test_reject_damaged_capacity(self):
  f=copy.deepcopy(self.f);f['edits'][0]['profiles']['ascii']['baseline_hex']='70'
  with self.assertRaisesRegex(ValueError,'Taille'):b.additions(f,'ascii')
if __name__=='__main__':unittest.main()
