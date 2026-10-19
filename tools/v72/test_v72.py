import collections,hashlib,importlib.util,json,os,struct,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import b,operations_payload,prove
def reports():return [(p,json.loads((ROOT/f'tests/emulation_v72/results_{p}.json').read_text())) for p in ('accents','ascii')]
def probe():
 spec=importlib.util.spec_from_file_location('probe72',ROOT/'tests/emulation_v72/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class OfflineTests(unittest.TestCase):
 def test_v71_patch_unchanged_no_v72_ips(self):
  hashes={'accents':'0290365376b20e6b77bd4bce12839f7378bd34c0431f36fad3dee19b852ed0a6','ascii':'4969ab315e6df24d9d4ef3bb47caac7f67c755d855d4c236c9f64402e20bdb68'}
  for p,h in hashes.items():self.assertEqual(b.sha((ROOT/f'patches/EarthBound_Beginnings_FR_v71_{p}.ips').read_bytes()),h)
  self.assertFalse(list((ROOT/'patches').glob('*v72*')))
 def test_state_chain_and_preparations(self):
  m=probe();plan=json.loads((ROOT/'tools/v71/validation_v71.json').read_text())
  for p,r in reports():
   self.assertEqual(set(r['cases']),set(m.CASES));self.assertEqual(r['patch_tested'],'v71');self.assertFalse(r['courier_script_called_by_tester']);self.assertFalse(r['natural_initial_phone_access_verified']);self.assertTrue(r['storage_inspection_access_forced']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    phases=c['phases'];self.assertEqual(list(phases),['courier','inspect']);first=phases['courier'];last=phases['inspect'];self.assertEqual(first['input_state_sha256'],r['initial_state_sha256']);self.assertEqual(len(first['output_state_sha256']),64);self.assertEqual(last['input_state_sha256'],first['output_state_sha256']);self.assertIsNone(last['output_state_sha256']);self.assertEqual(last['operations'],[['take',1]] if name!='pickup_three' else [])
    for phase,data in phases.items():
     entry=0x35C597 if phase=='courier' else 0x34B490;ops=m.CASES[name]['operations'] if phase=='courier' else [('take',1)] if name!='pickup_three' else [];self.assertEqual(data['operations'],[list(x) for x in ops]);self.assertEqual(data['entries'],[f'{entry:06X}']);self.assertEqual(data['returncode'],0);self.assertEqual(data['base_rom_sha256'],plan['profiles'][p]['target_rom_sha256']);self.assertEqual(data['trigger'],m.TRIGGER+(['A'] if phase=='inspect' and name!='pickup_three' else []));self.assertEqual(data['steps'],m.CASES[name]['phone'] if phase=='courier' else m.INSPECT)
     payload=operations_payload(ops)+b'\x08'+b.pointer(entry)+b'\x02';self.assertLessEqual(len(payload),64);self.assertEqual(data['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}])
 def test_controller_courier_and_storage_branches_reached(self):
  m=probe()
  for p,r in reports():
   for name,c in r['cases'].items():
    first=c['phases']['courier'];last=c['phases']['inspect'];self.assertEqual(first['courier_steps'],m.CASES[name]['courier']);self.assertEqual(first['wait_after_phone_frames'],600);self.assertGreater(first['pointer_frame_counts'].get('063EE5' if name=='pickup_three' else '0642BF',0),100);self.assertGreater(last['pointer_frame_counts'].get('32C7E2',0),100);self.assertEqual(last['captures'][-1]['path'].split('/')[-1],'page_03.png')
 def test_live_trace_counts(self):
  for p,r in reports():
   for c in r['cases'].values():
    for data in c['phases'].values():
     counts=collections.Counter();events=data['events']
     for i,e in enumerate(events):
      stop=events[i+1]['sample'] if i+1<len(events) else data['sampled_frames']+1;self.assertGreater(stop,e['sample'])
      if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
     self.assertEqual(dict(counts),data['pointer_frame_counts'])
 def test_png_integrity_and_private_files_absent(self):
  count=0
  for p,r in reports():
   for c in r['cases'].values():
    for data in c['phases'].values():
     for cap in data['captures']:
      path=ROOT/cap['path'];self.assertTrue(path.resolve().is_relative_to((ROOT/'tests/emulation_v72').resolve()));raw=path.read_bytes();self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',raw[16:24]),(256,224));self.assertEqual(hashlib.sha256(raw).hexdigest(),cap['artifact_png_sha256']);count+=1
  self.assertEqual(count,174)
  for f in (ROOT/'tests/emulation_v72').rglob('*'):
   if f.is_file():self.assertNotIn(f.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.wram','.dmp'))
class RomTests(unittest.TestCase):
 def test_fixture_hashes_engine_and_sprites(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA)
  for p,r in reports():
   base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v71_{p}.ips').read_bytes()))
   for c in r['cases'].values():
    for data in c['phases'].values():
     fixture=bytearray(base)
     for write in data['temporary_rom_writes']:
      a=int(write['offset'],16);raw=bytes.fromhex(write['hex']);fixture[a:a+len(raw)]=raw
     self.assertEqual(b.sha(fixture),data['fixture_rom_sha256']);prove(fixture);self.assertEqual(b.sprite_digest(fixture),b.sprite_digest(base));self.assertEqual(fixture[0x250000:0x260000],base[0x250000:0x260000])
if __name__=='__main__':unittest.main()
