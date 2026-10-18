import json,os,unittest
from pathlib import Path
import runtime as b
import build_v61 as historical
from opcode_proof import prove
from audit_aliases_v62 import audit
@unittest.skipUnless(os.environ.get('ROM_PATH'),'ROM_PATH required')
class ROM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=Path(os.environ['ROM_PATH']).read_bytes();assert b.sha(cls.source)==b.ROM_SHA;cls.targets={p:b.apply(cls.source,b.records((b.ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes())) for p in ('accents','ascii')}
 def test_original_and_both_profiles_have_the_proven_handler(self):
  expected=prove(self.source)
  for data in self.targets.values():self.assertEqual(prove(data),expected)
 def test_previously_blocked_routines_close_and_preserve_exact_bytes(self):
  for data in self.targets.values():
   for a,end,refs in ((0x37C079,0x37C093,[0x37C098,0x37C09D]),(0x37C100,0x37C123,[0x37C128])):
    old=historical.parse(data,a,8192,extra_glyphs=range(0xB0,0xC0));new=b.parse(data,a,8192,extra_glyphs=range(0xB0,0xC0));self.assertIn('1A 21',old['error']);self.assertTrue(new['terminal']);self.assertFalse(new['error']);self.assertEqual(new['end'],end);self.assertEqual([t for q,t in new['refs']],refs);self.assertEqual(b.spans_fr(data[a:end]),[]);self.assertEqual(b.commands(data[a:end]),data[a:end])
 def test_reproduce_complete_audits_for_both_profiles(self):
  for p,data in self.targets.items():
   filename='alias_audit_v62.json' if p=='accents' else 'alias_audit_v62_ascii.json';expected=json.loads((b.ROOT/'tools/v62'/filename).read_text());actual=audit(self.source,data);actual['profile']=p;self.assertEqual(actual,expected)
 def test_newly_followed_paths_add_no_text_and_no_unparsed_root(self):
  old=json.loads((b.ROOT/'tools/v61/alias_audit_v61.json').read_text());new=audit(self.source,self.targets['accents']);self.assertEqual(new['nonmenu_text_spans_examined'],old['nonmenu_text_spans_examined']);self.assertEqual(new['unchanged_candidates'],old['unchanged_candidates']);self.assertEqual(new['unparsed_roots'],[]);self.assertEqual(new['preserved_ranges_with_graph_edges'],[]);self.assertEqual(new['visited_roots']-old['visited_roots'],6);self.assertEqual(new['parsed_edges']-old['parsed_edges'],11)
if __name__=='__main__':unittest.main()
