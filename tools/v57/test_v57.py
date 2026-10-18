import json,os,unittest
from pathlib import Path
import build_v57 as b
ROOT=b.ROOT
@unittest.skipUnless(os.environ.get('ROM_PATH'),'ROM_PATH required')
class ROM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=Path(os.environ['ROM_PATH']).read_bytes();cls.f=json.loads((ROOT/'tools/v57/v57_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v57/validation_v57.json').read_text());cls.priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v56_{p}.ips').read_bytes() for p in ('accents','ascii')};cls.bases={p:b.apply(cls.source,b.records(v)) for p,v in cls.priors.items()};cls.targets={p:b.apply(cls.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v57_{p}.ips').read_bytes())) for p in cls.bases}
 def test_reproducible_fixtures(self):
  self.assertEqual(b.fixtures_from_baselines(self.source,self.bases,self.priors),self.f)
  refs=sorted(set(b.pointer_index(self.source))|set().union(*(set(b.pointer_index(d)) for d in self.bases.values())))
  self.assertEqual(self.f['reserves'],[[f'{a:06X}',f'{z:06X}'] for a,z in b.free_reserves(self.source,self.bases,self.priors,refs)])
 def test_target_sha_size_roundtrip(self):
  for p,target in self.targets.items():
   self.assertEqual(len(target),b.SIZE);self.assertEqual(b.sha(target),self.plan['profiles'][p]['target_rom_sha256']);self.assertEqual(target,b.apply(self.bases[p],b.additions_from_fixtures(self.f,p)))
 def test_interior_entries_and_literal_sites_unchanged(self):
  indexes=[b.pointer_index(self.source)]+[b.pointer_index(d) for d in self.bases.values()]
  for p,target in self.targets.items():
   base=self.bases[p]
   for e in self.f['edits']:
    a,z=int(e['offset'],16),int(e['end'],16);self.assertEqual(target[a+5:z],base[a+5:z])
    for t in e['interior_targets']:
     t=int(t,16);self.assertGreaterEqual(t,a+5);self.assertEqual(target[t:z],base[t:z])
     for idx in indexes:
      for q in idx.get(t,[]):self.assertEqual(target[q:q+4],base[q:q+4])
 def test_complete_linear_command_streams_preserved(self):
  for p,target in self.targets.items():
   for root,c in self.f['contexts'].items():self.assertEqual(b.context_commands(b.logical_context(target,self.f,root,p)),b.context_commands(bytes.fromhex(c[p]['baseline_hex'])))
 def test_actual_entry_copy_and_return_for_every_text_run(self):
  for p,target in self.targets.items():
   for e in self.f['edits']:
    a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16);raw=b.copy_text(e,p)+b'\x0a'+b.pointer(int(e['end'],16))
    self.assertEqual(target[a:a+5],b'\x0a'+b.pointer(d));self.assertEqual(target[d:d+len(raw)],raw);self.assertEqual(raw[-5:],b'\x0a'+b.pointer(z))
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
 def test_shared_dictionary_and_npc_table_unchanged(self):
  for p,target in self.targets.items():
   self.assertEqual(b.dictionary_from_rom(target),b.dictionary_from_rom(self.bases[p]));self.assertEqual(target[0x2021A8:0x2021A8+1584*17],self.bases[p][0x2021A8:0x2021A8+1584*17])
   for v in (54,55):
    menus=json.loads((ROOT/f'tools/v{v}/v{v}_fixtures.json').read_text())
    for e in menus['edits']:
     a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
     self.assertEqual(target[a:z],self.bases[p][a:z]);self.assertEqual(target[d:d+e['capacity']],self.bases[p][d:d+e['capacity']])
 def test_reject_wrong_rom(self):
  with self.assertRaisesRegex(ValueError,'ROM originale'):b.fixtures_from_baselines(bytes(b.SIZE),self.bases,self.priors)
 def test_reject_damaged_entry_copy_and_tail(self):
  e=self.f['edits'][0];a,d=int(e['offset'],16),int(e['copy_offset'],16)
  for q,reason in ((a,'Trajet'),(d,'Trajet'),(a+5,'intérieure')):
   target=bytearray(self.targets['accents']);target[q]^=1
   with self.assertRaisesRegex(ValueError,reason):b.logical_context(target,self.f,e['context'],'accents')
 def test_scoped_possessive_call_only_in_private_copy(self):
  e=next(e for e in self.f['edits'] if e.get('possessive_call'))
  for p,target in self.targets.items():
   raw=b.copy_text(e,p);refs=b.parse(raw+b'\x02',0,len(raw)+2,extra_glyphs=range(0xB0,0xC0))['refs']
   self.assertEqual([t for q,t in refs],[b.GRAMMAR_NEW]);self.assertEqual(raw[refs[0][0]-1],0x08)
   self.assertEqual(target[b.GRAMMAR_NEW:b.GRAMMAR_NEW+16],bytes.fromhex(b.GRAMMAR_HEX));self.assertEqual(target[0x07E660:0x07E66E],self.bases[p][0x07E660:0x07E66E])
   self.assertEqual(b.context_commands(raw+b'\x02'),b.commands(bytes.fromhex(e['profiles'][p]['baseline_hex'])+b'\x02'))
 def test_all_sprite_tables_headers_and_frames_unchanged(self):
  for p,target in self.targets.items():self.assertEqual(b.sprite_digest(target),b.sprite_digest(self.bases[p]))
  self.assertEqual(self.f['storage']['sprite_frames'],4177)
if __name__=='__main__':unittest.main()
