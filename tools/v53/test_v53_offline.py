import copy,json,unittest
import build_v53 as b
ROOT=b.ROOT
class Offline(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((ROOT/'tools/v53/v53_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v53/validation_v53.json').read_text())
  cls.synthetic=bytearray(b.SIZE)
  for e in cls.f['engine_proof']:
   a=int(e['offset'],16);raw=bytes.fromhex(e['raw_hex']);cls.synthetic[a:a+len(raw)]=raw
  for e in cls.f['edits']:
   if e['mode']=='npc_copy':
    p=e['npc_field_proof'];a=int(p['record_offset'],16);cls.synthetic[a:a+17]=bytes.fromhex(p['record_hex'])
 def test_inventory(self):
  self.assertEqual(len(self.f['edits']),4);self.assertEqual(self.plan['npc_copies'],3);self.assertEqual(self.plan['new_text_fragments'],4);self.assertFalse(self.plan['natural_scene_access_verified'])
 def test_exact_patch_rebuild(self):
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v52_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v53_{p}.ips').read_bytes()
   self.assertEqual(new,b.append(old,b.additions_from_fixtures(self.f,p)));self.assertEqual(b.sha(new),self.plan['profiles'][p]['sha256'])
 def test_npc_commands_preserved(self):
  for p in ('accents','ascii'):
   for e in self.f['edits']:
    if e['mode']=='npc_copy':self.assertEqual(b.commands(b.copy_bytes(e,p)),b.commands(bytes.fromhex(e['profiles'][p]['baseline_hex'])))
 def test_exclusive_end_branch_targets_not_remapped(self):
  for ident in ('33F3EE','3609EB'):
   e=next(e for e in self.f['edits'] if e['id']==ident)
   for p in ('accents','ascii'):
    out=b.copy_bytes(e,p);self.assertIn(int(e['end'],16),b.parse(out,0,len(out)+1,extra_glyphs=range(0xB0,0xC0))['targets'])
 def test_reject_bad_npc_field_metadata(self):
  f=copy.deepcopy(self.f);f['edits'][0]['npc_field_proof']['field_offset']=12
  with self.assertRaisesRegex(ValueError,'Champ NPC'):b.additions_from_fixtures(f,'accents')
 def test_reject_overflow(self):
  f=copy.deepcopy(self.f);f['edits'][0]['fr']='A'*1000
  with self.assertRaisesRegex(ValueError,'trop longue'):b.additions_from_fixtures(f,'accents')
 def test_reject_overlap(self):
  f=copy.deepcopy(self.f);f['edits'].append(f['edits'][0])
  with self.assertRaisesRegex(ValueError,'chevauchement'):b.additions_from_fixtures(f,'accents')
 def test_reject_outside_reserve(self):
  f=copy.deepcopy(self.f);f['edits'][0]['copy_offset']='200000'
  with self.assertRaisesRegex(ValueError,'hors réserve'):b.additions_from_fixtures(f,'accents')
 def test_reject_bad_source_capacity(self):
  f=copy.deepcopy(self.f);f['edits'][0]['end']='33F443'
  with self.assertRaisesRegex(ValueError,'Capacité'):b.additions_from_fixtures(f,'accents')
 def test_ten_distinct_engine_references(self):
  self.assertEqual(len({e['offset'] for e in self.f['engine_proof']}),10)
  self.assertEqual(b.engine_table_proof(self.synthetic,self.f['config']),self.f['engine_proof'])
 def test_reject_bad_asm_opcode(self):
  data=bytearray(self.synthetic);data[0x131CA]=0xEA
  with self.assertRaisesRegex(ValueError,'Structure ASM'):b.engine_table_proof(data,self.f['config'])
 def test_reject_changed_engine_table(self):
  data=bytearray(self.synthetic);data[0x131CB]^=1
  with self.assertRaisesRegex(ValueError,'Table NPC'):b.engine_table_proof(data,self.f['config'])
 def test_reject_bad_xl_opcode(self):
  data=bytearray(self.synthetic);data[0xC32E]=0xEA
  with self.assertRaisesRegex(ValueError,'Structure XL'):b.engine_table_proof(data,self.f['config'])
 def test_reject_non_field_slot(self):
  with self.assertRaisesRegex(ValueError,'Hors champ'):b.npc_field_proof(self.synthetic,0x205C00,0x33F3EE,self.f['config'])
 def test_reject_wrong_npc_destination(self):
  with self.assertRaisesRegex(ValueError,'Destination NPC'):b.npc_field_proof(self.synthetic,0x205BFF,0x33F3EF,self.f['config'])
 def test_reject_invalid_npc_record(self):
  data=bytearray(self.synthetic);data[0x205BFF-9]=0xFF
  with self.assertRaisesRegex(ValueError,'Enregistrement NPC'):b.npc_field_proof(data,0x205BFF,0x33F3EE,self.f['config'])
if __name__=='__main__':unittest.main()
