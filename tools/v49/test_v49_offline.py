import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v49'))
import build_v49 as b
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v49/v49_fixtures.json').read_text());cls.p=json.loads((ROOT/'tools/v49/validation_v49.json').read_text())
 def test_honest_inventory(self):
  self.assertEqual(len(self.f['edits']),211);self.assertEqual(len(self.f['contexts']),84)
  self.assertEqual(self.p['lexical_spans_translated'],207);self.assertEqual(self.p['distinct_english_fragments'],198)
  self.assertEqual(len({e['offset'] for e in self.f['edits']}),211)
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v48_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v49_{p}.ips').read_bytes()
   self.assertEqual(new,b.append(old,b.additions_from_fixtures(self.f,p)));self.assertEqual(b.sha(new),self.p['profiles'][p]['sha256'])
 def test_writes_are_disjoint_and_same_size_across_profiles(self):
  a=b.additions_from_fixtures(self.f,'accents');z=b.additions_from_fixtures(self.f,'ascii')
  self.assertEqual([(p,len(v)) for p,v in a],[(p,len(v)) for p,v in z])
  self.assertTrue(all(p+len(v)<=q for (p,v),(q,_) in zip(a,a[1:])))
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
if __name__=='__main__':unittest.main()
