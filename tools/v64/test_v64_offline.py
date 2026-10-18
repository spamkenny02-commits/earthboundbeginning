"""Validate published patch records and read-only service evidence without ROM."""
import collections,hashlib,json,struct,unittest
from pathlib import Path
from build_v64 import CONFIG,b
ROOT=Path(__file__).resolve().parents[2]
class OfflineTests(unittest.TestCase):
 def test_autonomous_ips_preserves_every_prior_record(self):
  f=json.loads((ROOT/'tools/v64/v64_fixtures.json').read_text());plan=json.loads((ROOT/'tools/v64/validation_v64.json').read_text())
  for p in ('accents','ascii'):
   old=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes());ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v64_{p}.ips').read_bytes();new=b.records(ips)
   self.assertEqual(b.sha(ips),plan['profiles'][p]['sha256']);self.assertEqual(new[:len(old)],old);self.assertEqual(new[len(old):],[(int(e['offset'],16),bytes.fromhex(e['profiles'][p]['replacement_hex'])) for e in f['edits']]);self.assertEqual(len(f['edits']),4)
 def test_trace_counts_and_controlled_entry_labels(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('v64_probe',ROOT/'tests/emulation_v64/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p in ('accents','ascii'):
   r=json.loads((ROOT/f'tests/emulation_v64/results_{p}.json').read_text());self.assertFalse(r['natural_service_location_access_verified']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(set(r['cases']),set(m.CASES))
   for name,c in r['cases'].items():
    entry,steps,kind=m.CASES[name];self.assertEqual(c['entry'],f'{entry:06X}');self.assertEqual(c['steps'],steps);self.assertEqual(c['kind'],kind);self.assertEqual(c['returncode'],0);self.assertTrue(c['only_declared_routing_changed']);self.assertEqual(len(c['temporary_routing']),1);self.assertEqual(c['temporary_routing'][0]['offset'],'368B51');self.assertEqual(c['temporary_routing'][0]['new'],b.pointer(entry).hex())
    counts=collections.Counter();events=c['events'];self.assertTrue(events)
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1;self.assertGreater(stop,e['sample'])
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
 def test_every_capture_is_present_and_unchanged(self):
  count=0
  for p in ('accents','ascii'):
   r=json.loads((ROOT/f'tests/emulation_v64/results_{p}.json').read_text())
   for c in r['cases'].values():
    for cap in c['captures']:
     data=(ROOT/cap['path']).read_bytes();self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',data[16:24]),(256,224));self.assertEqual(hashlib.sha256(data).hexdigest(),cap['artifact_png_sha256']);count+=1
  self.assertEqual(count,122)
 def test_all_reference_pairs_keep_changes_inside_text_window(self):
  r=json.loads((ROOT/'tests/emulation_v64/comparison_v61.json').read_text())
  for p in ('accents','ascii'):
   self.assertEqual(r[p]['paired_captures'],11);self.assertTrue(r[p]['controller_steps_identical_in_all_three_routes'])
   for c in r[p]['comparisons']:
    self.assertTrue(c['only_text_window_changed']);self.assertEqual(hashlib.sha256((ROOT/c['before_path']).read_bytes()).hexdigest(),c['before_png_sha256'])
    if c['bbox']:
     a,y,z,t=c['bbox'];self.assertGreaterEqual(a,104);self.assertGreaterEqual(y,8);self.assertLessEqual(z,248);self.assertLessEqual(t,98)
if __name__=='__main__':unittest.main()
