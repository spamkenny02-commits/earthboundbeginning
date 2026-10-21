import importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
from locker_stage import qualification,ENTRIES
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload
def read(path):return json.loads((ROOT/path).read_text())
class LockerOffline(unittest.TestCase):
 def test_controller_paths_and_native_preparation(self):
  from verify_remaining import verify
  result=verify(ROOT/'tests/emulation_v78_lockers');self.assertEqual(result['pairs'],108)
  spec=importlib.util.spec_from_file_location('locker78',ROOT/'tests/emulation_v78_lockers/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  self.assertEqual(operations_payload([('warp',0xD1)]),bytes.fromhex('1f21d1'))
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_lockers/results_{p}.json');self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['locker_script_called_by_tester']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(list(r['cases']),list(m.CASES))
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['entries'],['38B550']);self.assertEqual(c['npc'],cfg['npc']);self.assertEqual(c['steps'],m.actions(cfg));self.assertEqual(c['trigger'],m.TRIGGER);self.assertEqual(c['wait_after_preparation_frames'],600);self.assertEqual(c['returncode'],0)
    operations=[['give',cfg['item']]]+[['give',1]]*cfg['badges']+[['warp',0xD1]];self.assertEqual(c['operations'],operations);payload=operations_payload(operations)+b'\x08'+b.pointer(0x38B550)+b'\x02';self.assertLessEqual(len(payload),64)
    self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}])
    a,z={'pickup':(0x06FA2E,0x06FA68),'empty':(0x06FA93,0x06FAB4),'bent':(0x06FA68,0x06FA93),'full':(0x06FAB4,0x06FAE5)}[name];self.assertTrue(any(a<=int(ptr,16)<z for ptr in c['pointer_frame_counts']))
  for path in (ROOT/'tests/emulation_v78_lockers').rglob('*'):
   if path.is_file() and '__pycache__' not in path.parts:self.assertIn(path.suffix.lower(),('.py','.json','.png'))
class LockerRom(unittest.TestCase):
 def test_placed_npcs_exact_changes_and_capture_fixtures(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);f=read('tools/v78/v78_fixtures.json')['locker'];self.assertEqual(qualification(source),f['qualification']);self.assertEqual(len(ENTRIES),9)
  for p in ('accents','ascii'):
   records=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes());cut=len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()))+f['profiles'][p]['input_records_added'];base=b.apply(source,records[:cut]);target=b.apply(source,records[:len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()))+read('tools/v78/v78_fixtures.json')['locker_help']['profiles'][p]['input_records_added']]);writes=[(int(w['offset'],16),bytes.fromhex(w['hex'])) for w in f['profiles'][p]['records']];self.assertEqual(len(writes),9);self.assertEqual(b.apply(base,writes),target);self.assertEqual(b.sha(base),f['profiles'][p]['input_rom_sha256'])
   for root in set(int(e[0],16) for e in ENTRIES):
    q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));self.assertTrue(q['terminal']);self.assertFalse(q['error']);self.assertEqual(b.commands(base[root:q['end']]),b.commands(target[root:q['end']]))
   self.assertEqual(b.sprite_digest(base),b.sprite_digest(target))
   for c in read(f'tests/emulation_v78_lockers/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(target),c['base_rom_sha256']);fixture=bytearray(target)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
