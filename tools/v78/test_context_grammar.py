import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
from context_grammar_stage import PRONOUNS,FRENCH,CALLERS,EMPTY
from item_help_stage import help_path
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload,prove
def read(path):return json.loads((ROOT/path).read_text())
class GrammarOffline(unittest.TestCase):
 def test_context_images_and_native_inputs(self):
  from verify_remaining import verify
  result=verify(ROOT/'tests/emulation_v78_grammar');self.assertEqual(result['pairs'],56)
  spec=importlib.util.spec_from_file_location('grammar_probe78',ROOT/'tests/emulation_v78_grammar/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_grammar/results_{p}.json');self.assertEqual(list(r['cases']),list(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];entry=cfg['entry'];entries=cfg.get('entries',[entry]);self.assertEqual(c['entries'],[f'{v:06X}' for v in entries]);self.assertEqual(c['logical_entry'],f'{entry:06X}');self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['scope'],cfg['scope']);self.assertEqual(c['operations'],cfg.get('operations',[]));self.assertEqual(c['trigger'],m.m.TRIGGER);self.assertEqual(c['returncode'],0);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':(operations_payload(c['operations'])+b''.join(b'\x08'+b.pointer(v) for v in entries)+b'\x02').hex()}]);counts=collections.Counter()
    for i,e in enumerate(c['events']):
     stop=c['events'][i+1]['sample'] if i+1<len(c['events']) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
  for v in (ROOT/'tests/emulation_v78_grammar').rglob('*'):
   if v.is_file():self.assertNotIn(v.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.sav','.srm','.wram','.dmp'))
class GrammarRom(unittest.TestCase):
 def test_contexts_shortened_returns_and_only_authorized_writes(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);f=read('tools/v78/v78_fixtures.json')['context_grammar'];self.assertEqual(f['entries'],PRONOUNS);self.assertEqual(f['french_corrections'],FRENCH);dic=b.dictionary_from_rom(source)
  for p in ('accents','ascii'):
   ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();records=b.records(ips);n=len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()));cut=n+f['profiles'][p]['input_records_added'];endcut=n+read('tools/v78/v78_fixtures.json')['article_context']['profiles'][p]['input_records_added'];base=b.apply(source,records[:cut]);target=b.apply(source,records[:endcut]);self.assertEqual(b.sha(target),read('tools/v78/v78_fixtures.json')['article_context']['profiles'][p]['input_rom_sha256']);self.assertEqual(b.sha(base),f['profiles'][p]['input_rom_sha256']);self.assertEqual(b.sha(b.append(b'PATCHEOF',records[:cut])),f['profiles'][p]['input_patch_sha256']);indices=[b.pointer_index(v) for v in (source,base,target)];expected=[]
   self.assertEqual(indices[1][0x387B19],[0x33FC4D]);self.assertEqual(indices[1][0x387AA2],[int(a,16) for _,a in CALLERS]);self.assertEqual(target[EMPTY],2)
   for e in PRONOUNS:
    root,a,z=(int(e[k],16) for k in ('context','offset','end'));self.assertEqual(b.decode(base[a:z],dic),e['en']);self.assertEqual(base[z],2);self.assertFalse(any(a<t<=z for ix in indices[:2] for t in ix));raw=b.encode(e['fr'],p)+b'\x02';raw+=bytes(z+1-a-len(raw));expected.append((a,raw));q=b.parse(target,root,8192,extra_glyphs=range(0xb0,0xc0));old=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));self.assertFalse(q['error']);self.assertTrue(q['terminal']);self.assertEqual(b.commands(base[root:old['end']]),b.commands(target[root:q['end']]));self.assertEqual(target[a:q['end']],b.encode(e['fr'],p)+b'\x02')
   for e in FRENCH:
    a,z=int(e['offset'],16),int(e['end'],16);self.assertEqual(b.decode(base[a:z],dic),e['en']);guard_end=z+5 if e.get('mode')=='short_bridge' else z;self.assertFalse(any(a<t<guard_end for ix in indices[:2] for t in ix));raw=b.encode(e['fr'],p)
    if e.get('mode')=='short_bridge':
     self.assertEqual(base[z:z+5],b'\x0a'+b.pointer(0x33FC4C));raw+=base[z:z+5]+bytes(z-a-len(raw));q=b.parse(target,a,8192,extra_glyphs=range(0xb0,0xc0));old=b.parse(base,a,8192,extra_glyphs=range(0xb0,0xc0));self.assertEqual(b.commands(target[a:q['end']]),b.commands(base[a:old['end']]))
    expected.append((a,raw))
   normalized=bytearray(target)
   for root,a in CALLERS:
    root,a=int(root,16),int(a,16);q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));self.assertIn((a,0x387AA2),q['refs']);self.assertEqual(base[a-1],8);expected.append((a,b.pointer(EMPTY)));normalized[a:a+4]=base[a:a+4];self.assertEqual(b.commands(base[root:q['end']]),b.commands(normalized[root:q['end']]))
   self.assertEqual(records[cut:endcut],expected);self.assertTrue(all(target[a:a+len(raw)]==raw for a,raw in expected));self.assertEqual(target[0x387AA2:0x387AB8],base[0x387AA2:0x387AB8]);self.assertEqual(b.sprite_digest(target),b.sprite_digest(base));self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000]);self.assertEqual(target[0x330FC0:0x331000],base[0x330FC0:0x331000]);self.assertEqual(target[0x2021A8:0x2021A8+1584*17],base[0x2021A8:0x2021A8+1584*17]);prove(target)
   for npc in f['qualified_npcs']:
    a=int(npc['operand'],16);self.assertEqual(a,0x2021A8+17*npc['npc']+9);root=int(npc['root'],16);self.assertEqual(base[a:a+4],b.pointer(root))
    for path in npc['paths']:self.assertEqual(help_path(base,root,int(path[-1],16)),path)
   for c in read(f'tests/emulation_v78_grammar/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(target),c['base_rom_sha256']);fixture=bytearray(target)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
