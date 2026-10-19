import collections,hashlib,importlib.util,json,struct,unittest
from build_v65 import ROOT,b,HELPER,EMPTY
class OfflineTests(unittest.TestCase):
 def test_patch_records_preserve_baseline_and_never_write_bank25(self):
  f=json.loads((ROOT/'tools/v65/v65_fixtures.json').read_text());plan=json.loads((ROOT/'tools/v65/validation_v65.json').read_text())
  for p in ('accents','ascii'):
   prior=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v64_{p}.ips').read_bytes());ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v65_{p}.ips').read_bytes();records=b.records(ips);self.assertEqual(b.sha(ips),plan['profiles'][p]['sha256']);self.assertEqual(records[:len(prior)],prior);new=records[len(prior):];self.assertEqual(len(new),17)
   allowed={int(e['offset'],16):4 for e in f['profiles'][p]['safe_pointer_edits']};allowed[int(f['copy_offset'],16)]=27;allowed[int(f['text_offset'],16)]=int(f['text_end'],16)-int(f['text_offset'],16)
   for node in f['moved_scripts']:
    for c in node['chunks']:allowed[int(c['destination'],16)]=int(c['source_end'],16)-int(c['source_start'],16)+(5 if c['continuation'] else 0)
   self.assertEqual({a:len(raw) for a,raw in new},allowed)
   for a,raw in new:self.assertFalse(a<0x260000 and a+len(raw)>0x250000)
   self.assertEqual(bytes.fromhex(f['profiles'][p]['scoped_helper_hex'])[:6],bytes.fromhex(f['profiles'][p]['original_helper_hex'])[:6])
   for q in (6,10,14,18,22):self.assertEqual(bytes.fromhex(f['profiles'][p]['scoped_helper_hex'])[q:q+4],b.pointer(EMPTY))
 def test_controller_sequences_and_live_trace_counts(self):
  spec=importlib.util.spec_from_file_location('v65_probe',ROOT/'tests/emulation_v65/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  plan=json.loads((ROOT/'tools/v65/validation_v65.json').read_text())
  for p in ('accents','ascii'):
   r=json.loads((ROOT/f'tests/emulation_v65/results_{p}.json').read_text());self.assertEqual(set(r['cases']),set(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    entries,steps=m.CASES[name];self.assertEqual(c['entries'],[f'{a:06X}' for a in entries]);self.assertEqual(c['steps'],steps);self.assertEqual(c['returncode'],0);self.assertEqual(c['base_rom_sha256'],plan['profiles'][p]['target_rom_sha256']);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':(b''.join(b'\x08'+b.pointer(a) for a in entries)+b'\x02').hex()}])
    counts=collections.Counter();events=c['events'];self.assertTrue(events)
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1;self.assertGreater(stop,e['sample'])
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
 def test_capture_files_and_dimensions(self):
  count=0
  for p in ('accents','ascii'):
   r=json.loads((ROOT/f'tests/emulation_v65/results_{p}.json').read_text())
   for c in r['cases'].values():
    for cap in c['captures']:
     raw=(ROOT/cap['path']).read_bytes();self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',raw[16:24]),(256,224));self.assertEqual(hashlib.sha256(raw).hexdigest(),cap['artifact_png_sha256']);count+=1
  self.assertEqual(count,84)
 def test_reference_images_and_difference_bounds(self):
  r=json.loads((ROOT/'tests/emulation_v65/comparison_v64.json').read_text())
  for p in ('accents','ascii'):
   self.assertEqual(r[p]['paired_captures'],20);self.assertTrue(r[p]['same_controller_inputs'])
   for c in r[p]['comparisons']:
    self.assertEqual(hashlib.sha256((ROOT/c['before_path']).read_bytes()).hexdigest(),c['before_png_sha256']);self.assertTrue(c['only_text_window_changed'])
    if c['bbox']:
     x,y,z,t=c['bbox'];self.assertGreaterEqual(x,104);self.assertGreaterEqual(y,8);self.assertLessEqual(z,248);self.assertLessEqual(t,98)
if __name__=='__main__':unittest.main()
