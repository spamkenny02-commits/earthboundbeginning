import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v47'))
import build_v47 as b
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v47/v47_dialogues_fr.json').read_text())
  cls.p=json.loads((ROOT/'tools/v47/validation_v47.json').read_text())
 def test_real_translation_inventory(self):
  self.assertEqual(len(self.f['scripts']),21)
  self.assertEqual(self.p['newly_translated_fragments'],34)
  self.assertEqual(self.p['distinct_new_english_fragments'],28)
  self.assertTrue(all(any(a!=z for a,z in zip(e['english'],e['fr'])) for e in self.f['scripts']))
 def test_exact_rebuild_and_hashes(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v46_{p}.ips').read_bytes()
   new=(ROOT/f'patches/EarthBound_Beginnings_FR_v47_{p}.ips').read_bytes()
   changes,moved,refs=b.additions_from_fixtures(self.f,p)
   self.assertEqual(new,b.append(old,changes))
   self.assertEqual(b.sha(new),self.p['profiles'][p]['sha256'])
   self.assertEqual(moved,self.p['profiles'][p]['relocated'])
   self.assertEqual(refs,self.p['profiles'][p]['external_refs_rewritten'])
 def test_sources_are_disjoint_and_menus_deferred(self):
  ranges=[(int(e['id'],16),int(e['end'],16)) for e in self.f['scripts']]
  self.assertTrue(all(a<z for a,z in ranges))
  self.assertTrue(all(z<=c for (_,z),(c,_) in zip(ranges,ranges[1:])))
  choices=[(a,z) for e in self.f['scripts'] for a,z in zip(e['english'],e['fr']) if a in ('Yes','No')]
  self.assertEqual(choices,[('Yes','Yes'),('No','No')])
  self.assertTrue(all(int(e['id'],16)<0x390000 for e in self.f['scripts']))
 def test_unproven_references_excluded(self):
  held={r['offset'] for e in self.f['scripts'] for r in e['preserved_unproven_refs']}
  rewritten={r['offset'] for r in self.p['profiles']['accents']['external_refs_rewritten']}
  self.assertEqual(len(held),14)
  self.assertFalse(held&rewritten)
 def test_adjacent_entries_keep_distinct_targets(self):
  f={'scripts':[{'id':'002000','end':'002002','original_hex':'7102','spans':[[0,1]],'fr':['A'],'references':[]},{'id':'002002','end':'002005','original_hex':'727302','spans':[[0,2]],'fr':['Une copie plus longue'],'references':[{'offset':'001000','target':'002002','proof':{}}]}]}
  for p in ('accents','ascii'):
   changes,moved,refs=b.additions_from_fixtures(f,p)
   target=next(int(e['offset'],16) for e in moved if e['id']=='002002')
   self.assertEqual(dict(changes)[0x1000],b.pointer(target))
 def test_reserve_exhaustion_is_rejected(self):
  old=b.RESERVES
  try:
   b.RESERVES=((0x320000,0x320001),)
   with self.assertRaises(ValueError):b.additions_from_fixtures(self.f,'accents')
  finally:b.RESERVES=old
if __name__=='__main__':unittest.main()
