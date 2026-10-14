#!/usr/bin/env python3
"""Tests V17 synthétiques, sans ROM commerciale."""
import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import construire_v17_core as core
import construire_v17 as v17
from construire_v11 import encode, parse_ips, apply_ips

class TestV17(unittest.TestCase):
    def setUp(self):
        self.start = 0x1230
        self.english = "@Hello.\n@Bye![02]"
        self.source = bytearray(0x10000)
        raw = b"\x70" + encode("Hello.") + b"\x03\x00\x70" + encode("Bye!") + b"\x02"
        self.source[self.start:self.start+len(raw)] = raw
        self.source[0x80:0x84] = (0xC00000+self.start).to_bytes(4, "little")
        self.row = dict(id=f"{self.start:06X}", english=self.english,
                        translations=["Salut.", "Oui!"], pointer_refs=["000080"])

    def test_layout(self):
        self.assertEqual(core.derive_mask(self.source,self.start,self.english),0)

    def test_bad_layout(self):
        self.source[self.start] = 0
        with self.assertRaises(ValueError):
            core.derive_mask(self.source,self.start,self.english)

    def test_source_and_pointer(self):
        core.ROM_SIZE = len(self.source)
        core.ROM_SHA = hashlib.sha256(self.source).hexdigest()
        spans, refs = core.validate_and_spans(bytes(self.source),[self.row])
        self.assertEqual(len(spans),2)
        self.assertEqual(refs[self.start],[0x80])

    def test_pointer_interior_rejected(self):
        self.source[0x90:0x94] = (0xC00000+self.start+2).to_bytes(4,"little")
        core.ROM_SIZE = len(self.source)
        core.ROM_SHA = hashlib.sha256(self.source).hexdigest()
        with self.assertRaisesRegex(ValueError,"intérieur"):
            core.validate_and_spans(bytes(self.source),[self.row])

    def test_duplicate_ids_rejected(self):
        core.ROM_SIZE = len(self.source)
        core.ROM_SHA = hashlib.sha256(self.source).hexdigest()
        with self.assertRaisesRegex(ValueError,"doublons"):
            core.validate_and_spans(bytes(self.source),[self.row,self.row])

    def test_merge_by_id(self):
        c=dict(base="v16",entries=[dict(id="1230",english=self.english,pointer_refs_declared=["000080"])])
        t=dict(base="v16",entries=[dict(id="1230",translations=["Salut.","Oui!"],status="integre_v17")])
        self.assertEqual(core.merge_sources(c,t)[0]["pointer_refs"],["000080"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
