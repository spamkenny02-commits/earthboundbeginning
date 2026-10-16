import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v50'))
import build_v50 as b
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v50/v50_fixtures.json').read_text());cls.p=json.loads((ROOT/'tools/v50/validation_v50.json').read_text())
 def test_honest_inventory(self):
  self.assertEqual(len(self.f['edits']),46);self.assertEqual(len(self.f['contexts']),29)
  self.assertEqual(self.p['lexical_spans_translated'],46);self.assertEqual(self.p['distinct_english_fragments'],41)
  self.assertEqual(len({e['offset'] for e in self.f['edits']}),46)
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v49_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v50_{p}.ips').read_bytes()
   self.assertEqual(new,b.append(old,b.additions_from_fixtures(self.f,p)));self.assertEqual(b.sha(new),self.p['profiles'][p]['sha256'])
 def test_writes_are_disjoint_and_same_size_across_profiles(self):
  a=b.additions_from_fixtures(self.f,'accents');z=b.additions_from_fixtures(self.f,'ascii')
  self.assertEqual([(p,len(v)) for p,v in a],[(p,len(v)) for p,v in z])
  ranges=sorted((p,p+len(v)) for p,v in a);self.assertTrue(all(z<=q for (_,z),(q,_) in zip(ranges,ranges[1:])))
 def test_reject_overflow(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr']='A'*10000
  with self.assertRaisesRegex(ValueError,'trop longue'):b.additions_from_fixtures(f,'accents')
 def test_reject_overlapping_writes(self):
  f=copy.deepcopy(self.f);f['edits'].append(f['edits'][0])
  with self.assertRaisesRegex(ValueError,'chevauchement'):b.additions_from_fixtures(f,'accents')
 def test_reject_bad_capacity(self):
  f=copy.deepcopy(self.f);f['edits'][0]['source_hex']='50'
  with self.assertRaisesRegex(ValueError,'Capacité'):b.additions_from_fixtures(f,'accents')
 def test_french_span_parser_handles_accents_and_dictionary_tokens(self):
  self.assertEqual(b.spans_fr(bytes.fromhex('70b015000302')),[(0,4)])
  with self.assertRaisesRegex(ValueError,'non fermé'):b.spans_fr(bytes.fromhex('70b0'))
 def test_deferred_and_excluded_are_not_new_translations(self):
  edits={(e['offset'],e['end']) for e in self.f['edits']}
  self.assertFalse(edits&{(e['offset'],e['end']) for e in self.f['deferred']})
  self.assertNotIn('3508F4',{e['id'] for e in self.f['contexts']});self.assertNotIn('35EE08',{e['id'] for e in self.f['contexts']})
 def test_grammar_reserve_exhaustion(self):
  f=copy.deepcopy(self.f['grammar']);f['reserve'][1]=f['reserve'][0]
  with self.assertRaisesRegex(ValueError,'épuisée'):b.helper_additions(f,'accents')
 def test_audit_is_not_a_pointer_allowlist(self):
  audit=json.loads((ROOT/'tools/v50/audit_references_v49.json').read_text())
  self.assertEqual(len(audit),21)
  self.assertTrue(all(e['accepted_for_text_edit'] is False for e in audit))
if __name__=='__main__':unittest.main()
