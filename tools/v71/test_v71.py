import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v71 import ROOT,b,CONFIG
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload,prove
def reports():return [(p,json.loads((ROOT/f'tests/emulation_v71/results_{p}.json').read_text())) for p in ('accents','ascii')]
class OfflineTests(unittest.TestCase):
 def test_exact_patch_records_and_prefix(self):
  plan=json.loads((ROOT/'tools/v71/validation_v71.json').read_text());fixtures=json.loads((ROOT/'tools/v71/v71_fixtures.json').read_text())
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v70_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v71_{p}.ips').read_bytes();self.assertTrue(new.startswith(old[:-3]));self.assertEqual(b.sha(new),plan['profiles'][p]['sha256']);records=b.records(new)[len(b.records(old)):];self.assertEqual(len(records),32)
   for (a,data),f,cfg in zip(records,fixtures['profiles'][p],CONFIG):
    self.assertEqual(a,cfg[1]);self.assertEqual(data.hex(),f['replacement_hex']);self.assertEqual(len(data),cfg[2]-cfg[1]);self.assertEqual(f['english'],cfg[3]);self.assertEqual(f['french'],cfg[4])
 def test_declared_native_preparation_and_controller_sequences(self):
  spec=importlib.util.spec_from_file_location('probe71',ROOT/'tests/emulation_v71/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p,r in reports():
   self.assertTrue(r['initial_phone_access_forced']);self.assertFalse(r['courier_script_called_by_tester']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(set(r['cases']),set(m.CASES))
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['operations'],[list(x) for x in m.operations(cfg)]);self.assertEqual(c['phone_steps'],m.phone_steps());self.assertEqual(c['courier_steps'],cfg['courier']);self.assertEqual(c['returncode'],0);self.assertEqual(c['entries'],['35C597']);self.assertEqual(c['wait_after_phone_frames'],600)
    payload=operations_payload(m.operations(cfg))+b'\x08'+b.pointer(0x35C597)+b'\x02';self.assertLessEqual(len(payload),64);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}]);self.assertGreater(c['pointer_frame_counts'].get('063EE5',0),100)
    self.assertEqual(c['inventory_trigger'],['A','Right','A','A'] if name=='pickup_three' else [])
 def test_live_trace_counts(self):
  for p,r in reports():
   for c in r['cases'].values():
    counts=collections.Counter();events=c['events']
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1;self.assertGreater(stop,e['sample'])
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
class RomTests(unittest.TestCase):
 def test_text_boundaries_commands_sprites_and_hashes(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);plan=json.loads((ROOT/'tools/v71/validation_v71.json').read_text());dic=b.dictionary_from_rom(source)
  for p,r in reports():
   old=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v70_{p}.ips').read_bytes()));base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v71_{p}.ips').read_bytes()));self.assertEqual(b.sha(base),plan['profiles'][p]['target_rom_sha256']);self.assertEqual(b.sprite_digest(base),b.sprite_digest(old));self.assertEqual(base[0x250000:0x260000],old[0x250000:0x260000])
   for root,a,z,en,fr in CONFIG:
    end=b.parse(old,root,8192,extra_glyphs=range(0xB0,0xC0))['end'];self.assertIn((a-root,z-root),b.spans_fr(old[root:end]));self.assertEqual(b.decode(old[a:z],dic),en);self.assertEqual(b.commands(old[root:end]),b.commands(base[root:end]))
   for c in r['cases'].values():
    fixture=bytearray(base)
    for write in c['temporary_rom_writes']:
     a=int(write['offset'],16);data=bytes.fromhex(write['hex']);fixture[a:a+len(data)]=data
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256']);prove(fixture)
if __name__=='__main__':unittest.main()
