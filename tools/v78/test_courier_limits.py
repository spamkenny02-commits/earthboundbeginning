import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
from item_help_stage import help_path
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload
def read(path):return json.loads((ROOT/path).read_text())
def probe():
 spec=importlib.util.spec_from_file_location('courier78',ROOT/'tests/emulation_v78_courier/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class CourierOffline(unittest.TestCase):
 def test_linked_states_inputs_and_declared_preparation(self):
  from verify_remaining import verify
  self.assertEqual(verify(ROOT/'tests/emulation_v78_courier')['pairs'],152);m=probe()
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_courier/results_{p}.json');self.assertEqual(list(r['cases']),list(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['courier_script_called_by_tester']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['operations'],[list(v) for v in cfg['operations']]);self.assertEqual(c['post_operations'],[list(v) for v in cfg.get('post_operations',[])]);self.assertEqual(c['entries'],[f'{cfg["entry"]:06X}']);self.assertEqual(c['state_source'],cfg['state']);self.assertEqual(c['input_state_sha256'],r['initial_state_sha256'] if cfg['state']=='initial' else r['cases'][cfg['state']]['output_state_sha256']);self.assertEqual(c['exit_route'],m.EXIT if cfg.get('phone') else []);self.assertEqual(c['trigger'],m.TRIGGER);self.assertEqual(c['steps'],m.PHONE if cfg.get('phone') else cfg.get('steps',[]));self.assertEqual(c['courier_steps'],cfg.get('courier',[]));self.assertEqual(c['wait_after_phone_frames'],600 if cfg.get('phone') else 0);self.assertEqual(c['inventory_trigger'],['A','Right','A'] if cfg.get('inventory') else []);self.assertEqual(c['inventory_close'],['B','B'] if cfg.get('inventory') else []);self.assertEqual(c['returncode'],0)
    payload=operations_payload(c['operations'])+b'\x08'+b.pointer(cfg['entry'])+operations_payload(c['post_operations'])+b'\x02';self.assertLessEqual(len(payload),64);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}]);counts=collections.Counter()
    for i,e in enumerate(c['events']):
     stop=c['events'][i+1]['sample'] if i+1<len(c['events']) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
   # Exact native graph portions reached, rather than a claim based on filenames.
   for name in ('limit_three','reserve_full'):
    pointers={int(a,16) for a in r['cases'][name]['pointer_frame_counts']};self.assertTrue(any(0x35CFFF<=a<0x35D018 for a in pointers))
   pointers={int(a,16) for a in r['cases']['reserve_full']['pointer_frame_counts']};self.assertTrue(any(0x641B0<=a<0x64240 for a in pointers))
  for path in (ROOT/'tests/emulation_v78_courier').rglob('*'):
   if path.is_file() and '__pycache__' not in path.parts:self.assertIn(path.suffix.lower(),('.py','.json','.png'))
class CourierRom(unittest.TestCase):
 def test_phone_label_and_courier_fixture_hashes(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);dic=b.dictionary_from_rom(source);f=read('tools/v78/v78_fixtures.json')['phone_label'];e=f['entries'][0];root,a,z=(int(e[k],16) for k in ('context','offset','end'))
  for p in ('accents','ascii'):
   records=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes());cut=len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()))+f['profiles'][p]['input_records_added'];base=b.apply(source,records[:cut]);target=b.apply(source,records);self.assertEqual(b.sha(base),f['profiles'][p]['input_rom_sha256']);self.assertEqual(b.decode(base[a:z],dic),e['en']);self.assertEqual(target[a:z],b.encode(e['fr'],p)+b.encode(' ',p)*(z-a-len(b.encode(e['fr'],p))));self.assertEqual(target[:a],base[:a]);self.assertEqual(target[z:],base[z:]);self.assertEqual(f['profiles'][p]['phone_path'],help_path(base,0x35A925,root));q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));self.assertEqual(b.commands(base[root:q['end']]),b.commands(target[root:q['end']]));self.assertEqual(b.sprite_digest(base),b.sprite_digest(target))
   for c in read(f'tests/emulation_v78_courier/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(target),c['base_rom_sha256']);fixture=bytearray(target)
    for w in c['temporary_rom_writes']:
     a2=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a2:a2+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
