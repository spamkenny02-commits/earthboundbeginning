import json,os,unittest
from pathlib import Path
import build_v61 as b
@unittest.skipUnless(os.environ.get('ROM_PATH'),'ROM_PATH required')
class ROM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=Path(os.environ['ROM_PATH']).read_bytes();cls.f=json.loads((b.ROOT/'tools/v61/v61_fixtures.json').read_text());cls.plan=json.loads((b.ROOT/'tools/v61/validation_v61.json').read_text());cls.priors={p:(b.ROOT/f'patches/EarthBound_Beginnings_FR_v60_{p}.ips').read_bytes() for p in ('accents','ascii')};cls.bases={p:b.apply(cls.source,b.records(v)) for p,v in cls.priors.items()};cls.targets={p:b.apply(cls.source,b.records((b.ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes())) for p in cls.bases}
 def test_reproducible_fixture(self):self.assertEqual(b.fixtures(self.source,self.bases),self.f)
 def test_targets_sizes_shas_and_only_declared_text_bytes_change(self):
  for p,target in self.targets.items():
   self.assertEqual(len(target),b.SIZE);self.assertEqual(b.sha(target),self.plan['profiles'][p]['target_rom_sha256']);self.assertEqual(target,b.apply(self.bases[p],b.additions(self.f,p)));mask=bytearray(b.SIZE)
   for a,raw in b.additions(self.f,p):mask[a:a+len(raw)]=b'\1'*len(raw)
   self.assertFalse(any(x!=y and not m for x,y,m in zip(self.bases[p],target,mask)))
 def test_all_commands_branch_operands_and_waits_preserved(self):
  for p,target in self.targets.items():
   for root,c in self.f['contexts'].items():
    a,z=int(root,16),int(c[p]['end'],16);self.assertEqual(b.commands(target[a:z]),b.commands(bytes.fromhex(c[p]['baseline_hex'])))
 def test_timed_huées_join_correctly_at_original_command_boundaries(self):
  for root,start in b.BOOS:
   for p,target in self.targets.items():
    z=int(self.f['contexts'][root][p]['end'],16);parts=b.spans_fr(target[start:z]);self.assertEqual(''.join(b.decode(target[start+a:start+e],b.dictionary_from_rom(self.source)) for a,e in parts),'@Bouhouuuu!')
 def test_sprite_data_credits_and_npc_table_preserved(self):
  for p,target in self.targets.items():
   self.assertEqual(b.sprite_digest(target),b.sprite_digest(self.bases[p]));self.assertEqual(target[0x17FBE8:0x17FFEA],self.bases[p][0x17FBE8:0x17FFEA]);self.assertEqual(target[0x2021A8:0x2021A8+1584*17],self.bases[p][0x2021A8:0x2021A8+1584*17])
 def test_reject_wrong_rom_and_damaged_source_fragment(self):
  with self.assertRaisesRegex(ValueError,'ROM originale'):b.fixtures(bytes(b.SIZE),self.bases)
  damaged=dict(self.bases);raw=bytearray(damaged['accents']);raw[0x34FAE0]^=1;damaged['accents']=raw
  with self.assertRaisesRegex(ValueError,'source divergent'):b.fixtures(self.source,damaged)
if __name__=='__main__':unittest.main()
