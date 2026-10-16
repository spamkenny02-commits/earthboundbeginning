import copy,json,unittest
import build_v54 as b
ROOT=b.ROOT
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v54/v54_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v54/validation_v54.json').read_text())
 def test_inventory_without_counting_prior_french_labels(self):
  self.assertEqual(len(self.f['edits']),85);self.assertEqual(self.plan['labels_translated'],169);self.assertEqual(self.plan['yes_no_blocks'],81);self.assertEqual(self.plan['service_blocks'],4)
  self.assertEqual(sum(len(e['fr']) for e in self.f['edits']),171);self.assertFalse(self.plan['natural_scene_access_verified'])
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v53_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v54_{p}.ips').read_bytes()
   self.assertEqual(new,b.append(old,b.additions_from_fixtures(self.f,p)));self.assertEqual(b.sha(new),self.plan['profiles'][p]['sha256'])
 def test_reject_unsafe_entry(self):
  f=copy.deepcopy(self.f);f['edits'][0]['interior_targets'].append(f"{int(f['edits'][0]['offset'],16)+4:06X}")
  with self.assertRaisesRegex(ValueError,'intérieure'):b.additions_from_fixtures(f,'accents')
 def test_reject_overflow(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr'][0]='A'*1000
  with self.assertRaisesRegex(ValueError,'trop longue'):b.additions_from_fixtures(f,'accents')
 def test_reject_overlap(self):
  f=copy.deepcopy(self.f);f['edits'].append(f['edits'][0])
  with self.assertRaisesRegex(ValueError,'chevauchement'):b.additions_from_fixtures(f,'accents')
 def test_reject_bad_source_capacity(self):
  f=copy.deepcopy(self.f);f['edits'][0]['profiles']['accents']['baseline_hex']='50'
  with self.assertRaisesRegex(ValueError,'Capacité'):b.additions_from_fixtures(f,'accents')
 def test_reject_outside_reserve(self):
  f=copy.deepcopy(self.f);f['edits'][0]['copy_offset']='200000'
  with self.assertRaisesRegex(ValueError,'hors réserve'):b.additions_from_fixtures(f,'accents')
 def test_reject_changed_number_of_choices(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr'].append('Autre')
  with self.assertRaisesRegex(ValueError,'Nombre'):b.additions_from_fixtures(f,'accents')
 def test_option_semantics_and_order(self):
  mapping={'Yes':'Oui','Oui':'Oui','No':'Non','Store':'Déposer','Take out':'Retirer','Heal':'Soigner','Sleep':'Dormir','Small':'Petite','Medium':'Moyenne','Large':'Grande'}
  for e in self.f['edits']:self.assertEqual(e['fr'],[mapping[label] for label in e['en']])
 def test_copies_only_define_choices_then_jump_to_original_selector(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    raw=b.copy_bytes(e,p);parsed=b.parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
    self.assertFalse(parsed['error']);self.assertTrue(parsed['terminal']);self.assertEqual(parsed['end'],len(raw));self.assertEqual(parsed['targets'],[int(e['end'],16)])
    self.assertEqual(b.commands(raw),b'\x19\x02\x02'*len(e['fr'])+b'\x0a'+b.pointer(int(e['end'],16)))
 def test_unsupported_option_counts_rejected(self):
  for labels in (['Oui'],['a','b','c','d']):
   with self.assertRaisesRegex(ValueError,'Deux ou trois'):b.definitions(labels,'accents')
if __name__=='__main__':unittest.main()
