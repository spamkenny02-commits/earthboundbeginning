import collections,hashlib,importlib.util,json,os,struct,unittest
from pathlib import Path
from service_session import ROOT,b,operations_payload,prove
def probe():
 spec=importlib.util.spec_from_file_location('v69_probe',ROOT/'tests/emulation_v69/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def reports():
 return [(p,json.loads((ROOT/f'tests/emulation_v69/results_{p}.json').read_text())) for p in ('accents','ascii')]
class OfflineTests(unittest.TestCase):
 def test_native_operations_are_strict(self):
  self.assertEqual(operations_payload([('give',0x70),('take',0x70),('store',0x70)]),bytes.fromhex('1d0001701d0101701d187000'))
  for ops in ([('give',1)]*14,[('other',1)],[('give',0)],[('take',256)],[('give','1')]):
   with self.assertRaises(AssertionError):operations_payload(ops)
 def test_v67_patch_unchanged_no_duplicate_ips(self):
  hashes={'accents':'2f5a01f32dc9d431f3e81531fff4f539ef0002dbf2779206b8e1067c7586b277','ascii':'73a636a494601452264791e18390adbb5433c5ac4b743ee9409d88e637047119'}
  for p,h in hashes.items():self.assertEqual(b.sha((ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes()),h)
  self.assertFalse(list((ROOT/'patches').glob('*v69*')))
 def test_phase_links_and_declared_fixtures(self):
  m=probe();plan=json.loads((ROOT/'tools/v67/validation_v67.json').read_text())
  for p,r in reports():
   self.assertEqual(r['patch_tested'],'v67');self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(list(r['phases']),list(m.PHASES));previous=None;sha=r['initial_state_sha256']
   for name,c in r['phases'].items():
    cfg=m.PHASES[name];self.assertEqual(c['operations'],[list(x) for x in cfg['operations']]);self.assertEqual(c['trigger'],cfg['trigger']);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['input_state_sha256'],sha);self.assertEqual(c['state_source'],previous or 'initial_v33');self.assertEqual(c['returncode'],0);self.assertEqual(c['base_rom_sha256'],plan['profiles'][p]['target_rom_sha256']);self.assertEqual(c['entries'],[f'{a:06X}' for a in cfg['entries']])
    payload=operations_payload(cfg['operations'])+b''.join(b'\x08'+b.pointer(a) for a in cfg['entries'])+b'\x02';self.assertLessEqual(len(payload),64);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}]);sha=c['output_state_sha256'];previous=name
    if name!='exercise':self.assertEqual(len(sha),64)
    else:self.assertIsNone(sha)
 def test_live_trace_counts(self):
  for p,r in reports():
   for c in r['phases'].values():
    events=c['events'];self.assertTrue(events);counts=collections.Counter()
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1;self.assertGreater(stop,e['sample'])
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
 def test_captures_integrity_and_no_private_files(self):
  count=0
  for p,r in reports():
   for c in r['phases'].values():
    for cap in c['captures']:
     path=ROOT/cap['path'];self.assertTrue(path.resolve().is_relative_to((ROOT/'tests/emulation_v69').resolve()));raw=path.read_bytes();self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',raw[16:24]),(256,224));self.assertEqual(hashlib.sha256(raw).hexdigest(),cap['artifact_png_sha256']);count+=1
  self.assertEqual(count,50)
  for path in (ROOT/'tests/emulation_v69').rglob('*'):
   if path.is_file():self.assertNotIn(path.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.wram','.dmp'))
class RomTests(unittest.TestCase):
 def test_fixture_hashes_and_unmodified_engine(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA)
  for p,r in reports():
   base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes()))
   for c in r['phases'].values():
    fixture=bytearray(base)
    for write in c['temporary_rom_writes']:
     a=int(write['offset'],16);raw=bytes.fromhex(write['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256']);prove(fixture);self.assertEqual(b.sprite_digest(base),b.sprite_digest(fixture));self.assertEqual(base[0x250000:0x260000],fixture[0x250000:0x260000])
if __name__=='__main__':unittest.main()
