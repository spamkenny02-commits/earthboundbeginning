import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload
def read(path):return json.loads((ROOT/path).read_text())
class PartyOffline(unittest.TestCase):
 def test_native_count_paths_inputs_and_images(self):
  from verify_remaining import verify
  self.assertEqual(verify(ROOT/'tests/emulation_v78_party'),{'pairs':56,'changed_text_only':8,'sampled_frames':11728})
  spec=importlib.util.spec_from_file_location('party78',ROOT/'tests/emulation_v78_party/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  self.assertEqual(operations_payload([('join',2),('join',3)]),bytes.fromhex('1f11021f1103'))
  with self.assertRaises(AssertionError):operations_payload([('join',5)])
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_party/results_{p}.json');self.assertEqual(list(r['cases']),list(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['entries'],[f'{cfg["entry"]:06X}']);self.assertEqual(c['scope'],cfg['scope']);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['trigger'],m.m.TRIGGER);self.assertEqual(c['operations'],[list(v) for v in cfg['operations']]);self.assertEqual(c['returncode'],0);payload=operations_payload(c['operations'])+b'\x08'+b.pointer(cfg['entry'])+b'\x02';self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}]);counts=collections.Counter()
    for i,e in enumerate(c['events']):
     stop=c['events'][i+1]['sample'] if i+1<len(c['events']) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
   for name,expected,other in [('mother_two','387B37','387B2F'),('mother_three','387B2F','387B37')]:
    counts=r['cases'][name]['pointer_frame_counts'];self.assertIn(expected,counts);self.assertNotIn(other,counts)
  for path in (ROOT/'tests/emulation_v78_party').rglob('*'):
   if path.is_file() and '__pycache__' not in path.parts:self.assertIn(path.suffix.lower(),('.py','.json','.png'))
class PartyRom(unittest.TestCase):
 def test_native_recruitment_command_and_exact_fixtures(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA)
  for p in ('accents','ascii'):
   records=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes());cut=len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()))+read('tools/v78/v78_fixtures.json')['locker']['profiles'][p]['input_records_added'];data=b.apply(source,records[:cut]);q=b.parse(data,0x36E6DF,8192,extra_glyphs=range(0xb0,0xc0));self.assertTrue(q['terminal']);self.assertFalse(q['error']);self.assertIn(bytes.fromhex('1f1102'),b.commands(data[0x36E6DF:q['end']]))
   for c in read(f'tests/emulation_v78_party/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(data),c['base_rom_sha256']);fixture=bytearray(data)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
