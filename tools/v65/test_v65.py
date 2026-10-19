import json,os,unittest
from pathlib import Path
from build_v65 import ROOT,b,CALL,CALLS,RETURN_CALL,HELPER,EMPTY,TEXT,END,location,graph
from safe_storage import safe_reserves
from parser_v62 import length

@unittest.skipUnless(os.environ.get('ROM_PATH'),'ROM_PATH required')
class ROMTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=Path(os.environ['ROM_PATH']).read_bytes();assert b.sha(cls.source)==b.ROM_SHA
  cls.f=json.loads((ROOT/'tools/v65/v65_fixtures.json').read_text());cls.plan=json.loads((ROOT/'tools/v65/validation_v65.json').read_text())
  cls.priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v64_{p}.ips').read_bytes() for p in ('accents','ascii')}
  cls.bases={p:b.apply(cls.source,b.records(ips)) for p,ips in cls.priors.items()}
  cls.targets={p:b.apply(cls.source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v65_{p}.ips').read_bytes())) for p in cls.bases}
 def test_only_scoped_call_copy_and_confirmation_change(self):
  for p,base in self.bases.items():
   ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v65_{p}.ips').read_bytes();records=b.records(ips);prior=b.records(self.priors[p]);self.assertEqual(records[:len(prior)],prior);changes=records[len(prior):];self.assertEqual(len(changes),self.plan['profiles'][p]['records_added'])
   self.assertEqual(b.sha(ips),self.plan['profiles'][p]['sha256']);self.assertEqual(b.sha(self.targets[p]),self.plan['profiles'][p]['target_rom_sha256']);self.assertEqual(len(base),len(self.targets[p]))
   mask=bytearray(len(base))
   for a,v in changes:mask[a:a+len(v)]=b'\1'*len(v)
   self.assertTrue(all(x==y or m for x,y,m in zip(base,self.targets[p],mask)))
   self.assertEqual(self.targets[p][0x38B54B:0x38B5A2],base[0x38B54B:0x38B5A2]);self.assertEqual(self.targets[p][0x250000:0x260000],base[0x250000:0x260000]);self.assertEqual(b.sprite_digest(self.targets[p]),b.sprite_digest(base))
 def test_all_article_choices_keep_classifier_and_return_without_english(self):
  dest=int(self.f['copy_offset'],16)
  for p,data in self.targets.items():
   for call in CALLS:
    actual=location(self.f,call);self.assertEqual(data[actual:actual+4],b.pointer(dest))
   raw=data[dest:dest+27];old=self.bases[p][HELPER:HELPER+27]
   parsed=b.parse(data,dest,8192,extra_glyphs=range(0xB0,0xC0));self.assertFalse(parsed['error']);self.assertEqual(parsed['end'],dest+27);self.assertEqual(parsed['refs'],[(dest+q,EMPTY) for q in (6,10,14,18,22)]);self.assertEqual(data[EMPTY:EMPTY+1],b'\x02')
   normalized=bytearray(raw)
   for q in (6,10,14,18):normalized[q:q+4]=old[q:q+4]
   self.assertEqual(bytes(normalized),old)
   for r,parsed in graph(self.bases[p]).items():
    node=next((n for n in self.f['moved_scripts'] if int(n['root'],16)==r),None)
    if node:context=bytearray(b''.join(data[int(c['destination'],16):int(c['destination'],16)+int(c['source_end'],16)-int(c['source_start'],16)] for c in node['chunks']))
    else:context=bytearray(data[r:parsed['end']])
    for q,t in parsed['refs']:context[q-r:q-r+4]=b.pointer(t)
    self.assertEqual(b.commands(bytes(context)),b.commands(self.bases[p][r:parsed['end']]))
    if node:self.assertEqual(bytes(context),self.bases[p][r:parsed['end']])
 def test_copy_is_safe_padding_outside_prior_records_sprites_and_probe_slot(self):
  targets=set(b.pointer_index(self.source))
  for data in self.bases.values():targets.update(b.pointer_index(data))
  targets.update(range(0x330FC0,0x331000));reserves,storage=safe_reserves(self.source,self.bases,self.priors,targets,b.records)
  self.assertEqual(storage,self.f['storage']);dest=int(self.f['copy_offset'],16);self.assertTrue(any(a<=dest and dest+27<=z for a,z in reserves))
  for data in self.bases.values():self.assertEqual(data[dest:dest+27],bytes(27))
  for node in self.f['moved_scripts']:
   for c in node['chunks']:
    a=int(c['destination'],16);size=int(c['source_end'],16)-int(c['source_start'],16)+(5 if c['continuation'] else 0);self.assertTrue(any(lo<=a and a+size<=hi for lo,hi in reserves))
    for data in self.bases.values():self.assertEqual(data[a:a+size],bytes(size))
    for data in self.targets.values():
     if c['continuation']:self.assertEqual(data[a+size-5:a+size],b'\x0a'+b.pointer(int(c['continuation'],16)))
 def test_doctor_you_have_is_command_data_not_a_text_span(self):
  expected=bytes.fromhex('0300180a1c04101e1a150d00')
  for p,data in self.targets.items():
   self.assertEqual(data[0x24D4E0:0x24D4EC],expected);self.assertEqual(data[0x24D4E0:0x24D4EC],self.bases[p][0x24D4E0:0x24D4EC]);self.assertEqual(length(data,0x24D4E8),2);self.assertEqual(length(data,0x24D4EA),2)
   root=0x24D4A0;end=b.parse(data,root,8192,extra_glyphs=range(0xB0,0xC0))['end'];spans=b.spans_fr(data[root:end]);self.assertFalse(any(root+a<=0x24D4E9<root+z for a,z in spans))
if __name__=='__main__':unittest.main()
