"""V24 safety checks. ROM-dependent tests run only with ROM_PATH set."""
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/v19'))
from build_v19 import ROM_SHA, encode, records, apply, sha
from build_v24 import load_manifest, verify_entries, build

class V24Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries=load_manifest()
        cls.rom=Path(os.environ['ROM_PATH']).read_bytes() if os.environ.get('ROM_PATH') else None

    def test_63_real_translations(self):
        self.assertEqual(len(self.entries),63)
        self.assertEqual(len({e['id'] for e in self.entries}),63)
        self.assertTrue(all(e['english'] != e['fr'] for e in self.entries))

    def test_encodings_fit(self):
        for e in self.entries:
            for p in ('accents','ascii'):
                with self.subTest(id=e['id'],profile=p):
                    self.assertLessEqual(len(encode(e['fr'],p)),e['text_length'])

    def test_tsv_manifest_consistency(self):
        lines=(ROOT/'tools/v24/translations_v24.tsv').read_text().splitlines()
        pairs=dict(line.split('\t') for line in lines)
        self.assertEqual(len(pairs),len(lines))
        self.assertEqual(pairs,{e['id']:e['fr'] for e in self.entries})

    def test_no_internal_overlap(self):
        spans=sorted((int(e['id'],16),int(e['id'],16)+1+e['text_length']) for e in self.entries)
        self.assertTrue(all(b<=c for (_,b),(c,_) in zip(spans,spans[1:])))

    def test_extracted_parent_scripts(self):
        scripts={s['id']:s for s in json.loads((ROOT/'atelier/extraction/dialogues.json').read_text(encoding='utf-8'))}
        for e in self.entries:
            with self.subTest(id=e['id']):
                s=scripts[e['script']]
                raw=bytes.fromhex(s['raw_hex'])
                relative=int(e['id'],16)-int(s['id'],16)
                self.assertGreaterEqual(relative,0)
                self.assertLess(relative+1+e['text_length']+2,len(raw)+1)
                self.assertEqual(s['evidence'],'literal_pointer')
                self.assertEqual(s['literal_pointer_offsets'],e['script_refs'])
                self.assertEqual(raw[relative],0x70)
                self.assertEqual(raw[relative+1:relative+1+e['text_length']],
                                 bytes(ord(c)+48 for c in e['english']))
                self.assertEqual(raw[relative+1+e['text_length']:relative+3+e['text_length']].hex(),e['suffix'])

    def test_original_source(self):
        if self.rom is None:self.skipTest('ROM_PATH absent')
        self.assertEqual(sha(self.rom),ROM_SHA)
        extraction=json.loads((ROOT/'atelier/extraction/dialogues.json').read_text())
        self.assertEqual(len(verify_entries(self.rom,self.entries,extraction)),63)

    def test_build_on_v23_and_roundtrip(self):
        if self.rom is None:self.skipTest('ROM_PATH absent')
        base_dir=os.environ.get('V24_BASE_DIR')
        sha_override=None
        if base_dir:
            sha_override={p:sha((Path(base_dir)/f'EarthBound_Beginnings_FR_v23_{p}.ips').read_bytes()) for p in ('accents','ascii')}
        with tempfile.TemporaryDirectory() as d:
            report=build(Path(os.environ['ROM_PATH']),Path(d),base_dir=base_dir,expected_base=sha_override)
            self.assertEqual(report['new_segments'],63)
            for p in ('accents','ascii'):
                new=(Path(d)/f'EarthBound_Beginnings_FR_v24_{p}.ips').read_bytes()
                base=(Path(base_dir) if base_dir else ROOT/'patches')/f'EarthBound_Beginnings_FR_v23_{p}.ips'
                old=base.read_bytes()
                self.assertEqual(new[:len(old)-3],old[:-3])
                self.assertEqual(len(records(new))-len(records(old)),63)

if __name__=='__main__':unittest.main()