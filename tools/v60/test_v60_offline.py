import copy,json,unittest
import build_v60 as b
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.f=json.loads((b.ROOT/'tools/v60/v60_fixtures.json').read_text());cls.plan=json.loads((b.ROOT/'tools/v60/validation_v60.json').read_text())
 def test_inventory_and_capacity(self):
  self.assertEqual((len(self.f['titles']),len(self.f['names_preserved'])),(21,42));self.assertEqual((self.f['source_length'],self.f['translated_length'],self.f['height_pixels']),(1026,1004,1680));self.assertLessEqual(self.f['translated_length'],b.CAPACITY)
 def test_exact_patch_rebuild_and_preserved_records(self):
  for p in ('accents','ascii'):
   old=(b.ROOT/f'patches/EarthBound_Beginnings_FR_v59_{p}.ips').read_bytes();new=(b.ROOT/f'patches/EarthBound_Beginnings_FR_v60_{p}.ips').read_bytes()
   self.assertEqual(new,b.append(old,b.additions(self.f)));self.assertEqual(b.records(new),b.records(old)+b.additions(self.f));self.assertEqual(b.sha(new),self.plan['profiles'][p]['sha256'])
 def test_reject_unknown_glyph(self):
  with self.assertRaisesRegex(ValueError,'Glyphe inconnu'):b.decode_staff(b'\x01\x10\x00\xff')
 def test_reject_unknown_control(self):
  with self.assertRaisesRegex(ValueError,'Commande'):b.decode_staff(b'\x05\xff')
 def test_reject_missing_staff_terminator(self):
  with self.assertRaisesRegex(ValueError,'sans fin'):b.decode_staff(b'\x04')
 def test_reject_missing_line_terminator(self):
  with self.assertRaisesRegex(ValueError,'Ligne sans'):b.decode_staff(b'\x01\x42')
 def test_reject_truncated_spacing(self):
  with self.assertRaisesRegex(ValueError,'Espacement'):b.decode_staff(b'\x03')
 def test_reject_line_over_32_tiles(self):
  with self.assertRaisesRegex(ValueError,'trop longue'):b.decode_staff(b'\x01'+bytes([b.MAPS['small']['A']])*33+b'\x00\xff')
 def test_reject_corrupt_fixture_payload(self):
  f=copy.deepcopy(self.f);f['translated_hex']='ff'
  with self.assertRaisesRegex(ValueError,'divergente'):b.additions(f)
 def test_reject_changed_placement_and_report(self):
  for key,value in (('offset','17FBE9'),('capacity',1027),('height_pixels',1)):
   f=copy.deepcopy(self.f);f[key]=value
   with self.assertRaises(ValueError):b.additions(f)
 def test_all_roles_changed_and_name_field_retained(self):
  old,h,n=b.decode_staff(bytes.fromhex(self.f['source_hex']));new,h,n=b.decode_staff(bytes.fromhex(self.f['translated_hex']));changed=[(a.get('text'),z.get('text')) for a,z in zip(old,new) if a!=z]
  self.assertEqual(dict(changed),b.TITLES);self.assertEqual(sum(e['type']=='player_name' for e in new),1)
if __name__=='__main__':unittest.main()
