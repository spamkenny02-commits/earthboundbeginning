import collections,hashlib,importlib.util,json,os,struct,sys,unittest
from pathlib import Path
from build_v73 import ROOT,b,CONFIG,ENTRY,NO,RETURN,NPC_POINTER,flattened
from safe_storage import safe_reserves
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import prove
def reports():return [(p,json.loads((ROOT/f'tests/emulation_v73/results_{p}.json').read_text())) for p in ('accents','ascii')]
def fixtures():return json.loads((ROOT/'tools/v73/v73_fixtures.json').read_text())
class OfflineTests(unittest.TestCase):
 def test_patch_records_and_menu_bridge(self):
  f=fixtures();dest=int(f['copy_offset'],16);plan=json.loads((ROOT/'tools/v73/validation_v73.json').read_text())
  for p in ('accents','ascii'):
   prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v71_{p}.ips').read_bytes();ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v73_{p}.ips').read_bytes();self.assertTrue(ips.startswith(prior[:-3]));self.assertEqual(b.sha(ips),plan['profiles'][p]['sha256']);records=b.records(ips)[len(b.records(prior)):];self.assertEqual(len(records),9)
   for (a,data),cfg in zip(records[:7],CONFIG):self.assertEqual(a,cfg[1]);self.assertEqual(len(data),cfg[2]-cfg[1])
   self.assertEqual(records[-2],(NO,b'\x0a'+b.pointer(dest)));self.assertEqual(records[-1],(dest,b'\x19\x02'+b.encode('Non',p)+b'\x02\x0a'+b.pointer(RETURN)));self.assertEqual(f['copy_size'],11)
 def test_inputs_and_post_rest_state_chain(self):
  spec=importlib.util.spec_from_file_location('probe73',ROOT/'tests/emulation_v73/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p,r in reports():
   self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['rest_and_warp_called_by_tester']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(list(r['cases']),list(m.CASES));accepted=r['cases']['accept'];self.assertEqual(len(accepted['output_state_sha256']),64);self.assertEqual(r['cases']['revisit']['input_state_sha256'],accepted['output_state_sha256'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['entries'],['37899B']);self.assertEqual(c['operations'],[]);self.assertEqual(c['trigger'],m.TRIGGER);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['settle_frames'],cfg['wait']);self.assertEqual(c['status_buttons'],['A','B'] if cfg['status'] else []);self.assertEqual(c['state_source'],cfg['state']);self.assertEqual(c['returncode'],0)
    if name!='revisit':self.assertEqual(c['input_state_sha256'],r['initial_state_sha256'])
    payload=b'\x08'+b.pointer(ENTRY)+b'\x02';self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}])
 def test_live_counts_and_native_branches(self):
  expected={'decline':('378AF3',100),'accept':('387A07',100),'revisit':('378A9D',100)}
  for p,r in reports():
   for name,c in r['cases'].items():
    counts=collections.Counter();events=c['events']
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts']);pointer,minimum=expected[name];self.assertGreater(counts[pointer],minimum)
 def test_png_integrity_no_private_files(self):
  count=0
  for p,r in reports():
   for c in r['cases'].values():
    for cap in c['captures']:
     path=ROOT/cap['path'];self.assertTrue(path.resolve().is_relative_to((ROOT/'tests/emulation_v73').resolve()));raw=path.read_bytes();self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',raw[16:24]),(256,224));self.assertEqual(hashlib.sha256(raw).hexdigest(),cap['artifact_png_sha256']);count+=1
  self.assertEqual(count,40)
  for f in (ROOT/'tests/emulation_v73').rglob('*'):
   if f.is_file():self.assertNotIn(f.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.wram','.dmp'))
 def test_custom_root_inventory_is_scoped_not_coverage(self):
  r=json.loads((ROOT/'tools/v73/custom_npc_roots_v73.json').read_text());self.assertFalse(r['natural_access_verified']);self.assertFalse(r['language_classification_verified']);self.assertEqual(r['custom_roots_examined'],181);self.assertEqual(len(r['candidates']),11);self.assertEqual(r['unparsed_roots'],[]);roots={e['root'] for e in r['candidates']};self.assertIn('387221',roots);self.assertNotIn('37899B',roots)
class RomTests(unittest.TestCase):
 def setUp(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  self.source=Path(path).read_bytes();self.assertEqual(b.sha(self.source),b.ROM_SHA);self.priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v71_{p}.ips').read_bytes() for p in ('accents','ascii')};self.bases={p:b.apply(self.source,b.records(v)) for p,v in self.priors.items()}
 def test_safe_bridge_text_and_native_commands(self):
  f=fixtures();dest=int(f['copy_offset'],16);targets=set(b.pointer_index(self.source))
  for base in self.bases.values():targets.update(b.pointer_index(base))
  targets.update(range(0x330FC0,0x331000));reserves,_=safe_reserves(self.source,self.bases,self.priors,targets,b.records);self.assertTrue(any(a<=dest and dest+11<=z for a,z in reserves));dic=b.dictionary_from_rom(self.source)
  for p,base in self.bases.items():
   target=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v73_{p}.ips').read_bytes()));self.assertEqual(base[dest:dest+11],bytes(11));self.assertEqual(b.commands(flattened(target,dest)),b.commands(base[ENTRY:0x378A4B]));self.assertEqual(target[0x378A4B:0x378AEE],base[0x378A4B:0x378AEE]);self.assertEqual(target[NPC_POINTER:NPC_POINTER+4],b.pointer(ENTRY));self.assertEqual(b.sprite_digest(target),b.sprite_digest(base));self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000])
   for root,a,z,en,fr in CONFIG:self.assertEqual(b.decode(base[a:z],dic),en);self.assertEqual(target[a:z],bytes.fromhex(next(e for e in f['profiles'][p]['edits'] if e['offset']==f'{a:06X}')['replacement_hex']))
 def test_fixture_hashes_and_engine(self):
  plan=json.loads((ROOT/'tools/v73/validation_v73.json').read_text())
  for p,r in reports():
   base=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v73_{p}.ips').read_bytes()));self.assertEqual(b.sha(base),plan['profiles'][p]['target_rom_sha256'])
   for c in r['cases'].values():
    fixture=bytearray(base)
    for write in c['temporary_rom_writes']:
     a=int(write['offset'],16);raw=bytes.fromhex(write['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256']);prove(fixture)
 def test_custom_root_inventory_reproduces(self):
  from audit_custom_npc_roots import audit
  data=b.apply(self.source,b.records((ROOT/'patches/EarthBound_Beginnings_FR_v73_accents.ips').read_bytes()));self.assertEqual(audit(self.source,data),json.loads((ROOT/'tools/v73/custom_npc_roots_v73.json').read_text()))
if __name__=='__main__':unittest.main()
