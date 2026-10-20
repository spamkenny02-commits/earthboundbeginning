import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import prove
from item_help_stage import qualify,help_path
def read(path):return json.loads((ROOT/path).read_text())
class HelpOffline(unittest.TestCase):
 def test_help_images_inputs_and_trace_counts(self):
  from verify_remaining import verify
  result=verify(ROOT/'tests/emulation_v78_help');self.assertEqual(result['pairs'],164)
  spec=importlib.util.spec_from_file_location('help_probe78',ROOT/'tests/emulation_v78_help/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_help/results_{p}.json');self.assertEqual(list(r['cases']),list(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['entries'],[f'{cfg["entry"]:06X}']);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['scope'],cfg['scope']);self.assertEqual(c['trigger'],m.m.TRIGGER);self.assertEqual(c['operations'],[]);self.assertEqual(c['returncode'],0);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':(b'\x08'+b.pointer(cfg['entry'])+b'\x02').hex()}]);counts=collections.Counter()
    for i,e in enumerate(c['events']):
     stop=c['events'][i+1]['sample'] if i+1<len(c['events']) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
  for f in (ROOT/'tests/emulation_v78_help').rglob('*'):
   if f.is_file():self.assertNotIn(f.suffix.lower(),('.sfc','.smc','.so','.state','.bin','.sav','.srm','.dmp'))
class HelpRom(unittest.TestCase):
 def test_qualified_stock_paths_and_guarded_reference(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);f=read('tools/v78/v78_fixtures.json')['item_help'];self.assertEqual(len(f['entries']),15);self.assertEqual([e['offset'] for e in f['blocked_entries']],['05473C']);self.assertEqual(f['blocked_entries'][0]['targets'],['054743'])
  for p in ('accents','ascii'):
   ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes();prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes();records=b.records(ips);cut=len(b.records(prior))+f['profiles'][p]['input_records_added'];prefix=b.append(prior,records[len(b.records(prior)):cut]);self.assertEqual(b.sha(prefix),f['profiles'][p]['input_patch_sha256']);base=b.apply(source,records[:cut]);target=b.apply(source,records);self.assertEqual(b.sha(base),f['profiles'][p]['input_rom_sha256']);actual=qualify(base,source);self.assertEqual(actual['rows'],f['qualification']['rows']);self.assertEqual([{k:v for k,v in i.items() if k!='name'} for i in actual['items']],[{k:v for k,v in i.items() if k!='name'} for i in f['qualification']['items']]);self.assertEqual(len(f['qualification']['items']),82);expected=[];dic=b.dictionary_from_rom(source)
   if p=='accents':self.assertEqual(actual,f['qualification'])
   for e in f['entries']:
    item=next(i for i in f['qualification']['items'] if i['id']==e['item_id']);self.assertEqual(help_path(base,int(item['help_root'],16),int(e['context'],16)),e['help_path'])
    root,a,z=(int(e[k],16) for k in ('context','offset','end'));self.assertEqual(b.decode(base[a:z],dic),e['en']);raw=b.encode(e['fr'],p)+b.encode(' ',p)*(z-a-len(b.encode(e['fr'],p)));expected.append((a,raw));self.assertEqual(target[a:z],raw);end=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0))['end'];self.assertEqual(b.commands(target[root:end]),b.commands(base[root:end]));self.assertFalse(any(a<t<z for t in b.pointer_index(base)))
   self.assertEqual(records[cut:cut+len(expected)],expected);self.assertEqual(target[0x05473C:0x054758],base[0x05473C:0x054758]);self.assertEqual(b.sprite_digest(target),b.sprite_digest(base));self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000]);prove(target)
   snapshot=b.apply(source,records[:cut+len(expected)]);self.assertEqual(b.sha(snapshot),read('tools/v78/v78_fixtures.json')['scoped_help']['profiles'][p]['input_rom_sha256'])
   for c in read(f'tests/emulation_v78_help/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(snapshot),c['base_rom_sha256']);fixture=bytearray(snapshot)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
