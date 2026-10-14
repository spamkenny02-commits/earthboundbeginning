import json
import os
from pathlib import Path
import unittest
from ips import records, apply, append, sha, ROM_SHA
from build_work import ROOT, ACCENTS, encode

class IPSChecks(unittest.TestCase):
    def test_literal_and_rle(self):
        data = b'PATCH\x00\x00\x01\x00\x02ab\x00\x00\x04\x00\x00\x00\x03ZEOF'
        self.assertEqual(records(data), [(1,b'ab'),(4,b'ZZZ')])

    def test_truncated_inputs(self):
        for data in (b'', b'PATCH', b'PATCH\x00\x00\x01', b'PATCH\x00\x00\x01\x00\x03a', b'PATCH\x00\x00\x01\x00\x00\x00'):
            with self.subTest(data=data), self.assertRaises(ValueError):
                records(data)

    def test_invalid_trailer(self):
        with self.assertRaises(ValueError):
            records(b'PATCHEOFextra')

    def test_record_order(self):
        self.assertEqual(apply(b'0000', [(1,b'ab'),(2,b'Z')]), b'0aZ0')

    def test_out_of_bounds(self):
        with self.assertRaises(ValueError):
            apply(b'0000', [(3,b'ab')])

    def test_eof_offset_rejected(self):
        with self.assertRaises(ValueError):
            append(b'PATCHEOF',[(0x454f46,b'a')])

    def test_unencodable_char_rejected(self):
        for text in ('œ', '😀', '\n', '"'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                encode(text,'accents')

    def test_accent_ascii_profiles(self):
        self.assertEqual(encode('éàç','accents'), bytes((0xb0,0xb4,0xbc)))
        self.assertEqual(encode('éàç','ascii'), b'\x95\x91\x93')

class RealROMChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = Path(os.environ['ROM_PATH']).read_bytes()
        cls.entries = json.loads((ROOT/'v18_work_dialogues_fr.json').read_text())['entries']

    def test_original_fingerprint(self):
        self.assertEqual(sha(self.rom),ROM_SHA)

    def test_independent_decode_and_regression(self):
        # Independently interpret IPS framing (including RLE), then decode every
        # new target string; do not use the builder's expected target ROM.
        def interpret(data):
            out=bytearray(self.rom); i=5
            self.assertEqual(data[:5],b'PATCH')
            while data[i:i+3] != b'EOF':
                pos=int(data[i:i+3].hex(),16); i+=3
                size=int(data[i:i+2].hex(),16); i+=2
                if size:
                    payload=data[i:i+size]; i+=size
                else:
                    size=int(data[i:i+2].hex(),16); i+=2
                    payload=bytes([data[i]])*size; i+=1
                out[pos:pos+size]=payload
            self.assertEqual(i+3,len(data))
            return out
        for profile in ('accents','ascii'):
            with self.subTest(profile=profile):
                base=interpret((ROOT/'base'/f'EarthBound_Beginnings_FR_v18_{profile}.ips').read_bytes())
                target=interpret((ROOT/f'EarthBound_Beginnings_FR_v18_work_{profile}.ips').read_bytes())
                allowed=bytearray(len(base))
                for e in self.entries:
                    start=int(e['id'],16)+1; n=e['text_length']
                    allowed[start:start+n]=b'\1'*n
                    text=''.join(ACCENTS[b-0xb0] if 0xb0<=b<0xb0+len(ACCENTS) else chr(b-48) for b in target[start:start+n]).rstrip()
                    expected=e['fr']
                    if profile=='ascii':
                        import unicodedata
                        expected=''.join(c for c in unicodedata.normalize('NFD',expected) if not unicodedata.combining(c))
                    self.assertEqual(text,expected)
                self.assertEqual(sum(a!=b for a,b,m in zip(base,target,allowed) if not m),0)

if __name__ == '__main__':
    unittest.main()
