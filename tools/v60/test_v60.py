import json,os,unittest
from pathlib import Path
import build_v60 as b
@unittest.skipUnless(os.environ.get('ROM_PATH'),'ROM_PATH required')
class ROM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=Path(os.environ['ROM_PATH']).read_bytes();cls.f=json.loads((b.ROOT/'tools/v60/v60_fixtures.json').read_text());cls.plan=json.loads((b.ROOT/'tools/v60/validation_v60.json').read_text());cls.priors={p:(b.ROOT/f'patches/EarthBound_Beginnings_FR_v59_{p}.ips').read_bytes() for p in ('accents','ascii')};cls.bases={p:b.apply(cls.source,b.records(v)) for p,v in cls.priors.items()};cls.targets={p:b.apply(cls.source,b.records((b.ROOT/f'patches/EarthBound_Beginnings_FR_v60_{p}.ips').read_bytes())) for p in cls.bases}
 def test_reproducible_fixture(self):self.assertEqual(b.fixtures(self.source,self.bases),self.f)
 def test_target_size_sha_and_autonomous_patch(self):
  for p,target in self.targets.items():
   self.assertEqual(len(target),b.SIZE);self.assertEqual(b.sha(target),self.plan['profiles'][p]['target_rom_sha256']);self.assertEqual(target,b.apply(self.bases[p],b.additions(self.f)))
 def test_only_credit_payload_changed_tail_and_all_other_bytes_preserved(self):
  n=self.f['translated_length']
  for p,target in self.targets.items():
   self.assertEqual(target[:b.START],self.bases[p][:b.START]);self.assertEqual(target[b.START+n:],self.bases[p][b.START+n:]);self.assertEqual(target[b.START+n-1],255)
 def test_names_spacing_player_name_and_height_preserved(self):
  old,h,n=b.decode_staff(self.source[b.START:b.START+b.CAPACITY]);indices={e['entry_index'] for e in self.f['titles']}
  for target in self.targets.values():
   new,h2,n=b.decode_staff(target[b.START:b.START+b.CAPACITY]);self.assertEqual(h,h2);self.assertEqual(len(old),len(new))
   for i,(a,z) in enumerate(zip(old,new)):
    if i not in indices:self.assertEqual(a,z)
 def test_sprites_and_credit_loader_height_operands_unchanged(self):
  for p,target in self.targets.items():
   self.assertEqual(b.sprite_digest(target),b.sprite_digest(self.bases[p]));self.assertEqual(target[b.POINTER_SITE:b.POINTER_SITE+12],bytes.fromhex(b.POINTER_HEX))
   for a in b.HEIGHT_SITES:self.assertEqual(int.from_bytes(target[a:a+2],'little'),1680)
 def test_reject_wrong_source_or_damaged_loader_and_height(self):
  with self.assertRaisesRegex(ValueError,'ROM originale'):b.fixtures(bytes(b.SIZE),self.bases)
  for offset,reason in ((b.POINTER_SITE,'Chargeur'),(b.HEIGHT_SITES[0],'Hauteur'),(b.START,'antérieur')):
   bases=dict(self.bases);data=bytearray(bases['accents']);data[offset]^=1;bases['accents']=data
   with self.assertRaisesRegex(ValueError,reason):b.fixtures(self.source,bases)
if __name__=='__main__':unittest.main()
