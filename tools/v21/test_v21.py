"""V21: unit checks plus independent IPS interpreter on original ROM."""
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import ROM_SHA, encode, read_translations, pointer_index
from build_v21 import get_candidates

ROM_PATH=Path(os.environ['ROM_PATH']) if os.environ.get('ROM_PATH') else None
IPS_DIR=Path(os.environ.get('V21_OUT',str(ROOT/'build_v21')))

def independent_ips(data,rom):
    if not data.startswith(b'PATCH'):raise ValueError('header')
    result=bytearray(rom);i=5; entries=[]
    while True:
        if i+3>len(data):raise ValueError('EOF missing')
        if data[i:i+3]==b'EOF':
            if i+3!=len(data):raise ValueError('trailer')
            return bytes(result),entries
        if i+5>len(data):raise ValueError('record header')
        pos=int.from_bytes(data[i:i+3],'big');n=int.from_bytes(data[i+3:i+5],'big');i+=5
        if n:
            if i+n>len(data):raise ValueError('record payload')
            payload=data[i:i+n];i+=n
        else:
            if i+3>len(data):raise ValueError('rle payload')
            count=int.from_bytes(data[i:i+2],'big');value=data[i+2];i+=3
            if not count:raise ValueError('zero rle')
            payload=bytes((value,))*count
        if pos+len(payload)>len(result):raise ValueError('out of bounds')
        result[pos:pos+len(payload)]=payload
        entries.append((pos,payload))

class V21Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries=json.loads((ROOT/'tools/v21/v21_dialogues_fr.json').read_text())['entries']
        cls.translations=read_translations(ROOT/'tools/v21/translations_v21.tsv')
        cls.validation=json.loads((ROOT/'tools/v21/validation_v21.json').read_text())
        cls.rom=ROM_PATH.read_bytes() if ROM_PATH else None

    def test_153_real_changes(self):
        self.assertEqual(len(self.entries),153)
        self.assertEqual(len(self.translations),153)
        self.assertEqual(set(self.translations),{e['id'] for e in self.entries})
        self.assertTrue(all(e['fr']!=e['english'] for e in self.entries))

    def test_manifest_is_source_consistent(self):
        candidates=get_candidates()
        for e in self.entries:
            with self.subTest(id=e['id']):
                self.assertEqual(e['fr'],self.translations[e['id']])
                self.assertEqual({k:v for k,v in e.items() if k!='fr'},candidates[e['id']])

    def test_all_fit_both_encodings(self):
        for e in self.entries:
            for profile in ('accents','ascii'):
                with self.subTest(id=e['id'],profile=profile):
                    self.assertLessEqual(len(encode(e['fr'],profile)),e['text_length'])

    def test_no_duplicate_prior_translations(self):
        old={e['id'] for e in json.loads((ROOT/'tools/v18_work/v18_work_dialogues_fr.json').read_text())['entries']}
        old|={e['id'] for e in json.loads((ROOT/'tools/v19/v19_dialogues_fr.json').read_text())['entries']}
        old|={e['id'] for e in json.loads((ROOT/'tools/v20/v20_dialogues_fr.json').read_text())['entries']}
        self.assertFalse(set(self.translations)&old)

    def test_invalid_ips_rejected(self):
        for b in (b'',b'PATCHEOFxx',b'PATCH\0\0\1\0\3A',b'PATCH\0\0\1\0\0\0\0ZEOF'):
            with self.subTest(b=b),self.assertRaises(ValueError):
                independent_ips(b,b'\0'*64)

    def test_original_rom_hash(self):
        if self.rom is None:self.skipTest('ROM_PATH non fourni')
        self.assertEqual(hashlib.sha256(self.rom).hexdigest(),ROM_SHA)

    def test_two_profiles_roundtrip_and_prefix(self):
        if self.rom is None:self.skipTest('ROM_PATH non fourni')
        for profile in ('accents','ascii'):
            with self.subTest(profile=profile):
                prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v20_{profile}.ips').read_bytes()
                current=(IPS_DIR/f'EarthBound_Beginnings_FR_v21_{profile}.ips').read_bytes()
                self.assertEqual(current[:len(prior)-3],prior[:-3])
                base,base_entries=independent_ips(prior,self.rom)
                result,all_entries=independent_ips(current,self.rom)
                self.assertEqual(all_entries[:len(base_entries)],base_entries)
                self.assertEqual(len(all_entries)-len(base_entries),153)
                self.assertEqual(hashlib.sha256(current).hexdigest(),self.validation['profiles'][profile]['sha256'])
                expected=bytearray(base)
                for e in self.entries:
                    p=int(e['id'],16)+1;n=e['text_length']
                    expected[p:p+n]=encode(e['fr'],profile).ljust(n,b'\x50')
                self.assertEqual(result,bytes(expected))
                self.assertEqual(hashlib.sha256(result).hexdigest(),self.validation['profiles'][profile]['target_rom_sha256'])

    def test_english_commands_and_pointers(self):
        if self.rom is None:self.skipTest('ROM_PATH non fourni')
        refs=pointer_index(self.rom)
        for e in self.entries:
            p=int(e['id'],16);n=e['text_length']
            with self.subTest(id=e['id']):
                self.assertEqual(self.rom[p],0x70)
                self.assertEqual(self.rom[p+1:p+1+n],bytes(ord(c)+48 for c in e['english']))
                self.assertEqual(self.rom[p+1+n:p+3+n].hex(),e['suffix'])
                self.assertEqual([f'{x:06X}' for x in refs.get(p,[])],e['refs'])
                self.assertFalse(any(x in refs for x in range(p+1,p+1+n)))

    def test_base_preserved_and_outside_unchanged(self):
        if self.rom is None:self.skipTest('ROM_PATH non fourni')
        allowed=bytearray(len(self.rom))
        for e in self.entries:
            p=int(e['id'],16)+1;allowed[p:p+e['text_length']]=b'\1'*e['text_length']
        for profile in ('accents','ascii'):
            with self.subTest(profile=profile):
                base,old=independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v20_{profile}.ips').read_bytes(),self.rom)
                result,new=independent_ips((IPS_DIR/f'EarthBound_Beginnings_FR_v21_{profile}.ips').read_bytes(),self.rom)
                for p,payload in old:self.assertEqual(result[p:p+len(payload)],base[p:p+len(payload)])
                self.assertFalse(any(a!=b for a,b,m in zip(base,result,allowed) if not m))

    def test_no_v21_range_overlap(self):
        spans=sorted((int(e['id'],16)+1,int(e['id'],16)+1+e['text_length']) for e in self.entries)
        self.assertTrue(all(b<=c for (a,b),(c,d) in zip(spans,spans[1:])))

if __name__=='__main__':unittest.main()
