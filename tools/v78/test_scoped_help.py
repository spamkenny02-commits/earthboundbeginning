import collections,importlib.util,json,os,sys,unittest
from pathlib import Path
from build_v78 import ROOT,b,safe_reserves
from item_help_stage import qualify
from remaining_stage import atoms
sys.path.insert(0,str(ROOT/'tools/v70'))
from service_session import prove
def read(path):return json.loads((ROOT/path).read_text())
class ScopedOffline(unittest.TestCase):
 def test_images_inputs_and_counts(self):
  from verify_remaining import verify
  self.assertEqual(verify(ROOT/'tests/emulation_v78_scoped')['pairs'],36)
  spec=importlib.util.spec_from_file_location('scoped_probe78',ROOT/'tests/emulation_v78_scoped/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  f=read('tools/v78/v78_fixtures.json')['scoped_help']
  for p in ('accents','ascii'):
   r=read(f'tests/emulation_v78_scoped/results_{p}.json');self.assertEqual(list(r['cases']),list(m.CASES));self.assertFalse(r['natural_scene_access_verified']);self.assertFalse(r['wram_written_directly_by_tester'])
   for name,c in r['cases'].items():
    cfg=m.CASES[name];entry=cfg['entry']
    if cfg.get('scoped_copy'):entry=int(next(e for e in f['entries'] if int(e['context'],16)==entry)['chunks'][0]['destination'],16)
    self.assertEqual(c['logical_entry'],f'{cfg["entry"]:06X}');self.assertEqual(c['entries'],[f'{entry:06X}']);self.assertEqual(c['steps'],cfg['steps']);self.assertEqual(c['scope'],cfg['scope']);self.assertEqual(c['operations'],[]);self.assertEqual(c['trigger'],m.m.TRIGGER);self.assertEqual(c['returncode'],0);self.assertEqual(c['temporary_rom_writes'],[{'offset':'368B51','hex':b.pointer(0x330FC0).hex()},{'offset':'330FC0','hex':(b'\x08'+b.pointer(entry)+b'\x02').hex()}]);counts=collections.Counter()
    for i,e in enumerate(c['events']):
     stop=c['events'][i+1]['sample'] if i+1<len(c['events']) else c['sampled_frames']+1
     if e['pointer']:counts[e['pointer']['rom_offset']]+=stop-e['sample']
    self.assertEqual(dict(counts),c['pointer_frame_counts'])
  for v in (ROOT/'tests/emulation_v78_scoped').rglob('*'):
   if v.is_file():self.assertNotIn(v.suffix.lower(),('.sfc','.smc','.so','.bin','.state','.sav','.srm','.dmp','.wram'))
class ScopedRom(unittest.TestCase):
 def test_exact_scoped_copies_and_preserved_aliases(self):
  path=os.environ.get('EARTHBOUND_ROM')
  if not path:self.skipTest('Private ROM not supplied')
  source=Path(path).read_bytes();self.assertEqual(b.sha(source),b.ROM_SHA);f=read('tools/v78/v78_fixtures.json')['scoped_help'];ps={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v78_{p}.ips').read_bytes() for p in ('accents','ascii')};prefixes={p:b.records(v)[:len(b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v77_{p}.ips').read_bytes()))+f['profiles'][p]['input_records_added']] for p,v in ps.items()};bases={p:b.apply(source,v) for p,v in prefixes.items()};targets=set(b.pointer_index(source))
  for base in bases.values():targets.update(b.pointer_index(base))
  targets.update(range(0x330FC0,0x331000));reserves,_=safe_reserves(source,bases,{p:b.append(b'PATCH' + b'EOF',v) for p,v in prefixes.items()},targets,b.records)
  for p,base in bases.items():
   records=b.records(ps[p]);target=b.apply(source,records);self.assertEqual(b.sha(base),f['profiles'][p]['input_rom_sha256']);self.assertEqual(b.sha(b.append(b'PATCHEOF',prefixes[p])),f['profiles'][p]['input_patch_sha256']);expected=[];seen=[]
   for e in f['entries']:
    root,a,z,end,caller=(int(e[k],16) for k in ('context','offset','end','context_end','caller'));body=base[root:a]+b.encode(e['fr'],p)+base[z:end];self.assertEqual(b.commands(body),b.commands(base[root:end]));self.assertEqual(target[root:end],base[root:end]);self.assertEqual(base[caller:caller+4],b.pointer(root));payload=bytearray();pos=0
    for i,c in enumerate(e['chunks']):
     d=int(c['destination'],16);size=c['payload_size'];raw=body[pos:pos+size]+(b'\x0a'+b.pointer(int(e['chunks'][i+1]['destination'],16)) if i+1<len(e['chunks']) else bytes(5));pos+=size;self.assertEqual(target[d:d+len(raw)],raw);self.assertEqual(source[d:d+len(raw)],bytes(len(raw)));self.assertEqual(base[d:d+len(raw)],bytes(len(raw)));self.assertTrue(any(lo<=d and d+len(raw)<=hi for lo,hi in reserves));self.assertFalse(any(d<=t<d+len(raw) for t in targets));seen.append((d,d+len(raw)));expected.append((d,raw));payload.extend(target[d:d+size]);q=b.parse(target,d,8192,extra_glyphs=range(0xb0,0xc0));self.assertTrue(q['terminal']);self.assertFalse(q['error'])
    self.assertEqual(bytes(payload),body);self.assertEqual([len(v) for v in atoms(body)],[c['payload_size'] for c in e['chunks']]);expected.append((caller,b.pointer(int(e['chunks'][0]['destination'],16))))
    for t,occ in e['preserved_interior_occurrences'].items():
     self.assertEqual([f'{v:06X}' for v in b.pointer_index(base)[int(t,16)]],occ)
     for v in occ:
      q=int(v,16);self.assertEqual(target[q:q+4],base[q:q+4])
   seen.sort();self.assertTrue(all(a[1]<=z[0] for a,z in zip(seen,seen[1:])));self.assertEqual(records[len(prefixes[p]):],expected);self.assertEqual(b.sprite_digest(base),b.sprite_digest(target));self.assertEqual(target[0x250000:0x260000],base[0x250000:0x260000]);self.assertEqual(target[0x2021A8:0x2021A8+1584*17],base[0x2021A8:0x2021A8+1584*17]);self.assertEqual(target[0x330FC0:0x331000],base[0x330FC0:0x331000]);self.assertEqual(qualify(target,source)['items'][next(i for i,v in enumerate(qualify(target,source)['items']) if v['id']=='6E')]['help_root'],f['entries'][0]['chunks'][0]['destination']);prove(target)
   for c in read(f'tests/emulation_v78_scoped/results_{p}.json')['cases'].values():
    self.assertEqual(b.sha(target),c['base_rom_sha256']);fixture=bytearray(target)
    for w in c['temporary_rom_writes']:
     q=int(w['offset'],16);raw=bytes.fromhex(w['hex']);fixture[q:q+len(raw)]=raw
    self.assertEqual(b.sha(fixture),c['fixture_rom_sha256'])
