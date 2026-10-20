import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v77 import ROOT,b,CONFIG,CONTEXTS,ENTRY,MENUS,NPC_POINTER,flattened,safe_reserves
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import prove
def fixtures():return json.loads((ROOT/'tools/v77/v77_fixtures.json').read_text())
def reports():return [(p,json.loads((ROOT/f'tests/emulation_v77/results_{p}.json').read_text())) for p in ('accents','ascii')]
class OfflineTests(unittest.TestCase):
 def test_fixed_records_and_non_bridge(self):
  f=fixtures();plan=json.loads((ROOT/'tools/v77/validation_v77.json').read_text());self.assertEqual(plan['changed_text_spans'],14);self.assertEqual(plan['english_text_spans_translated'],13);self.assertEqual(plan['existing_french_spans_polished'],1)
  dest=int(f['menus'][0]['destination'],16);menu=MENUS[0]
  for p in ('accents','ascii'):
   prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v76_{p}.ips').read_bytes();ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes();self.assertTrue(ips.startswith(prior[:-3]));self.assertEqual(b.sha(ips),plan['profiles'][p]['sha256']);records=b.records(ips)[len(b.records(prior)):];self.assertEqual(len(records),15)
   for (a,raw),cfg in zip(records[:13],CONFIG):self.assertEqual((a,len(raw)),(cfg[1],cfg[2]-cfg[1]))
   self.assertEqual(records[13],(menu[3],b'\x0a'+b.pointer(dest)));self.assertEqual(records[14],(dest,b'\x19\x02'+b.encode('Non',p)+b'\x02\x0a'+b.pointer(menu[4])))
 def test_declared_calls_and_no_direct_wram(self):
  spec=importlib.util.spec_from_file_location('probe77',ROOT/'tests/emulation_v77/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p,r in reports():
   self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(r['patch_tested'],'v77');self.assertEqual(list(r['cases']),list(m.CASES))
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['entries'],[f'{cfg["entry"]:06X}']);self.assertEqual(c['scope'],cfg['scope']);self.assertEqual(c['operations'],[]);self.assertEqual(c['trigger'],m.TRIGGER);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['returncode'],0);payload=b'\x08'+b.pointer(cfg['entry'])+b'\x02';self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}])
 def test_live_counts_and_camel_retry(self):
  for p,r in reports():
   for name,c in r['cases'].items():
    counts=collections.Counter();events=c['events']
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
   counts=r['cases']['camel_no_then_yes']['pointer_frame_counts'];self.assertIn('37440A',counts);self.assertIn('374371',counts);self.assertNotIn('37440A',r['cases']['camel_yes']['pointer_frame_counts'])
 def test_only_declared_public_pngs(self):
  comparison=json.loads((ROOT/'tests/emulation_v77/comparison_v76.json').read_text());declared={ROOT/pair[key] for profile in comparison.values() for pair in profile['comparisons'] for key in ('before_path','after_path')};self.assertEqual(set((ROOT/'tests/emulation_v77').rglob('*.png')),declared);self.assertEqual(len(declared),96)
  for path in (ROOT/'tests/emulation_v77').rglob('*'):
   if path.is_file():self.assertNotIn(path.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.wram','.dmp'))
 def test_all_48_display_pairs(self):
  spec=importlib.util.spec_from_file_location('display77',ROOT/'tools/v77/verify_display.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);self.assertEqual(m.verify()['captures_and_pairs'],48)
class RomTests(unittest.TestCase):
 def setUp(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  self.source=Path(path).read_bytes();self.assertEqual(b.sha(self.source),b.ROM_SHA);self.priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v76_{p}.ips').read_bytes() for p in ('accents','ascii')};self.bases={p:b.apply(self.source,b.records(v)) for p,v in self.priors.items()}
 def test_safe_non_bridge_and_retry_context(self):
  f=fixtures();dest=int(f['menus'][0]['destination'],16);targets=set(b.pointer_index(self.source))
  for base in self.bases.values():targets.update(b.pointer_index(base))
  targets.update(range(0x330FC0,0x331000));reserves,_=safe_reserves(self.source,self.bases,self.priors,targets,b.records);self.assertTrue(any(a<=dest and dest+11<=z for a,z in reserves))
  for p,base in self.bases.items():
   target=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()));self.assertEqual(base[dest:dest+11],bytes(11))
   for menu in (MENUS[0],(0x374351,*MENUS[0][1:])):self.assertEqual(b.commands(flattened(target,menu,dest)),b.commands(base[menu[0]:menu[5]]))
   for root in (ENTRY,0x374351,dest,MENUS[0][4]):
    q=b.parse(target,root,8192,extra_glyphs=range(0xB0,0xC0));self.assertTrue(q['terminal']);self.assertFalse(q['error'])
 def test_text_native_commands_npc_table_sprites_and_bank(self):
  dic=b.dictionary_from_rom(self.source);f=fixtures();plan=json.loads((ROOT/'tools/v77/validation_v77.json').read_text())
  for p,base in self.bases.items():
   target=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()));self.assertEqual(b.sha(target),plan['profiles'][p]['target_rom_sha256'])
   for root,a,z,en,fr in CONFIG:self.assertEqual(b.decode(base[a:z],dic),b.decode(b.encode(en,p),dic));self.assertEqual(target[a:z],bytes.fromhex(next(x for x in f['profiles'][p]['edits'] if x['offset']==f'{a:06X}')['replacement_hex']))
   for root in CONTEXTS:
    end=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0))['end'];self.assertEqual(b.commands(target[root:end]),b.commands(base[root:end]))
   self.assertEqual(target[0x2021A8:0x2021A8+1584*17],base[0x2021A8:0x2021A8+1584*17]);self.assertEqual(target[NPC_POINTER:NPC_POINTER+4],b.pointer(ENTRY));self.assertEqual(b.sprite_digest(target),b.sprite_digest(base));self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000]);self.assertEqual(target[0x330FC0:0x331000],base[0x330FC0:0x331000])
 def test_fixture_hashes_and_engine(self):
  for p,r in reports():
   base=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()))
   for c in r['cases'].values():
    fixture=bytearray(base)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(base),c['base_rom_sha256']);self.assertEqual(b.sha(fixture),c['fixture_rom_sha256']);prove(fixture)
if __name__=='__main__':unittest.main()
