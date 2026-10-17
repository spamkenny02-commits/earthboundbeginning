import copy,json,unittest
from pathlib import Path
import build_v56 as b
ROOT=b.ROOT
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v56/v56_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v56/validation_v56.json').read_text())
 def test_inventory(self):
  self.assertEqual((len(self.f['edits']),len(self.f['contexts']),self.plan['new_text_fragments']),(22,17,24))
  self.assertFalse(self.plan['natural_scene_access_verified']);self.assertEqual(self.plan['literal_reference_operands_rewritten'],0)
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v55_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v56_{p}.ips').read_bytes()
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
 def test_merged_run_retains_delay(self):
  e=next(e for e in self.f['edits'] if e['offset']=='351AC4')
  for p in ('accents','ascii'):
   raw=b.copy_text(e,p);self.assertEqual(b.commands(raw+b'\x02'),b'\x10\x0f\x10\x0f\x02')
 def test_reject_branch_command_in_run(self):
  with self.assertRaisesRegex(ValueError,'non permise'):b.text_layout(b.encode('@Texte','accents')+b'\x08'+b.pointer(0x350000)+b.encode('suite','accents'))
 def test_reject_fragment_count_mismatch(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr']=[]
  with self.assertRaisesRegex(ValueError,'Nombre'):b.additions_from_fixtures(f,'accents')
 def test_only_tail_jumps_no_calls_in_additions(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
    edits=dict(b.additions_from_fixtures(self.f,p));self.assertEqual(edits[a],b'\x0a'+b.pointer(d));self.assertEqual(edits[d],b.copy_text(e,p)+b'\x0a'+b.pointer(z))
if __name__=='__main__':unittest.main()
