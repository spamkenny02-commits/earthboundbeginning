import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v48'))
import build_v48 as b
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v48/v48_dialogues_fr.json').read_text())
  cls.p=json.loads((ROOT/'tools/v48/validation_v48.json').read_text())
 def test_translation_inventory(self):
  self.assertEqual(len(self.f['scripts']),44)
  self.assertEqual(sum(not e['private_helper'] for e in self.f['scripts']),40)
  self.assertEqual(self.p['newly_translated_fragments'],66)
  self.assertEqual(self.p['distinct_new_english_fragments'],60)
  self.assertEqual(len(self.f['touchups']),2)
  self.assertEqual(self.p['nonlexical_fragments_adjusted'],13)
 def test_exact_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v47_{p}.ips').read_bytes()
   new=(ROOT/f'patches/EarthBound_Beginnings_FR_v48_{p}.ips').read_bytes()
   changes,moved,refs=b.additions_from_fixtures(self.f,p)
   self.assertEqual(new,b.append(old,changes));self.assertEqual(b.sha(new),self.p['profiles'][p]['sha256'])
   self.assertEqual(moved,self.p['profiles'][p]['relocated']);self.assertEqual(refs,self.p['profiles'][p]['external_refs_rewritten'])
 def test_sources_disjoint(self):
  ranges=[(int(e['id'],16),int(e['end'],16)) for e in self.f['scripts']]
  self.assertTrue(all(a<z for a,z in ranges))
  self.assertTrue(all(z<=c for (_,z),(c,_) in zip(ranges,ranges[1:])))
 def test_exhaustion(self):
  old=b.RESERVES
  try:
   b.RESERVES=((0x320000,0x320001),)
   with self.assertRaises(ValueError):b.additions_from_fixtures(self.f,'accents')
  finally:b.RESERVES=old
 def test_fragmented_reserve_reuses_earlier_hole(self):
  old=b.RESERVES
  def entry(i,n):return {'id':f'{0x2000+i*0x100:06X}','end':f'{0x2000+i*0x100+2:06X}','original_hex':'7102','spans':[[0,1]],'fr':['A'*(n-1)],'references':[]}
  try:
   b.RESERVES=((0x10000,0x10010),(0x20000,0x2000C))
   changes,moved,_=b.additions_from_fixtures({'scripts':[entry(i,n) for i,n in enumerate((12,8,4,4))]},'accents')
   self.assertEqual([(p,len(v)) for p,v in changes],[(0x10000,12),(0x20000,8),(0x1000C,4),(0x20008,4)])
  finally:b.RESERVES=old
 def test_text_interior_alias_is_rejected(self):
  f={'scripts':[{'id':'002000','end':'002004','original_hex':'71727302','spans':[[0,3]],'fr':['Texte'],'references':[{'offset':'001000','target':'002001','proof':{}}]}]}
  with self.assertRaisesRegex(ValueError,'Alias au milieu du texte'):b.additions_from_fixtures(f,'accents')
 def test_adjacent_scripts_keep_separate_entry(self):
  f={'scripts':[{'id':'002000','end':'002002','original_hex':'7102','spans':[[0,1]],'fr':['A'],'references':[]},{'id':'002002','end':'002005','original_hex':'727302','spans':[[0,2]],'fr':['Une copie plus longue'],'references':[{'offset':'001000','target':'002002','proof':{}}]}]}
  changes,moved,_=b.additions_from_fixtures(f,'accents')
  target=next(int(e['offset'],16) for e in moved if e['id']=='002002')
  self.assertEqual(dict(changes)[0x1000],b.pointer(target))
 def test_nonlexical_and_menu_counts(self):
  self.assertEqual(self.p['dialogue_yes_no_choices_deferred_to_menu_pass'],0)
  self.assertEqual(self.p['private_helper_scripts'],4)
  self.assertFalse(self.p['shared_dictionary_modified'])
if __name__=='__main__':unittest.main()
