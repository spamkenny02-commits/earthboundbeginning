import json,os,unittest
from pathlib import Path
import build_v53 as b
ROOT=b.ROOT
@unittest.skipUnless(os.environ.get('ROM_PATH'),'ROM_PATH required')
class ROM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=Path(os.environ['ROM_PATH']).read_bytes();cls.f=json.loads((ROOT/'tools/v53/v53_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v53/validation_v53.json').read_text())
  cls.priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v52_{p}.ips').read_bytes() for p in ('accents','ascii')};cls.bases={p:b.apply(cls.source,b.records(v)) for p,v in cls.priors.items()};cls.targets={p:b.apply(cls.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v53_{p}.ips').read_bytes())) for p in cls.bases}
 def test_reproducible_fixtures(self):self.assertEqual(b.fixtures_from_baselines(self.source,self.bases,self.priors),self.f)
 def test_target_sha_size_roundtrip(self):
  for p,target in self.targets.items():
   self.assertEqual(len(target),b.SIZE);self.assertEqual(b.sha(target),self.plan['profiles'][p]['target_rom_sha256']);self.assertEqual(target,b.apply(self.bases[p],b.additions_from_fixtures(self.f,p)))
 def test_npc_sources_entirely_unchanged(self):
  for e in self.f['edits']:
   if e['mode']=='npc_copy':
    a,z=int(e['id'],16),int(e['end'],16)
    for p,target in self.targets.items():self.assertEqual(target[a:z],self.bases[p][a:z])
 def test_all_interior_reference_sites_and_other_start_sites_preserved(self):
  for e in self.f['edits']:
   for p,target in self.targets.items():
    for r in e['preserved_interior_refs']:
     t=int(r['target'],16);z=int(e['end'],16);self.assertEqual(target[t:z],self.bases[p][t:z])
     for q in r['sites']:
      q=int(q,16);self.assertEqual(target[q:q+4],self.bases[p][q:q+4])
    for q in e.get('other_start_ref_sites',[]):
     q=int(q,16);self.assertEqual(target[q:q+4],self.bases[p][q:q+4])
 def test_npc_destinations_exact_copies(self):
  for e in self.f['edits']:
   if e['mode']!='npc_copy':continue
   q,d=int(e['slot'],16),int(e['copy_offset'],16)
   for p,target in self.targets.items():
    self.assertEqual(target[q:q+4],b.pointer(d));out=b.copy_bytes(e,p);self.assertEqual(target[d:d+len(out)],out)
 def test_current_engine_bindings_identical(self):
  for target in self.targets.values():self.assertEqual(b.engine_table_proof(target,self.f['config']),self.f['engine_proof'])
 def test_prefix_jump_returns_to_original_shop_command(self):
  e=next(e for e in self.f['edits'] if e['mode']=='text_jump');a,z,d=int(e['id'],16),int(e['end'],16),int(e['copy_offset'],16);root=int(e['context'],16)
  for p,target in self.targets.items():
   base=self.bases[p];end=int(e['context_end'],16);self.assertEqual(target[a:a+5],b'\x0a'+b.pointer(d));self.assertEqual(b.copy_bytes(e,p),b.encode('@Objet: ',p)+b'\x0a'+b.pointer(z));self.assertEqual(target[z:end],base[z:end])
   logical=target[root:a]+b.encode(e['fr'],p)+target[z:end];self.assertEqual(b.commands(logical),b.commands(base[root:end]))
 def test_previous_v35_continuation_preserved(self):
  e=next(e for e in self.f['edits'] if e['id']=='3609EB')
  for p,target in self.targets.items():
   self.assertEqual(target[0x360A16:0x360A1A],b.pointer(0x16F920));self.assertIn(0x16F920,b.parse(b.copy_bytes(e,p),0,256,extra_glyphs=range(0xB0,0xC0))['targets'])
 def test_outside_declared_writes_unchanged(self):
  for p,target in self.targets.items():
   mask=bytearray(b.SIZE)
   for a,v in b.additions_from_fixtures(self.f,p):mask[a:a+len(v)]=b'\1'*len(v)
   self.assertFalse(any(x!=y and not m for x,y,m in zip(self.bases[p],target,mask)))
 def test_reserves_zero_unreferenced_not_prior_records(self):
  refs=set(b.pointer_index(self.source))|set().union(*(set(b.pointer_index(d)) for d in self.bases.values()))
  for e in self.f['edits']:
   a=int(e['copy_offset'],16);z=a+e['capacity'];self.assertFalse(refs.intersection(range(a,z)))
   for p,base in self.bases.items():
    self.assertEqual(self.source[a:z],bytes(z-a));self.assertEqual(base[a:z],bytes(z-a));self.assertFalse(any(q<z and q+len(raw)>a for q,raw in b.records(self.priors[p])))
 def test_shared_dictionary_unchanged(self):
  for p,target in self.targets.items():self.assertEqual(b.dictionary_from_rom(target),b.dictionary_from_rom(self.bases[p]))
 def test_reject_wrong_rom(self):
  with self.assertRaisesRegex(ValueError,'ROM originale'):b.fixtures_from_baselines(bytes(b.SIZE),self.bases,self.priors)
 def test_reject_unlisted_source_changes(self):
  bases=dict(self.bases);data=bytearray(bases['accents']);data[0x3609EC]^=1;bases['accents']=data
  with self.assertRaisesRegex(ValueError,'Source déjà'):b.fixtures_from_baselines(self.source,bases,self.priors)
if __name__=='__main__':unittest.main()
