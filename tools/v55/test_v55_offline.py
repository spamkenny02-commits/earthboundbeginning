import copy,json,unittest
import build_v55 as b
ROOT=b.ROOT
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v55/v55_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v55/validation_v55.json').read_text())
 def test_inventory(self):
  self.assertEqual(len(self.f['edits']),18);self.assertEqual(sum(e['kind']=='fares' for e in self.f['edits']),16);self.assertFalse(self.plan['natural_scene_access_verified'])
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v54_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v55_{p}.ips').read_bytes();self.assertEqual(new,b.append(old,b.additions_from_fixtures(self.f,p)));self.assertEqual(b.sha(new),self.plan['profiles'][p]['sha256'])
 def test_rows_width_and_currency(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    for r in e.get('rows',[]):
     raw=b.row_bytes(r,p,self.f);self.assertEqual(b.width(raw,p,self.f),128);self.assertTrue(raw.startswith(b.encode('Vers '+r['city'],p)));self.assertTrue(raw.endswith(b.encode(str(r['fare'])+' $',p)))
 def test_original_fares_and_order(self):
  self.assertEqual([(r['city'],r['fare']) for e in self.f['edits'] for r in e.get('rows',[])],[('Reindeer',9),('Snowman',11),('Merrysville',25),('Reindeer',16),('Spookane',25),('Snowman',36),('Spookane',9),('Merrysville',16),('Snowman',20),('Merrysville',12),('Reindeer',28),('Spookane',37),('Snowman',48),('Youngtown',37),('Youngtown',12),('Youngtown',28)])
 def reject(self,mutate,reason):
  f=copy.deepcopy(self.f);mutate(f)
  with self.assertRaisesRegex(ValueError,reason):b.additions_from_fixtures(f,'accents')
 def test_unsafe_entry(self):self.reject(lambda f:f['edits'][0]['interior_targets'].append(f"{int(f['edits'][0]['offset'],16)+4:06X}"),'intérieure')
 def test_changed_city(self):self.reject(lambda f:f['edits'][0]['rows'][0].update(city='Paris'),'Ville')
 def test_changed_fare(self):self.reject(lambda f:f['edits'][0]['rows'][0].update(fare=99),'tarif')
 def test_bad_width(self):self.reject(lambda f:f['font'].update(row_width=1),'trop longue')
 def test_overflow(self):self.reject(lambda f:f['edits'][-1].update(fr='A'*1000),'trop longue')
 def test_overlap(self):self.reject(lambda f:f['edits'].append(f['edits'][0]),'chevauchement')
 def test_bad_capacity(self):self.reject(lambda f:f['edits'][0]['profiles']['accents'].update(baseline_hex='50'),'Capacité')
 def test_outside_reserve(self):self.reject(lambda f:f['edits'][0].update(copy_offset='200000'),'hors réserve')
 def test_copies_closed_and_return(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    raw=b.copy_bytes(e,p,self.f);parsed=b.parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0));self.assertFalse(parsed['error']);self.assertTrue(parsed['terminal']);self.assertEqual(parsed['end'],len(raw));self.assertEqual(parsed['targets'],[int(e['end'],16)])
if __name__=='__main__':unittest.main()
