#!/usr/bin/env python3
"""Tests synthétiques V17, sans ROM commerciale et sans revendication d'émulation."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "traduction"))
from preparer_v17 import (ROM_SIZE, decode_layout, occupied_spans, overlaps,
                          parse_ips, prepare)


def ips(*records):
    out = bytearray(b"PATCH")
    for pos, data in records:
        out += pos.to_bytes(3, "big") + len(data).to_bytes(2, "big") + data
    return bytes(out + b"EOF")


class PreparationV17(unittest.TestCase):
    def setUp(self):
        self.rom = bytearray(ROM_SIZE)
        self.pos = 0x339A00
        self.english = "@Hello there.\n@How are you?[13][02]"
        self.payload = b"\x70" + bytes(ord(c)+48 for c in "Hello there.") + b"\x03\x00\x70" + bytes(ord(c)+48 for c in "How are you?") + b"\x13\x02"
        self.rom[self.pos:self.pos+len(self.payload)] = self.payload
        self.ptr_at = 0x1000
        self.rom[self.ptr_at:self.ptr_at+4] = (0xC00000+self.pos).to_bytes(4, "little")
        self.row = {"id": f"{self.pos:06X}", "category": "script", "status": "a_examiner",
                    "english": self.english, "incoming_literal_candidates": [f"{self.ptr_at:06X}"]}

    def test_retour_de_ligne_deux_octets_et_pointeur(self):
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips())
        self.assertEqual(report["selectionnes"], 1)
        self.assertEqual(result["entries"][0]["newline_one_byte_mask"], 0)
        self.assertEqual(result["entries"][0]["translations"], ["Hello there.", "How are you?"])
        self.assertEqual(result["entries"][0]["status"], "a_traduire_et_revalider")

    def test_retour_de_ligne_un_octet(self):
        self.rom[self.pos:self.pos+len(self.payload)] = self.payload.replace(b"\x03\x00", b"\x00") + b"\x00"
        layout = decode_layout(bytes(self.rom), self.pos, self.english)
        self.assertEqual(layout[1], 1)

    def test_collision_v16_exclue(self):
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips((self.pos+3, b"abc")))
        self.assertEqual(report["selectionnes"], 0)
        self.assertEqual(report["collision_ips_ou_candidat"], 1)

    def test_collision_uniquement_ascii_exclue(self):
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips(),
                                 ips((self.pos+3, b"abc")))
        self.assertEqual(report["selectionnes"], 0)
        self.assertEqual(report["collision_ips_ou_candidat"], 1)

    def test_pointeur_interieur_exclu(self):
        self.rom[0x1100:0x1104] = (0xC00000+self.pos+4).to_bytes(4, "little")
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips())
        self.assertEqual(report["selectionnes"], 0)
        self.assertEqual(report["pointeur_interieur"], 1)

    def test_pointeur_declare_inexact(self):
        self.row["incoming_literal_candidates"] = ["001111"]
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips())
        self.assertEqual(report["selectionnes"], 0)
        self.assertEqual(report["pointeur_declare_non_conforme"], 1)

    def test_source_differente(self):
        self.rom[self.pos] = 0
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips())
        self.assertEqual(report["selectionnes"], 0)
        self.assertEqual(report["format_ou_source_non_conforme"], 1)

    def test_commandes_conservees_si_source_exacte(self):
        self.row["english"] = "[18 04]@Hi![13][02]"
        self.rom[self.pos:self.pos+len(self.payload)] = b"\x00" * len(self.payload)
        self.rom[self.pos:self.pos+8] = b"\x18\x04\x70" + bytes(ord(c)+48 for c in "Hi!") + b"\x13\x02"
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips())
        self.assertEqual(report["selectionnes"], 1)
        self.assertEqual(result["entries"][0]["translations"], ["Hi!"])

    def test_commandes_inconnues_refusees(self):
        self.row["english"] = "@[1C ZZ]Hello[13][02]"
        result, report = prepare(bytes(self.rom), {"entries": [self.row]}, ips())
        self.assertEqual(report["selectionnes"], 0)

    def test_ips_rle_et_erreurs(self):
        rle = b"PATCH" + (10).to_bytes(3, "big") + b"\x00\x00" + b"\x00\x03" + b"\x50" + b"EOF"
        self.assertEqual(list(parse_ips(rle)), [(10, 13)])
        self.assertTrue(overlaps(11, 12, occupied_spans(rle)))
        with self.assertRaises(ValueError):
            list(parse_ips(b"PATCH" + b"\x00"))
        with self.assertRaises(ValueError):
            list(parse_ips(b"PATCH" + b"EOF" + b"x"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
