import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import operations_payload,prove
def load(name):return json.loads((ROOT/name).read_text())
class RemainingOffline(unittest.TestCase):
 def test_all_public_pairs_and_no_private_files(self):
  from verify_remaining import verify
  result=verify();self.assertGreater(result['pairs'],130)
  for f in (ROOT/'tests/emulation_v78_remaining').rglob('*'):
   if f.is_file():self.assertNotIn(f.suffix.lower(),('.sfc','.smc','.state','.sav','.so','.bin','.dmp'))
 def test_inputs_and_native_preparations(self):
  spec=importlib.util.spec_from_file_location('remain_probe',ROOT/'tests/emulation_v78_remaining/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for p in ('accents','ascii'):
   report=load(f'tests/emulation_v78_remaining/results_{p}.json');self.assertEqual(list(report['cases']),list(m.CASES));self.assertFalse(report['natural_scene_access_verified']);self.assertFalse(report['wram_written_directly_by_tester'])
   for name,c in report['cases'].items():
    cfg=m.CASES[name];self.assertEqual(c['logical_entry'],f'{cfg["entry"]:06X}');self.assertEqual(c['entries'],[c['logical_entry']]);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['trigger'],m.m.TRIGGER);self.assertEqual(c['operations'],cfg.get('operations',[]));self.assertEqual(c['scope'],cfg['scope']);self.assertEqual(c['returncode'],0);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':(operations_payload(c['operations'])+b'\x08'+b.pointer(cfg['entry'])+b'\x02').hex()}]);counts=collections.Counter()
    for i,e in enumerate(c['events']):
     stop=c['events'][i+1]['sample'] if i+1<len(c['events']) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
class RemainingRom(unittest.TestCase):
 def setUp(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  self.source=Path(path).read_bytes();self.assertEqual(b.sha(self.source),b.ROM_SHA);self.f=load('tools/v78/v78_fixtures.json')['remaining']
 def test_copied_scripts_commands_and_exact_callers(self):
  for p in ('accents','ascii'):
   base=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()));target=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes()));prove(target)
   for n in self.f['moved_scripts']:
    root,end,caller=(int(n[k],16) for k in ('root','end','caller'));self.assertEqual(b.pointer_index(base)[root],[caller]);self.assertEqual(target[caller:caller+4],b.pointer(int(n['chunks'][0]['destination'],16)));body=bytearray()
    for i,c in enumerate(n['chunks']):
     a=int(c['destination'],16);size=c['payload_size'];body.extend(target[a:a+size]);tail=b'\x0a'+b.pointer(int(n['chunks'][i+1]['destination'],16)) if i+1<len(n['chunks']) else bytes(5);self.assertEqual(target[a+size:a+size+5],tail)
    yes,no,ret=(int(n[k],16) for k in ('yes','no_definition','continuation'));expected=base[root:yes]+b.encode('Oui',p)+base[yes+3:no]+b'\x19\x02'+b.encode('Non',p)+b'\x02'+base[ret:end];self.assertEqual(body,expected);self.assertEqual(b.commands(bytes(body)),b.commands(base[root:end]))
   self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000]);self.assertEqual(b.sprite_digest(target),b.sprite_digest(base))
 def test_remaining_contexts_and_fixture_hashes(self):
  for p in ('accents','ascii'):
   final=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes()));base=b.apply(self.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()));expansions=[]
   for n in self.f['menus']:
    a,z,d=(int(n[k],16) for k in ('no_definition','continuation','destination'));expansions.append((a,z,final[d:d+6]));self.assertEqual(final[a:a+5],b'\x0a'+b.pointer(d));self.assertEqual(final[d+6:d+11],b'\x0a'+b.pointer(z))
   for e in self.f['labels']:
    a,z,d=(int(e[k],16) for k in ('offset','end','destination'));payload=b'\x19\x02'+b.encode(e['fr'],p)+b'\x02';self.assertEqual(final[a-2:a+3],b'\x0a'+b.pointer(d));self.assertEqual(final[d:d+len(payload)+5],payload+b'\x0a'+b.pointer(z+1));expansions.append((a-2,z+1,payload))
   roots={int(e['context'],16) for e in self.f['entries']+self.f['menus']+self.f['labels']}
   normalized=bytearray(final)
   for n in self.f['moved_scripts']:
    a=int(n['caller'],16);normalized[a:a+4]=b.pointer(int(n['root'],16))
   for root in roots:
    q=b.parse(base,root,8192,extra_glyphs=range(0xb0,0xc0));cursor=root;flat=bytearray()
    for a,z,payload in sorted(expansions):
     if root<=a<z<=q['end']:flat.extend(normalized[cursor:a]);flat.extend(payload);cursor=z
    flat.extend(normalized[cursor:q['end']]);self.assertEqual(b.commands(bytes(flat)),b.commands(base[root:q['end']]))
   for c in load(f'tests/emulation_v78_remaining/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(final),c['base_rom_sha256']);fixture=bytearray(final)
    for w in c['temporary_rom_writes']:
     a=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[a:a+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
