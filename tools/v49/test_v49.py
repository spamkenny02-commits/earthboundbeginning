import bisect,json,os,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/v49'),str(ROOT/'tools/v38')]
import build_v49 as b
from test_v38 import independent_apply

def commands(raw):
 p=0;out=[]
 while p<len(raw):
  c=raw[p]
  if 0x50<=c<0xC0 or c in (0xC8,0xC9,0xCA,0xCB):p+=1;continue
  if c in (0x15,0x16,0x17):p+=2;continue
  n=b.length(raw,p);out.append((p,raw[p:p+n]));p+=n
 return out

class Rom(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.o=Path(os.environ['ROM_PATH']).read_bytes();cls.f=json.loads((ROOT/'tools/v49/v49_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v49/validation_v49.json').read_text());cls.data={}
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v48_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v49_{p}.ips').read_bytes()
   cls.data[p]={'old':old,'new':new,'base':independent_apply(cls.o,old),'target':independent_apply(cls.o,new)}
 def test_original_and_regenerated_provenance(self):
  self.assertEqual(len(self.o),b.SIZE);self.assertEqual(b.sha(self.o),b.ROM_SHA)
  f=b.fixtures_from_baselines(self.o,{p:d['base'] for p,d in self.data.items()})
  # JSON converts span tuples into lists.
  self.assertEqual(json.loads(json.dumps(f)),self.f)
 def test_independent_ips_and_hashes(self):
  for p,d in self.data.items():
   self.assertEqual(b.sha(d['old']),b.BASE_SHA[p]);self.assertEqual(b.sha(d['new']),self.plan['profiles'][p]['sha256']);self.assertEqual(b.sha(d['target']),self.plan['profiles'][p]['target_rom_sha256']);self.assertEqual(d['target'],b.apply(self.o,b.records(d['new'])))
 def test_every_edit_is_original_english_and_a_complete_span(self):
  dictionary=b.dictionary_from_rom(self.o);contexts={e['id']:e for e in self.f['contexts']}
  for e in self.f['edits']:
   a,z=int(e['offset'],16),int(e['end'],16);src=bytes.fromhex(e['source_hex'])
   self.assertEqual(self.o[a:z],src);self.assertEqual(b.decode(src,dictionary),e['english'])
   for p,d in self.data.items():
    self.assertEqual(d['base'][a:z],src)
    for root in e['contexts']:
     c=contexts[root];start=int(root,16)
     self.assertIn([a-start,z-start],c['profiles'][p]['spans'])
 def test_full_contexts_commands_and_all_branch_operands_unchanged(self):
  for e in self.f['contexts']:
   a=int(e['id'],16)
   for p,d in self.data.items():
    z=int(e['profiles'][p]['end'],16);old=d['base'][a:z];new=d['target'][a:z]
    self.assertEqual(old,bytes.fromhex(e['profiles'][p]['baseline_hex']))
    self.assertEqual(commands(old),commands(new))
    before=b.parse(old,0,len(old)+1,extra_glyphs=range(0xB0,0xC0));after=b.parse(new,0,len(new)+1,extra_glyphs=range(0xB0,0xC0))
    self.assertEqual(before['refs'],after['refs']);self.assertEqual(before['end'],after['end']);self.assertFalse(after['error']);self.assertTrue(after['terminal'])
 def test_exhaustive_diff_and_previous_records(self):
  for p,d in self.data.items():
   mask=bytearray(b.SIZE)
   for e in self.f['edits']:
    a,z=int(e['offset'],16),int(e['end'],16);mask[a:z]=b'\1'*(z-a)
   self.assertTrue(all(a==z for a,z,m in zip(d['base'],d['target'],mask) if not m))
   old,new=b.records(d['old']),b.records(d['new']);self.assertEqual(new[:len(old)],old)
   for a,raw in old:self.assertTrue(all(d['target'][q]==d['base'][q] for q in range(a,a+len(raw)) if not mask[q]))
 def test_independent_french_decode_padding_and_glyphs(self):
  for p,d in self.data.items():
   for e in self.f['edits']:
    a,z=int(e['offset'],16),int(e['end'],16);raw=d['target'][a:z]
    self.assertTrue(all(0x50<=c<0xC0 for c in raw))
    actual=''.join(b.ACCENTS[c-0xB0] if 0xB0<=c<0xC0 else chr(c-48) for c in raw)
    import unicodedata
    expected=e['fr'] if p=='accents' else ''.join(c for c in unicodedata.normalize('NFD',e['fr']) if not unicodedata.combining(c))
    self.assertEqual(actual,expected.ljust(z-a))
 def test_existing_french_and_other_text_spans_preserved(self):
  edits={(int(e['offset'],16),int(e['end'],16)) for e in self.f['edits']}
  for c in self.f['contexts']:
   a=int(c['id'],16)
   for p,d in self.data.items():
    for lo,hi in c['profiles'][p]['spans']:
     if (a+lo,a+hi) not in edits:self.assertEqual(d['target'][a+lo:a+hi],d['base'][a+lo:a+hi])
 def test_no_pointer_enters_an_edited_text_interior(self):
  targets=sorted(set(b.pointer_index(self.o))|set().union(*(set(b.pointer_index(d['base'])) for d in self.data.values())))
  for e in self.f['edits']:
   a,z=int(e['offset'],16),int(e['end'],16);i=bisect.bisect_right(targets,a)
   self.assertTrue(i==len(targets) or targets[i]>=z,e)
 def test_deferred_texts_and_references_preserved(self):
  self.assertEqual(len(self.f['deferred']),21)
  for e in self.f['deferred']:
   a,z=int(e['offset'],16),int(e['end'],16)
   for d in self.data.values():self.assertEqual(d['target'][a:z],d['base'][a:z])
 def test_dictionary_font_and_grammar_copies_preserved(self):
  dictionary=b.dictionary_from_rom(self.o)
  for d in self.data.values():
   self.assertEqual(d['target'][0x8CDED:0x8D9ED],d['base'][0x8CDED:0x8D9ED])
   for e in dictionary.values():
    a=int(e['offset'],16);n=len(bytes.fromhex(e['raw_hex']))+1;self.assertEqual(d['target'][a:a+n],d['base'][a:a+n])
   # New writes are all in the main text banks; no grammar copy is there.
   for a,z in ((0x250000,0x260000),(0x320000,0x330000)):
    self.assertEqual(d['target'][a:z],d['base'][a:z])
 def test_menu_labels_preserved(self):
  count=0
  for c in self.f['contexts']:
   a=int(c['id'],16)
   for p,d in self.data.items():
    for lo,hi in c['profiles'][p]['spans']:
     raw=d['base'][a+lo:a+hi]
     if raw in [b.encode(x,p) for x in ('Yes','No','Store','Take out','Heal','Sleep')]:
      self.assertEqual(d['target'][a+lo:a+hi],raw);count+=1
  self.assertGreater(count,50)
 def test_reject_wrong_original(self):
  bad=bytearray(self.o);bad[100]^=1
  with self.assertRaisesRegex(ValueError,'ROM originale'):b.fixtures_from_baselines(bad,{p:d['base'] for p,d in self.data.items()})
if __name__=='__main__':unittest.main()
