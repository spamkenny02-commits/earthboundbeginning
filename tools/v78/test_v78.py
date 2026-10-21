import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b,CONFIG,MENUS,safe_reserves
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import prove
def fixtures():return json.loads((ROOT/'tools/v78/v78_fixtures.json').read_text())
def reports():return [(p,json.loads((ROOT/f'tests/emulation_v78/results_{p}.json').read_text())) for p in ('accents','ascii')]
def read_plan():return json.loads((ROOT/'tools/v78/validation_v78.json').read_text())
def expansions(f,p,target):
 result=[]
 for menu in f['menus']:
  a,z,d=(int(menu[k],16) for k in ('no_definition','continuation','destination'));result.append((a,z,target[d:d+6]))
 for e in f['medical']['profiles'][p]['edits']:
  if e['mode']=='fixed':continue
  a,z=(int(e[k],16) for k in ('bridge_start','bridge_end'));payload=b''.join(target[int(n['offset'],16):int(n['offset'],16)+n['payload_size']] for n in e['blocks']);expected=b.encode(e['fr'],p)
  if e['mode']=='menu_bridge':expected=b'\x19\x02'+expected+b'\x02'
  assert payload==expected
  for i,node in enumerate(e['blocks']):
   d=int(node['offset'],16);size=node['payload_size'];ret=int(e['blocks'][i+1]['offset'],16) if i+1<len(e['blocks']) else z;assert target[d+size:d+size+5]==b'\x0a'+b.pointer(ret)
   if e['mode']=='text_bridge' and i+1<len(e['blocks']):assert target[d+size-1:d+size]==b.encode(' ',p)
  assert target[a:a+5]==b'\x0a'+b.pointer(int(e['blocks'][0]['offset'],16));result.append((a,z,payload))
 for menu in f['medical']['menus']:
  a,z,d=(int(menu[k],16) for k in ('offset','end','destination'));result.append((a,z,target[d:d+6]))
 return sorted(result)
class OfflineTests(unittest.TestCase):
 def test_batch_counter_and_blocked_entry(self):
  f=fixtures();p=read_plan();texts={e['english'] for e in f['profiles']['accents']['edits']}|{'No'}|{e['en'] for e in f['medical']['entries']}|{e['en'] for e in f['remaining']['entries']+f['remaining']['labels']+f['item_help']['entries']+f['scoped_help']['entries']+f['context_grammar']['entries']+f['phone_label']['entries']};self.assertEqual(len(texts),120);self.assertEqual(p['distinct_new_translations'],120);self.assertEqual(p['batch_target_distinct_texts'],150);self.assertTrue(p['release_pending']);self.assertEqual(p['changed_text_spans'],158);self.assertEqual([e['offset'] for e in f['medical']['blocked_entries']],['0911ED'])
  from update_ledger import build
  ledger=json.loads((ROOT/'tools/v78/batch_ledger.json').read_text());self.assertEqual(ledger,build());self.assertEqual({e['source'] for e in ledger['entries']},texts);self.assertEqual(len({a for e in ledger['entries'] for a in e['offsets']}),158)
 def test_patch_prefix_hash_and_changed_records(self):
  f=fixtures();plan=read_plan()
  for p in ('accents','ascii'):
   prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes();ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();self.assertTrue(ips.startswith(prior[:-3]));self.assertEqual(b.sha(ips),plan['profiles'][p]['sha256']);added=b.records(ips)[len(b.records(prior)):];self.assertEqual(len(added),plan['profiles'][p]['records_added']);expected=[(int(e['offset'],16),bytes.fromhex(e['hex'])) for stage in ('medical','remaining','item_help','scoped_help','context_grammar','article_context','phone_label') for e in f[stage]['profiles'][p]['records']];self.assertEqual(added[26:],expected)
 def test_inputs_and_recomputed_trace_counts(self):
  spec=importlib.util.spec_from_file_location('probe78',ROOT/'tests/emulation_v78/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p,r in reports():
   self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester']);self.assertEqual(list(r['cases']),list(m.CASES))
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['entries'],[f'{cfg["entry"]:06X}']);self.assertEqual(c['operations'],[]);self.assertEqual(c['trigger'],m.TRIGGER);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['settle_frames'],cfg.get('wait',180));self.assertEqual(c['returncode'],0);payload=b'\x08'+b.pointer(cfg['entry'])+b'\x02';self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':payload.hex()}]);counts=collections.Counter();events=c['events']
    for i,e in enumerate(events):
     stop=events[i+1]['sample'] if i+1<len(events) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
 def test_only_declared_public_images(self):
  comparison=json.loads((ROOT/'tests/emulation_v78/comparison_v77.json').read_text());declared={ROOT/pair[key] for profile in comparison.values() for pair in profile['comparisons'] for key in ('before_path','after_path')};self.assertEqual(set((ROOT/'tests/emulation_v78').rglob('*.png')),declared);self.assertEqual(len(declared),292)
  for path in (ROOT/'tests/emulation_v78').rglob('*'):
   if path.is_file():self.assertNotIn(path.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.wram','.dmp'))
 def test_146_rgb_pairs(self):
  spec=importlib.util.spec_from_file_location('display78',ROOT/'tools/v78/verify_display.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);self.assertEqual(m.verify()['captures_and_pairs'],146)
class RomTests(unittest.TestCase):
 def setUp(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  self.source=Path(path).read_bytes();self.assertEqual(b.sha(self.source),b.ROM_SHA);self.priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes() for p in ('accents','ascii')};self.bases={p:b.apply(self.source,b.records(v)) for p,v in self.priors.items()}
 def test_expanded_native_commands_and_preserved_alias(self):
  f=fixtures();contexts={root for root,*_ in CONFIG}|{int(e['context'],16) for e in f['medical']['entries']}|{int(e['context'],16) for e in f['medical']['menus']}
  for p,base in self.bases.items():
   records=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes());target=b.apply(self.source,records[:len(b.records(self.priors[p]))+f['scoped_help']['profiles'][p]['input_records_added']]);edits=expansions(f,p,target)
   for root in contexts:
    end=b.parse(base,root,8192,extra_glyphs=range(0xB0,0xC0))['end'];cursor=root;flat=bytearray()
    for a,z,payload in edits:
     if root<=a and z<=end:flat.extend(target[cursor:a]);flat.extend(payload);cursor=z
    flat.extend(target[cursor:end]);self.assertEqual(b.commands(bytes(flat)),b.commands(base[root:end]))
   self.assertEqual(target[0x0911ED:0x091212],base[0x0911ED:0x091212]);self.assertEqual(target[0x2021A8:0x2021A8+1584*17],base[0x2021A8:0x2021A8+1584*17]);self.assertEqual(b.sprite_digest(target),b.sprite_digest(base));self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000]);self.assertEqual(target[0x330FC0:0x331000],base[0x330FC0:0x331000])
 def test_allocations_are_original_protected_zero_padding(self):
  f=fixtures();targets=set(b.pointer_index(self.source))
  for base in self.bases.values():targets.update(b.pointer_index(base))
  targets.update(range(0x330FC0,0x331000));reserves,_=safe_reserves(self.source,self.bases,self.priors,targets,b.records)
  for p,base in self.bases.items():
   ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();added=b.records(ips)[len(b.records(self.priors[p])):len(b.records(self.priors[p]))+f['context_grammar']['profiles'][p]['input_records_added']];allocated=sorted((a,raw) for a,raw in added if 0x328A70<=a<0x331000 and a not in (0x32E139,0x32E13D,0x329025))
   for i,(a,raw) in enumerate(allocated):
    self.assertEqual(base[a:a+len(raw)],bytes(len(raw)));self.assertTrue(any(lo<=a and a+len(raw)<=hi for lo,hi in reserves));self.assertFalse(any(a<=t<a+len(raw) for t in targets))
    if i:self.assertLessEqual(allocated[i-1][0]+len(allocated[i-1][1]),a)
 def test_fixtures_and_patched_engine(self):
  plan=read_plan()
  for p,r in reports():
   records=b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes());final=b.apply(self.source,records);self.assertEqual(b.sha(final),plan['profiles'][p]['target_rom_sha256']);prove(final)
   # The retained medical captures certify the 81-text checkpoint exactly.
   # New train/dialogue captures certify the later target separately.
   base=b.apply(self.source,records[:len(b.records(self.priors[p]))+219]);self.assertEqual(b.sha(base),fixtures()['remaining']['profiles'][p]['input_rom_sha256'])
   for c in r['cases'].values():
    fixture=bytearray(base)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(base),c['base_rom_sha256']);self.assertEqual(b.sha(fixture),c['fixture_rom_sha256']);prove(fixture)
if __name__=='__main__':unittest.main()
