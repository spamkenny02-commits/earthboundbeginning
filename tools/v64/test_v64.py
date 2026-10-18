import json,os,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'v62'))
import runtime as b
from build_v64 import CONFIG
from audit_bank import audit
@unittest.skipUnless(os.environ.get('ROM_PATH'),'ROM_PATH required')
class ROMTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=Path(os.environ['ROM_PATH']).read_bytes();assert b.sha(cls.source)==b.ROM_SHA
 def test_only_four_authorized_text_ranges_change(self):
  plan=json.loads((b.ROOT/'tools/v64/validation_v64.json').read_text())
  for p in ('accents','ascii'):
   old=(b.ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes();new=(b.ROOT/f'patches/EarthBound_Beginnings_FR_v64_{p}.ips').read_bytes()
   before=b.apply(self.source,b.records(old));after=b.apply(self.source,b.records(new));self.assertEqual(b.sha(new),plan['profiles'][p]['sha256']);self.assertEqual(b.sha(after),plan['profiles'][p]['target_rom_sha256'])
   self.assertEqual(b.records(new)[:len(b.records(old))],b.records(old));changes=b.records(new)[len(b.records(old)):];self.assertEqual(len(changes),4)
   mask=bytearray(len(after))
   for (r,a,z,en,fr),(offset,raw) in zip(CONFIG,changes):
    r,a,z=int(r,16),int(a,16),int(z,16);self.assertEqual(offset,a);self.assertEqual(len(raw),z-a);mask[a:z]=b'\1'*(z-a)
    self.assertEqual(b.decode(before[a:z],b.dictionary_from_rom(self.source)),en)
    expected=b.encode(fr,p)+b.encode(' ',p)*(z-a-len(b.encode(fr,p)));self.assertEqual(after[a:z],expected)
    end=b.parse(before,r,8192,extra_glyphs=range(0xB0,0xC0))['end'];self.assertEqual(b.commands(before[r:end]),b.commands(after[r:end]))
   self.assertTrue(all(x==y or m for x,y,m in zip(before,after,mask)));self.assertEqual(len(before),len(after));self.assertEqual(b.sprite_digest(before),b.sprite_digest(after))
 def test_atm_graph_reproduces_and_contains_no_previous_english_prompts(self):
  for p in ('accents','ascii'):
   data=b.apply(self.source,b.records((b.ROOT/f'patches/EarthBound_Beginnings_FR_v64_{p}.ips').read_bytes()));actual=audit(self.source,data,p);expected=json.loads((b.ROOT/f'tools/v64/bank_audit_{p}.json').read_text());self.assertEqual(actual,expected)
   texts=[s['text'] for n in actual['nodes'] for s in n['spans']]
   self.assertFalse(any('Please' in s or 'Balance' in s for s in texts));self.assertEqual(actual['unparsed_roots'],[])
if __name__=='__main__':unittest.main()
