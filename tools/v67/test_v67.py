import collections,hashlib,importlib.util,json,struct,unittest
from build_v67 import ROOT,b,CONFIG,CONTEXT
class OfflineTests(unittest.TestCase):
 def test_reject_invalid_native_preparations(self):
  from service_session import ServiceSession
  for items in ([-1],[256],['1'],[1]*14):
   with self.assertRaises(AssertionError):ServiceSession(None,None,None,None,[],seed_items=items)
 def test_exact_patch_scope(self):
  plan=json.loads((ROOT/'tools/v67/validation_v67.json').read_text());f=json.loads((ROOT/'tools/v67/v67_fixtures.json').read_text())
  for p in ('accents','ascii'):
   prior=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v66_{p}.ips').read_bytes());ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes();r=b.records(ips);self.assertEqual(b.sha(ips),plan['profiles'][p]['sha256']);self.assertEqual(r[:len(prior)],prior)
   self.assertEqual(r[len(prior):],[(int(x['offset'],16),bytes.fromhex(x['replacement_hex'])) for x in f['profiles'][p]])
   self.assertEqual([a for a,_ in r[len(prior):]],[0x37BBB0,0x37BBBB])
 def test_controller_and_trace_proofs(self):
  spec=importlib.util.spec_from_file_location('v67_probe',ROOT/'tests/emulation_v67/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);plan=json.loads((ROOT/'tools/v67/validation_v67.json').read_text())
  for p in ('accents','ascii'):
   r=json.loads((ROOT/f'tests/emulation_v67/results_{p}.json').read_text());self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(set(r['cases']),set(m.CASES))
   for name,c in r['cases'].items():
    entries,seed,steps=m.CASES[name];self.assertEqual(c['steps'],steps);self.assertEqual(c['seed_items'],seed);self.assertEqual(c['entries'],[f'{a:06X}' for a in entries]);self.assertEqual(c['returncode'],0);self.assertEqual(c['base_rom_sha256'],plan['profiles'][p]['target_rom_sha256']);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':(b''.join(bytes((0x1D,0,1,item)) for item in seed)+b''.join(b'\x08'+b.pointer(a) for a in entries)+b'\x02').hex()}])
    counts=collections.Counter();events=c['events']
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1;self.assertGreater(stop,e['sample'])
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
 def test_png_integrity(self):
  count=0
  for p in ('accents','ascii'):
   r=json.loads((ROOT/f'tests/emulation_v67/results_{p}.json').read_text())
   for c in r['cases'].values():
    for cap in c['captures']:
     raw=(ROOT/cap['path']).read_bytes();self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',raw[16:24]),(256,224));self.assertEqual(hashlib.sha256(raw).hexdigest(),cap['artifact_png_sha256']);count+=1
  self.assertEqual(count,86)
 def test_reference_integrity_and_bounds(self):
  r=json.loads((ROOT/'tests/emulation_v67/comparison_v66.json').read_text());count=0
  for p,c in r.items():
   self.assertTrue(c['same_controller_inputs'])
   for x in c['comparisons']:
    self.assertEqual(hashlib.sha256((ROOT/x['before_path']).read_bytes()).hexdigest(),x['before_png_sha256']);self.assertTrue(x['only_text_window_changed']);count+=1
    if x['bbox']:
     a,y,z,t=x['bbox'];self.assertGreaterEqual(a,104);self.assertGreaterEqual(y,8);self.assertLessEqual(z,248);self.assertLessEqual(t,98)
  self.assertEqual(count,86)
class RomTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import os
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:raise unittest.SkipTest('Private ROM not supplied')
  cls.source=__import__('pathlib').Path(path).read_bytes();assert b.sha(cls.source)==b.ROM_SHA
 def test_commands_unchanged(self):
  for p in ('accents','ascii'):
   a=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v66_{p}.ips').read_bytes()));z=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes()));end=b.parse(a,CONTEXT,8192,extra_glyphs=range(0xB0,0xC0))['end'];self.assertEqual(b.commands(a[CONTEXT:end]),b.commands(z[CONTEXT:end]))
 def test_sprites_and_bank25_unchanged(self):
  for p in ('accents','ascii'):
   a=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v66_{p}.ips').read_bytes()));z=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes()));self.assertEqual(b.sprite_digest(a),b.sprite_digest(z));self.assertEqual(a[0x250000:0x260000],z[0x250000:0x260000])
 def test_target_hashes(self):
  plan=json.loads((ROOT/'tools/v67/validation_v67.json').read_text())
  for p in ('accents','ascii'):self.assertEqual(b.sha(b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes()))),plan['profiles'][p]['target_rom_sha256'])
if __name__=='__main__':unittest.main()
