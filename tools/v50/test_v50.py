import bisect,json,os,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/v50'),str(ROOT/'tools/v38')]
import build_v50 as b
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
  cls.o=Path(os.environ['ROM_PATH']).read_bytes();cls.f=json.loads((ROOT/'tools/v50/v50_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v50/validation_v50.json').read_text());cls.data={}
  for p in ('accents','ascii'):
   old=(ROOT/f'patches/EarthBound_Beginnings_FR_v49_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v50_{p}.ips').read_bytes()
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
    restored=bytearray(new)
    for call in self.f['grammar']['calls']:
     q=int(call['offset'],16)
     if a<=q<z:restored[q-a:q-a+4]=b.pointer(int(call['old_target'],16))
    self.assertEqual(commands(old),commands(restored))
    before=b.parse(old,0,len(old)+1,extra_glyphs=range(0xB0,0xC0));after=b.parse(new,0,len(new)+1,extra_glyphs=range(0xB0,0xC0))
    restored_parse=b.parse(bytes(restored),0,len(restored)+1,extra_glyphs=range(0xB0,0xC0));self.assertEqual(before['refs'],restored_parse['refs']);self.assertEqual(before['end'],after['end']);self.assertFalse(after['error']);self.assertTrue(after['terminal'])
 def test_exhaustive_diff_and_previous_records(self):
  for p,d in self.data.items():
   mask=bytearray(b.SIZE)
   for a,raw in b.additions_from_fixtures(self.f,p):mask[a:a+len(raw)]=b'\1'*len(raw)
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
  self.assertEqual(len(self.f['deferred']),7)
  for e in self.f['deferred']:
   a,z=int(e['offset'],16),int(e['end'],16)
   for d in self.data.values():self.assertEqual(d['target'][a:z],d['base'][a:z])
 def test_dictionary_font_and_grammar_copies_preserved(self):
  dictionary=b.dictionary_from_rom(self.o)
  for d in self.data.values():
   self.assertEqual(d['target'][0x8CDED:0x8D9ED],d['base'][0x8CDED:0x8D9ED])
   for e in dictionary.values():
    a=int(e['offset'],16);n=len(bytes.fromhex(e['raw_hex']))+1;self.assertEqual(d['target'][a:a+n],d['base'][a:a+n])
   for e in self.f['grammar']['scripts']:
    a,z=int(e['id'],16),int(e['end'],16);self.assertEqual(d['target'][a:z],d['base'][a:z])
 def test_menu_labels_preserved(self):
  count=0
  for c in self.f['contexts']:
   a=int(c['id'],16)
   for p,d in self.data.items():
    for lo,hi in c['profiles'][p]['spans']:
     raw=d['base'][a+lo:a+hi]
     if raw in [b.encode(x,p) for x in ('Yes','No','Store','Take out','Heal','Sleep')]:
      self.assertEqual(d['target'][a+lo:a+hi],raw);count+=1
  self.assertGreater(count,0)
 def test_reject_wrong_original(self):
  bad=bytearray(self.o);bad[100]^=1
  with self.assertRaisesRegex(ValueError,'ROM originale'):b.fixtures_from_baselines(bad,{p:d['base'] for p,d in self.data.items()})
 def test_grammar_reserve_and_original_callers(self):
  a,z=(int(q,16) for q in self.f['grammar']['reserve'])
  for p,d in self.data.items():
   self.assertEqual(self.o[a:z],bytes(z-a));self.assertEqual(d['base'][a:z],bytes(z-a))
   self.assertFalse(any(q<z and q+len(raw)>a for q,raw in b.records(d['old'])))
   self.assertFalse(any(a<=t<z for t in b.pointer_index(d['base'])))
   allowed={int(e['offset'],16) for e in self.f['grammar']['calls']}
   idx=b.pointer_index(d['base'])
   for helper in b.HELPERS:
    for q in idx.get(helper,[]):
     if q not in allowed:self.assertEqual(d['target'][q:q+4],d['base'][q:q+4])
 def test_scoped_calls_and_both_gender_branches(self):
  for p,d in self.data.items():
   copies={e['id']:e for e in self.plan['profiles'][p]['grammar_copies']}
   for call in self.f['grammar']['calls']:
    q=int(call['offset'],16);root=int(call['root'],16);old=int(call['old_target'],16)
    self.assertIn((q,old),b.parse(d['base'],root,8192,extra_glyphs=range(0xB0,0xC0))['refs'])
    self.assertEqual(d['target'][q:q+4],b.pointer(int(copies[call['old_target']]['offset'],16)))
   for ident,word in (('07E660','sa'),('07E66B','sa'),('35C758','son'),('35C764','son')):
    e=copies[ident];a=int(e['offset'],16);raw=d['target'][a:a+e['length']]
    parsed=b.parse(raw,0,len(raw)+1);self.assertFalse(parsed['error']);self.assertTrue(parsed['terminal'])
    self.assertEqual([raw[x:y] for x,y in b.spans_fr(raw)],[b.encode(word,p)])
    for r in e['internal_refs']:
     q=int(r['offset'],16);self.assertEqual(d['target'][q:q+4],b.pointer(int(copies[r['old_target']]['offset'],16)))
    restored=bytearray(raw)
    for r in e['internal_refs']:
     q=int(r['offset'],16)-a;restored[q:q+4]=b.pointer(int(r['old_target'],16))
    source=bytes.fromhex(next(x['raw_hex'] for x in self.f['grammar']['scripts'] if x['id']==ident))
    self.assertEqual([v for _,v in commands(source)],[v for _,v in commands(restored)])
 def test_all_21_v49_protections_remain(self):
  previous=json.loads((ROOT/'tools/v49/v49_fixtures.json').read_text())
  self.assertEqual(len(previous['deferred']),21)
  for e in previous['deferred']:
   a,z=int(e['offset'],16),int(e['end'],16)
   for d in self.data.values():self.assertEqual(d['target'][a:z],d['base'][a:z])
if __name__=='__main__':unittest.main()
