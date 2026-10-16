import copy,json,unittest
from pathlib import Path
import build_v51 as b
ROOT=b.ROOT
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v51/v51_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v51/validation_v51.json').read_text())
 def test_inventory(self):
  self.assertEqual((len(self.f['edits']),len(self.f['contexts']),len(self.f['deferred'])),(24,21,4))
  self.assertFalse(self.plan['natural_scene_access_verified']);self.assertEqual(self.plan['literal_reference_operands_rewritten'],0)
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v50_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v51_{p}.ips').read_bytes()
   self.assertEqual(new,b.append(old,b.additions_from_fixtures(self.f,p)));self.assertEqual(b.sha(new),self.plan['profiles'][p]['sha256'])
 def test_reject_unsafe_entry(self):
  f=copy.deepcopy(self.f);f['edits'][0]['interior_targets'].append(f"{int(f['edits'][0]['offset'],16)+4:06X}")
  with self.assertRaisesRegex(ValueError,'intérieure'):b.additions_from_fixtures(f,'accents')
 def test_reject_overflow(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr']='A'*1000
  with self.assertRaisesRegex(ValueError,'trop longue'):b.additions_from_fixtures(f,'accents')
 def test_reject_overlap(self):
  f=copy.deepcopy(self.f);f['edits'].append(f['edits'][0])
  with self.assertRaisesRegex(ValueError,'chevauchement'):b.additions_from_fixtures(f,'accents')
 def test_reject_bad_source_capacity(self):
  f=copy.deepcopy(self.f);f['edits'][0]['source_hex']='50'
  with self.assertRaisesRegex(ValueError,'Capacité'):b.additions_from_fixtures(f,'accents')
 def test_reject_outside_reserve(self):
  f=copy.deepcopy(self.f);f['edits'][0]['copy_offset']='200000'
  with self.assertRaisesRegex(ValueError,'hors réserve'):b.additions_from_fixtures(f,'accents')
 def test_deferred_remain_guarded(self):
  for e in self.f['deferred']:
   a=int(e['offset'],16);self.assertTrue(any(a<int(t,16)<a+5 for t in e['interior_targets']))
 def test_only_tail_jumps_no_calls_in_additions(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
    edits=dict(b.additions_from_fixtures(self.f,p));self.assertEqual(edits[a],b'\x0a'+b.pointer(d));self.assertEqual(edits[d],b.encode(e['fr'],p)+b'\x0a'+b.pointer(z))
if __name__=='__main__':unittest.main()
