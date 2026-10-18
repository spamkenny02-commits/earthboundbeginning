import copy,json,unittest
from pathlib import Path
import build_v58 as b
ROOT=b.ROOT
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v58/v58_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v58/validation_v58.json').read_text())
 def test_inventory(self):
  self.assertEqual((len(self.f['edits']),len(self.f['contexts']),self.plan['new_text_fragments']),(20,14,33))
  self.assertFalse(self.plan['natural_scene_access_verified']);self.assertEqual(self.plan['literal_reference_operands_rewritten'],0)
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v57_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v58_{p}.ips').read_bytes()
   self.assertEqual(new,b.append(old,b.additions_from_fixtures(self.f,p)));self.assertEqual(b.sha(new),self.plan['profiles'][p]['sha256'])
 def test_reject_unsafe_entry(self):
  f=copy.deepcopy(self.f);f['edits'][0]['interior_targets'].append(f"{int(f['edits'][0]['offset'],16)+4:06X}")
  with self.assertRaisesRegex(ValueError,'intérieure'):b.additions_from_fixtures(f,'accents')
 def test_reject_overflow(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr'][0]='A'*1000
  with self.assertRaisesRegex(ValueError,'trop longue'):b.additions_from_fixtures(f,'accents')
 def test_reject_overlap(self):
  f=copy.deepcopy(self.f);f['edits'].append(f['edits'][0])
  with self.assertRaisesRegex(ValueError,'chevauchement'):b.additions_from_fixtures(f,'accents')
 def test_reject_bad_source_capacity(self):
  f=copy.deepcopy(self.f);f['edits'][0]['profiles']['accents']['baseline_hex']='50'
  with self.assertRaisesRegex(ValueError,'Capacité'):b.additions_from_fixtures(f,'accents')
 def test_reject_outside_reserve(self):
  f=copy.deepcopy(self.f);f['edits'][0]['copy_offset']='200000'
  with self.assertRaisesRegex(ValueError,'hors réserve'):b.additions_from_fixtures(f,'accents')
 def test_terminal_directions_preserve_return_without_crossing_next_entry(self):
  entries=[e for e in self.f['edits'] if e['offset'].startswith('09F9') and int(e['offset'],16)>=0x09F990]
  self.assertEqual(len(entries),8)
  for e in entries:
   for p in ('accents','ascii'):
    raw=b.copy_text(e,p);parsed=b.parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
    self.assertEqual(parsed['end'],len(raw));self.assertTrue(parsed['terminal']);self.assertFalse(parsed['error'])
    self.assertEqual(b.commands(raw),b'\x02')
 def test_reject_branch_command_in_run(self):
  with self.assertRaisesRegex(ValueError,'non permi'):b.text_layout(b.encode('@Texte','accents')+b'\x08'+b.pointer(0x350000)+b.encode('suite','accents'))
 def test_reject_fragment_count_mismatch(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr']=[]
  with self.assertRaisesRegex(ValueError,'Nombre'):b.additions_from_fixtures(f,'accents')
 def test_only_tail_jumps_no_calls_in_additions(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
    edits=dict(b.additions_from_fixtures(self.f,p));self.assertEqual(edits[a],b'\x0a'+b.pointer(d));self.assertEqual(edits[d],b.copy_text(e,p)+b'\x0a'+b.pointer(z))
 def test_reject_unapproved_effect_command(self):
  raw=b.encode('@Texte','accents')+b'\x1f\x02\x44'+b.encode('suite','accents')
  with self.assertRaises(ValueError):b.text_layout(raw)
 def test_reject_branch_subcommand(self):
  raw=b.encode('@Texte','accents')+b'\x1b\x03'+b.pointer(0x350000)+b.encode('suite','accents')
  with self.assertRaises(ValueError):b.text_layout(raw)
 def test_retained_marker_not_counted_as_translation(self):
  self.assertEqual(self.plan['retained_text_fragments'],1)
  unchanged=[a for e in self.f['edits'] for a,c in zip(e['profiles']['accents']['english_or_prior_french'],e['fr']) if a==c]
  self.assertEqual(unchanged,['@'])
 def test_reject_undeclared_grammar_call(self):
  e=copy.deepcopy(next(e for e in self.f['edits'] if e.get('possessive_call')));e['possessive_call']=False
  with self.assertRaisesRegex(ValueError,'non déclaré'):b.copy_text(e,'accents')
 def test_reject_other_grammar_target(self):
  e=copy.deepcopy(next(e for e in self.f['edits'] if e.get('possessive_call')))
  raw=bytes.fromhex(e['profiles']['accents']['baseline_hex']);e['profiles']['accents']['baseline_hex']=raw.replace(b.pointer(b.GRAMMAR_OLD),b.pointer(0x350000)).hex()
  with self.assertRaisesRegex(ValueError,'non permis'):b.copy_text(e,'accents')
 def test_reject_sprite_zero_hole_even_if_fixture_claims_it_is_free(self):
  f=copy.deepcopy(self.f);f['edits'][0]['copy_offset']='256BA0';f['reserves'].append(['256000','257000'])
  with self.assertRaisesRegex(ValueError,'hors réserve'):b.additions_from_fixtures(f,'accents')
 def test_three_scoped_helpers_agree_with_french_noun(self):
  cases={'097CD2':'sa','097EFB':'sa','09F89F':'son'}
  for offset,word in cases.items():
   e=next(e for e in self.f['edits'] if e['offset']==offset)
   for p in ('accents','ascii'):
    raw=b.copy_text(e,p)+b'\x02';refs=b.parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))['refs']
    self.assertEqual([t for q,t in refs],[b.GRAMMAR_HELPERS[word][0]])
    self.assertEqual(bytes.fromhex(b.GRAMMAR_HELPERS[word][1]),b.encode(word,p)+b'\x02')
 def test_reject_non_name_19_command_in_run(self):
  with self.assertRaises(ValueError):
   b.text_layout(b.encode('@Texte','accents')+b'\x19\x02'+b.encode('suite','accents'))
if __name__=='__main__':unittest.main()
