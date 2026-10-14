import tempfile
import unittest
from pathlib import Path
from build_v19 import encode, records, apply, append, read_translations, ACCENTS

ROOT = Path(__file__).parent

class V19LocalTests(unittest.TestCase):
    def test_translation_count_and_unique_ids(self):
        t = read_translations(ROOT/'translations_v19.tsv')
        self.assertEqual(len(t), 119)
        self.assertEqual(len(t), len(set(t)))

    def test_encodable_both_profiles(self):
        for ident, french in read_translations(ROOT/'translations_v19.tsv').items():
            for profile in ('accents','ascii'):
                with self.subTest(ident=ident, profile=profile):
                    self.assertTrue(encode(french, profile))

    def test_length_against_github_candidate_fixture(self):
        pairs = (ROOT/'candidate_lengths.txt').read_text().strip().split(',')
        lengths = dict((ident, int(size)) for ident, size in (p.split(':') for p in pairs))
        for ident, french in read_translations(ROOT/'translations_v19.tsv').items():
            self.assertIn(ident, lengths)
            for profile in ('accents','ascii'):
                with self.subTest(ident=ident, profile=profile):
                    self.assertLessEqual(len(encode(french, profile)), lengths[ident])

    def test_accent_mapping(self):
        self.assertEqual(encode('éàç','accents'),bytes((176,180,188)))
        self.assertEqual(encode('éàç','ascii'),bytes((149,145,147)))

    def test_reject_unsupported_glyph(self):
        for glyph in ('œ','—','…','😀','"','['):
            with self.subTest(glyph=glyph), self.assertRaises(ValueError):
                encode(glyph,'accents')

    def test_ordinary_ips(self):
        raw=b'PATCH\x00\x00\x01\x00\x02ABEOF'
        self.assertEqual(records(raw),[(1,b'AB')])
        self.assertEqual(apply(b'0000',records(raw)),b'0AB0')

    def test_rle_ips(self):
        raw=b'PATCH\x00\x00\x01\x00\x00\x00\x03ZEOF'
        self.assertEqual(records(raw),[(1,b'ZZZ')])

    def test_append_and_preserve_prefix(self):
        base=b'PATCH\x00\x00\x01\x00\x02ABEOF'
        combined=append(base,[(3,b'CD')])
        self.assertEqual(records(combined),[(1,b'AB'),(3,b'CD')])
        self.assertEqual(combined[:len(base)-3],base[:-3])

    def test_bad_ips_rejected(self):
        for raw in (b'',b'PATCHEOFgarbage',b'PATCH\x00\x00\x01\x00\x03A', b'PATCH\x00\x00\x01\x00', b'PATCH\x00\x00\x01\x00\x00\x00\x01'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                records(raw)

    def test_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'dup.tsv'
            p.write_text('123ABC\tbonjour\n123ABC\tsalut\n')
            with self.assertRaises(ValueError):
                read_translations(p)

    def test_tab_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.tsv'
            p.write_text('123ABC sans tab\n')
            with self.assertRaises(ValueError):
                read_translations(p)

if __name__=='__main__':
    unittest.main()
