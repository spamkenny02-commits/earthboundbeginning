import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
from item_help_stage import help_path
from article_context_stage import CALLS
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload,prove
def read(path):return json.loads((ROOT/path).read_text())
class ArticlesOffline(unittest.TestCase):
 def test_display_inputs_and_semantic_trace(self):
  from verify_remaining import verify
  self.assertEqual(verify(ROOT/'tests/emulation_v78_articles')['pairs'],48)
  spec=importlib.util.spec_from_file_location('articles_probe78',ROOT/'tests/emulation_v78_articles/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_articles/results_{p}.json');self.assertEqual(list(r['cases']),list(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];entry=cfg['entry'];self.assertEqual(c['entries'],[f'{entry:06X}']);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['scope'],cfg['scope']);self.assertEqual(c['operations'],cfg.get('operations',[]));self.assertEqual(c['trigger'],m.m.TRIGGER);self.assertEqual(c['returncode'],0);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':(operations_payload(c['operations'])+b'\x08'+b.pointer(entry)+b'\x02').hex()}]);counts=collections.Counter()
    for i,e in enumerate(c['events']):
     stop=c['events'][i+1]['sample'] if i+1<len(c['events']) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
  for v in (ROOT/'tests/emulation_v78_articles').rglob('*'):
   if v.is_file():self.assertNotIn(v.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.sav','.srm','.wram','.dmp'))
class ArticlesRom(unittest.TestCase):
 def test_two_qualified_calls_and_classifier_preserved(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);f=read('tools/v78/v78_fixtures.json')['article_context'];self.assertEqual(f['new_source_count'],0);neutral=int(f['neutral_helper'],16)
  for p in ('accents','ascii'):
   ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();records=b.records(ips);cut=len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()))+f['profiles'][p]['input_records_added'];records=records[:cut+len(f['profiles'][p]['records'])];base=b.apply(source,records[:cut]);target=b.apply(source,records);self.assertEqual(b.sha(base),f['profiles'][p]['input_rom_sha256']);self.assertEqual(b.sha(b.append(b'PATCHEOF',records[:cut])),f['profiles'][p]['input_patch_sha256']);expected=[(0x32B50A,b.pointer(neutral)),(0x36B830,b.pointer(neutral)),(0x32B501,b.encode('@Objet: ',p)),(0x32B511,b.encode('.',p)+b'\x03\x02'+bytes(15)),(0x36B839,b.encode('  Cet objet sera bien gardé. ',p)),(0x36BA48,b.encode('@   ',p))];self.assertEqual(records[cut:],expected);self.assertTrue(all(target[a:a+len(raw)]==raw for a,raw in expected));normalized=bytearray(target)
   for npc,root,context,caller,helper in CALLS:
    row=next(v for v in f['qualified_contexts'] if v['npc']==npc);a=0x2021A8+17*npc+9;self.assertEqual(base[a:a+4],b.pointer(root));self.assertEqual(help_path(base,root,context),row['path']);q=b.parse(base,context,8192,extra_glyphs=range(0xb0,0xc0));self.assertIn((caller,helper),q['refs']);self.assertEqual(base[caller-1],8);self.assertEqual(target[neutral:neutral+6],base[helper:helper+6]);normalized[caller:caller+4]=b.pointer(helper)
   helper=b.parse(target,neutral,8192,extra_glyphs=range(0xb0,0xc0));self.assertEqual([t for _,t in helper['refs']],[0x38B550]*5);self.assertEqual(target[0x38B550],2)
   self.assertEqual(f['withdrawal_prefix']['path'],help_path(base,0x36B788,0x36BA13));self.assertEqual(base[0x36BA48:0x36BA4C],b.encode('@Le ',p))
   for root in (0x32B500,0x36B7D5,0x36BA13):
    old=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));new=b.parse(normalized,root,8192,extra_glyphs=range(0xb0,0xc0));self.assertTrue(new['terminal']);self.assertFalse(new['error']);self.assertEqual(b.commands(base[root:old['end']]),b.commands(normalized[root:new['end']]))
   indices=[b.pointer_index(v) for v in (source,base)]
   for a,z in ((0x32B501,0x32B509),(0x32B511,0x32B523),(0x36B839,0x36B856),(0x36BA48,0x36BA4C)):self.assertFalse(any(a<t<z for ix in indices for t in ix))
   for a,z in ((0x38B52B,0x38B5A2),(neutral,neutral+27),(0x32F120,0x32F1B2),(0x250000,0x260000),(0x2021A8,0x2021A8+1584*17),(0x330FC0,0x331000)):self.assertEqual(target[a:z],base[a:z])
   self.assertEqual(b.sprite_digest(base),b.sprite_digest(target));prove(target)
   for c in read(f'tests/emulation_v78_articles/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(target),c['base_rom_sha256']);fixture=bytearray(target)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
