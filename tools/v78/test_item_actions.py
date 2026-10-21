import importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
from item_action_stage import LABELS,READER,READER_HEX
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload
def read(path):return json.loads((ROOT/path).read_text())
class ActionOffline(unittest.TestCase):
 def test_native_actions_inputs_and_public_evidence(self):
  from action_evidence import verify
  result=verify();self.assertEqual(result['pairs'],132);self.assertEqual(result['sampled_frames'],34084)
  spec=importlib.util.spec_from_file_location('actions78',ROOT/'tests/emulation_v78_actions/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_actions/results_{p}.json');self.assertEqual(list(r['cases']),list(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertFalse(r['target_scripts_called_directly_by_tester'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['entries'],['38B550']);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['trigger'],m.TRIGGER);self.assertEqual(c['operations'],[list(v) for v in cfg['operations']]);self.assertEqual(c['returncode'],0);payload=operations_payload(c['operations'])+b'\x08'+b.pointer(0x38B550)+b'\x02';self.assertLessEqual(len(payload),64);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}])
   for name,a,z in [('help_machine',0x055546,0x05558A),('help_key',0x055D82,0x055DA1),('retry_locker',0x2F69A1,0x2F69BA),('paper_locker',0x06FA2E,0x06FA68)]:self.assertTrue(any(a<=int(ptr,16)<z for ptr in r['cases'][name]['pointer_frame_counts']))
  for path in (ROOT/'tests/emulation_v78_actions').rglob('*'):
   if path.is_file() and '__pycache__' not in path.parts:self.assertIn(path.suffix.lower(),('.py','.json','.png'))
class ActionRom(unittest.TestCase):
 def test_reader_stride_help_commands_and_exact_capture_rom(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);f=read('tools/v78/v78_fixtures.json');dic=b.dictionary_from_rom(source)
  for p in ('accents','ascii'):
   records=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes());prefix=len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()));base=b.apply(source,records[:prefix+f['locker_help']['profiles'][p]['input_records_added']]);target=b.apply(source,records);writes=[(int(e['offset'],16),bytes.fromhex(e['hex'])) for stage in ('locker_help','item_action') for e in f[stage]['profiles'][p]['records']];self.assertEqual(len(writes),10);self.assertEqual(b.apply(base,writes),target);self.assertEqual(base[READER:READER+len(bytes.fromhex(READER_HEX))],bytes.fromhex(READER_HEX));self.assertEqual(target[READER:READER+len(bytes.fromhex(READER_HEX))],bytes.fromhex(READER_HEX))
   for i,(en,fr) in enumerate(LABELS):
    a=0x38E834+6*i;self.assertEqual(b.decode(base[a:a+6].split(b'\0')[0],dic),en);self.assertEqual(target[a:a+6],b.encode(fr,p).ljust(6,b'\0'));self.assertEqual(target[a+5],0)
   for item,root in ((0xAC,0x055546),(0xCD,0x055D82)):
    a=0x155000+39*item+35;self.assertEqual(target[a:a+4],base[a:a+4]);self.assertEqual(target[a:a+4],b.pointer(root))
   for root in (0x055546,0x055D82,0x2F69A1):
    q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));self.assertTrue(q['terminal']);self.assertFalse(q['error']);self.assertEqual(b.commands(base[root:q['end']]),b.commands(target[root:q['end']]))
   for c in read(f'tests/emulation_v78_actions/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(target),c['base_rom_sha256']);fixture=bytearray(target)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
