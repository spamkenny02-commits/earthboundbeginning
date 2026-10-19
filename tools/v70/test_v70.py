import collections,importlib.util,json,os,unittest
from pathlib import Path
from service_session import ROOT,b,operations_payload,prove
from build_v70 import CONFIG
def reports():
 return [(p,json.loads((ROOT/f'tests/emulation_v70/results_{p}.json').read_text())) for p in ('accents','ascii')]
class OfflineTests(unittest.TestCase):
 def test_strict_native_preparation(self):
  self.assertEqual(operations_payload([('spend',20),('store',112)]),bytes.fromhex('1d0914001d187000'))
  self.assertEqual(len(operations_payload([('give',1)]*14)),56)
  for ops in ([('give',1)]*15,[('spend',0)],[('spend',65536)],[('give',256)],[('give','1')]):
   with self.assertRaises(AssertionError):operations_payload(ops)
 def test_patch_prefix_and_exact_records(self):
  plan=json.loads((ROOT/'tools/v70/validation_v70.json').read_text());fixtures=json.loads((ROOT/'tools/v70/v70_fixtures.json').read_text())
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v70_{p}.ips').read_bytes()
   self.assertTrue(new.startswith(old[:-3]));self.assertEqual(b.sha(new),plan['profiles'][p]['sha256'])
   extra=b.records(new)[len(b.records(old)):];self.assertEqual(len(extra),24)
   for (a,data),f,cfg in zip(extra,fixtures['profiles'][p],CONFIG):
    self.assertEqual(a,cfg[1]);self.assertEqual(data.hex(),f['replacement_hex']);self.assertEqual(len(data),cfg[2]-cfg[1]);self.assertEqual(f['english'],cfg[3]);self.assertEqual(f['french'],cfg[4])
 def test_controller_scenarios_and_native_arrival(self):
  spec=importlib.util.spec_from_file_location('probe70',ROOT/'tests/emulation_v70/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p,r in reports():
   self.assertTrue(r['initial_phone_access_forced']);self.assertFalse(r['courier_script_called_by_tester']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(set(r['cases']),set(m.CASES))
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['operations'],[list(x) for x in m.operations(cfg)]);self.assertEqual(c['phone_steps'],m.phone_steps(len(cfg['items'])));self.assertEqual(c['courier_steps'],cfg['courier']);self.assertEqual(c['returncode'],0);self.assertEqual(c['entries'],['35C597'])
    payload=operations_payload(m.operations(cfg))+b'\x08'+b.pointer(0x35C597)+b'\x02';self.assertLessEqual(len(payload),64)
    self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}]);self.assertGreater(c['pointer_frame_counts'].get('0642BF',0),100)
 def test_live_counts(self):
  for p,r in reports():
   for c in r['cases'].values():
    counts=collections.Counter();events=c['events']
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
class RomTests(unittest.TestCase):
 def test_commands_sprites_and_fixture_hashes(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA)
  plan=json.loads((ROOT/'tools/v70/validation_v70.json').read_text())
  for p,r in reports():
   old=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v67_{p}.ips').read_bytes()));base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v70_{p}.ips').read_bytes()));self.assertEqual(b.sha(base),plan['profiles'][p]['target_rom_sha256']);self.assertEqual(b.sprite_digest(base),b.sprite_digest(old));self.assertEqual(base[0x250000:0x260000],old[0x250000:0x260000])
   for root in set(c[0] for c in CONFIG):
    end=b.parse(old,root,8192,extra_glyphs=range(0xB0,0xC0))['end'];self.assertEqual(b.commands(old[root:end]),b.commands(base[root:end]))
   for c in r['cases'].values():
    fixture=bytearray(base)
    for write in c['temporary_rom_writes']:
     a=int(write['offset'],16);data=bytes.fromhex(write['hex']);fixture[a:a+len(data)]=data
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256']);prove(fixture)
if __name__=='__main__':unittest.main()
