import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v74 import ROOT,b,CONFIG,ENTRY,MENUS,NPC_POINTER,flattened,safe_reserves
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import prove,operations_payload
def fixtures():return json.loads((ROOT/'tools/v74/v74_fixtures.json').read_text())
def reports():return [(p,json.loads((ROOT/f'tests/emulation_v74/results_{p}.json').read_text())) for p in ('accents','ascii')]
class OfflineTests(unittest.TestCase):
 def test_append_records_and_four_bridges(self):
  f=fixtures();plan=json.loads((ROOT/'tools/v74/validation_v74.json').read_text());self.assertEqual(plan['english_text_spans_translated'],9);self.assertEqual(plan['existing_french_spans_polished'],2)
  for p in ('accents','ascii'):
   prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v73_{p}.ips').read_bytes();ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v74_{p}.ips').read_bytes();self.assertTrue(ips.startswith(prior[:-3]));self.assertEqual(b.sha(ips),plan['profiles'][p]['sha256']);records=b.records(ips)[len(b.records(prior)):];self.assertEqual(len(records),15)
   for (a,raw),cfg in zip(records[:7],CONFIG):self.assertEqual((a,len(raw)),(cfg[1],cfg[2]-cfg[1]))
   for i,(menu,copy) in enumerate(zip(MENUS,f['menus'])):
    dest=int(copy['destination'],16);self.assertEqual(records[7+2*i],(menu[3],b'\x0a'+b.pointer(dest)));self.assertEqual(records[8+2*i],(dest,b'\x19\x02'+b.encode('Non',p)+b'\x02\x0a'+b.pointer(menu[4])))
 def test_declared_inputs_and_fixture_scope(self):
  spec=importlib.util.spec_from_file_location('probe74',ROOT/'tests/emulation_v74/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p,r in reports():
   self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertIn('V71 reference lodging',r['initial_state_source']);self.assertEqual(r['patch_tested'],'v74');self.assertEqual(list(r['cases']),list(m.CASES))
   for name,c in r['cases'].items():
    cfg=m.CASES[name];ops=m.operations(cfg);self.assertEqual(c['operations'],[list(op) for op in ops]);self.assertEqual(c['entries'],['387221']);self.assertEqual(c['trigger'],m.TRIGGER);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['inventory_trigger'],['A','Right','A','A'] if cfg['inventory'] else []);self.assertEqual(c['returncode'],0)
    payload=operations_payload(ops)+b'\x08'+b.pointer(ENTRY)+b'\x02';self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}])
 def test_native_branch_trace_counts(self):
  pointers={'decline_entry':'387289','protected_card':'387216','sale_accept':'3872D1','sale_decline':'3873E5'}
  for p,r in reports():
   for name,c in r['cases'].items():
    counts=collections.Counter();events=c['events']
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts']);self.assertGreater(counts[pointers[name]],20)
 def test_no_private_binary_or_absolute_capture_paths(self):
  for p,r in reports():
   for c in r['cases'].values():
    for cap in c['captures']:self.assertFalse(Path(cap['path']).is_absolute());self.assertTrue((ROOT/cap['path']).resolve().is_relative_to((ROOT/'tests/emulation_v74').resolve()))
  for path in (ROOT/'tests/emulation_v74').rglob('*'):
   if path.is_file():self.assertNotIn(path.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.wram','.dmp'))
 def test_all_56_display_pairs(self):
  spec=importlib.util.spec_from_file_location('display74',ROOT/'tools/v74/verify_display.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  self.assertEqual(m.verify()['captures_and_pairs'],56)
class RomTests(unittest.TestCase):
 def setUp(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  self.source=Path(path).read_bytes();self.assertEqual(b.sha(self.source),b.ROM_SHA);self.priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v73_{p}.ips').read_bytes() for p in ('accents','ascii')};self.bases={p:b.apply(self.source,b.records(v)) for p,v in self.priors.items()}
 def test_safe_allocations_and_preserved_engine(self):
  f=fixtures();targets=set(b.pointer_index(self.source))
  for base in self.bases.values():targets.update(b.pointer_index(base))
  targets.update(range(0x330FC0,0x331000));reserves,_=safe_reserves(self.source,self.bases,self.priors,targets,b.records);destinations=[int(c['destination'],16) for c in f['menus']];self.assertEqual(len(set(destinations)),4)
  for dest in destinations:self.assertTrue(any(a<=dest and dest+11<=z for a,z in reserves))
  for p,base in self.bases.items():
   target=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v74_{p}.ips').read_bytes()))
   for menu,dest in zip(MENUS,destinations):
    self.assertEqual(base[dest:dest+11],bytes(11));self.assertEqual(b.commands(flattened(target,menu,dest)),b.commands(base[menu[0]:menu[5]]))
    for root in (menu[0],dest,menu[4]):
     q=b.parse(target,root,8192,extra_glyphs=range(0xB0,0xC0));self.assertTrue(q['terminal']);self.assertFalse(q['error'])
   self.assertEqual(target[NPC_POINTER:NPC_POINTER+4],b.pointer(ENTRY));self.assertEqual(b.sprite_digest(target),b.sprite_digest(base));self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000]);self.assertEqual(target[0x330FC0:0x331000],base[0x330FC0:0x331000])
 def test_fixed_text_and_polished_native_commands(self):
  dic=b.dictionary_from_rom(self.source);f=fixtures()
  for p,base in self.bases.items():
   target=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v74_{p}.ips').read_bytes()))
   for root,a,z,en,fr in CONFIG:
    self.assertEqual(b.decode(base[a:z],dic),en);self.assertEqual(target[a:z],bytes.fromhex(next(e for e in f['profiles'][p]['edits'] if e['offset']==f'{a:06X}')['replacement_hex']))
   for root in (0x38714B,0x387202):
    end=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0))['end'];self.assertEqual(b.commands(base[root:end]),b.commands(target[root:end]))
 def test_fixture_hashes_and_engine(self):
  plan=json.loads((ROOT/'tools/v74/validation_v74.json').read_text())
  for p,r in reports():
   base=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v74_{p}.ips').read_bytes()));self.assertEqual(b.sha(base),plan['profiles'][p]['target_rom_sha256'])
   for c in r['cases'].values():
    fixture=bytearray(base)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(base),c['base_rom_sha256']);self.assertEqual(b.sha(fixture),c['fixture_rom_sha256']);prove(fixture)
if __name__=='__main__':unittest.main()
