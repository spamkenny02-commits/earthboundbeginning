import copy,json,unittest
from pathlib import Path
import build_v59 as b
ROOT=b.ROOT
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v59/v59_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v59/validation_v59.json').read_text())
 def test_inventory(self):
  self.assertEqual((len(self.f['edits']),len(self.f['contexts']),self.plan['new_text_fragments']),(59,39,61))
  self.assertFalse(self.plan['natural_scene_access_verified']);self.assertEqual(self.plan['literal_reference_operands_rewritten'],0)
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v58_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v59_{p}.ips').read_bytes()
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
 def test_reject_branch_command_in_run(self):
  with self.assertRaisesRegex(ValueError,'non permi'):b.text_layout(b.encode('@Texte','accents')+b'\x08'+b.pointer(0x350000)+b.encode('suite','accents'))
 def test_reject_fragment_count_mismatch(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr']=[]
  with self.assertRaisesRegex(ValueError,'Nombre'):b.additions_from_fixtures(f,'accents')
 def test_only_tail_jumps_no_calls_in_additions(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
    edits=dict(b.additions_from_fixtures(self.f,p));self.assertEqual(edits[a],b'\x0a'+b.pointer(d));self.assertEqual(edits[d],b.copy_text(e,p)+b'\x0a'+b.pointer(z))
 def test_reject_unapproved_effect_command(self):
  raw=b.encode('@Texte','accents')+b'\x1f\x02\x44'+b.encode('suite','accents')
  with self.assertRaises(ValueError):b.text_layout(raw)
 def test_reject_branch_subcommand(self):
  raw=b.encode('@Texte','accents')+b'\x1b\x03'+b.pointer(0x350000)+b.encode('suite','accents')
  with self.assertRaises(ValueError):b.text_layout(raw)
 def test_reject_sprite_zero_hole_even_if_fixture_claims_it_is_free(self):
  f=copy.deepcopy(self.f);f['edits'][0]['copy_offset']='256BA0';f['reserves'].append(['256000','257000'])
  with self.assertRaisesRegex(ValueError,'hors réserve'):b.additions_from_fixtures(f,'accents')
 def test_short_conjunction_preserves_complete_trailing_item_output(self):
  e=next(e for e in self.f['edits'] if e['offset']=='0638CD')
  for p in ('accents','ascii'):
   self.assertEqual(b.copy_text(e,p),b.encode(' et ',p)+b'\x1c\x05\x00')
   self.assertEqual(b.commands(b.copy_text(e,p)+b'\x02'),b'\x1c\x05\x00\x02')
 def test_reject_truncated_trailing_variable(self):
  with self.assertRaises(ValueError):b.text_layout(b.encode(' et ','accents')+b'\x1c\x05')
if __name__=='__main__':unittest.main()
