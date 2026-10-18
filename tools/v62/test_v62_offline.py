import json,sys,unittest
from pathlib import Path
import runtime as b
from opcode_proof import ANCHORS,prove
from parser_v62 import length,parse,spans_fr
import build_v61 as historical
class Offline(unittest.TestCase):
 def test_extension_has_no_operand_and_returns_to_immediately_following_command(self):
  raw=b'\x1a\x21\x1b\x02'+b.pointer(0x37C098)+b'\x02';p=parse(raw,0,len(raw)+1)
  self.assertEqual(length(raw,0),2);self.assertTrue(p['terminal']);self.assertFalse(p['error']);self.assertEqual(p['refs'],[(4,0x37C098)]);self.assertEqual(p['end'],len(raw));self.assertEqual(spans_fr(raw),[])
 def test_historical_parser_remains_strict_and_unmodified(self):
  raw=b'\x1a\x21\x02';self.assertIn('1A 21',historical.parse(raw,0,4)['error']);self.assertTrue(parse(raw,0,4)['terminal'])
 def test_unknown_neighbor_still_rejected(self):
  self.assertIn('1A 22',parse(b'\x1a\x22\x02',0,4)['error'])
 def test_parameter_bytes_not_reinterpreted_as_commands(self):
  raw=b'\x0d\x21\x1a\x21\x02';p=parse(raw,0,6);self.assertEqual(p['end'],5);self.assertFalse(p['error']);self.assertEqual(b.commands(raw),raw)
 def test_truncated_opcode_still_rejected(self):
  p=parse(b'\x1a',0,2);self.assertTrue(p['error']);self.assertFalse(p['terminal'])
 def test_every_engine_anchor_enforced(self):
  data=bytearray(b.SIZE)
  for a,h in ANCHORS.values():data[a:a+len(bytes.fromhex(h))]=bytes.fromhex(h)
  self.assertEqual(prove(data)['operand_bytes'],0)
  for label,(a,h) in ANCHORS.items():
   damaged=bytearray(data);damaged[a]^=1
   with self.assertRaisesRegex(ValueError,label):prove(damaged)
 def test_metadata_keeps_gameplay_limits_explicit(self):
  for name in ('alias_audit_v62.json','alias_audit_v62_ascii.json'):
   x=json.loads((b.ROOT/'tools/v62'/name).read_text());self.assertFalse(x['natural_access_verified']);self.assertFalse(x['computed_callers_covered']);self.assertFalse(x['word_check_is_language_proof']);self.assertEqual(x['opcode_proof']['length_bytes'],2)
if __name__=='__main__':unittest.main()
