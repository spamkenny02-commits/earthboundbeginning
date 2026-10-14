#!/usr/bin/env python3
"""Independent ROM-level regression checks for the V19 IPS outputs.

Uses its own IPS decoder and glyph decoding; does not call build_v19.
ROM supplied separately and NEVER packaged with patches.
"""
import hashlib
import json
import os
from pathlib import Path
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parent
REPO = Path(os.environ.get('REPO_ROOT', ROOT.parents[1]))
OUT = Path(os.environ.get('V19_OUT', REPO/'build_v19'))
ROM_SHA = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
ACCENTS = 'éèêëàâîïôùûüçÉÀÇ'


def independent_ips(data, rom):
    assert data[:5] == b'PATCH', 'Missing IPS signature'
    result = bytearray(rom)
    i = 5
    entries = []
    while True:
        assert i + 3 <= len(data), 'Truncated IPS stream'
        if data[i:i+3] == b'EOF':
            assert i + 3 == len(data), 'Unexpected IPS trailer'
            return bytes(result), entries
        assert i + 5 <= len(data), 'Truncated IPS header'
        pos = int.from_bytes(data[i:i+3], 'big')
        length = int.from_bytes(data[i+3:i+5], 'big')
        i += 5
        if length:
            assert i + length <= len(data), 'Truncated IPS data'
            payload = data[i:i+length]
            i += length
        else:
            assert i + 3 <= len(data), 'Truncated IPS RLE'
            count = int.from_bytes(data[i:i+2], 'big')
            assert count, 'Zero length RLE'
            payload = data[i+2:i+3] * count
            i += 3
        assert pos + len(payload) <= len(result), 'IPS outside ROM'
        result[pos:pos+len(payload)] = payload
        entries.append((pos, payload))


def decode_text(raw):
    chars = []
    for byte in raw:
        if 0xB0 <= byte < 0xB0 + len(ACCENTS):
            chars.append(ACCENTS[byte-0xB0])
        else:
            assert 0x50 <= byte <= 0xAA, f'Unrecognized glyph byte {byte:#x}'
            chars.append(chr(byte - 48))
    return ''.join(chars).rstrip(' ')


class V19ROMIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom = Path(os.environ['ROM_PATH']).read_bytes()
        cls.candidates = {e['id']:e for e in json.loads(
            (REPO/'tools/v18_work/sources/v18_work_candidates.json').read_text())}
        cls.translations = {}
        for line in (ROOT/'translations_v19.tsv').read_text().splitlines():
            if line.strip() and not line.startswith('#'):
                ident, fr = line.split('\t')
                cls.translations[ident] = fr

    def test_original_rom_fingerprint(self):
        self.assertEqual(len(self.rom), 4*1024*1024)
        self.assertEqual(hashlib.sha256(self.rom).hexdigest(), ROM_SHA)

    def test_both_profiles_independent_rom_roundtrip(self):
        self.assertEqual(len(self.translations), 119)
        for profile in ('accents', 'ascii'):
            with self.subTest(profile=profile):
                prior_bytes = (REPO/'patches'/f'EarthBound_Beginnings_FR_v18_work_{profile}.ips').read_bytes()
                final_bytes = (OUT/f'EarthBound_Beginnings_FR_v19_{profile}.ips').read_bytes()
                self.assertEqual(final_bytes[:len(prior_bytes)-3], prior_bytes[:-3])
                old_rom, old_entries = independent_ips(prior_bytes, self.rom)
                new_rom, new_entries = independent_ips(final_bytes, self.rom)
                self.assertEqual(len(new_entries), len(old_entries) + len(self.translations))
                self.assertEqual(new_entries[:len(old_entries)], old_entries)
                self.assertEqual(hashlib.sha256(final_bytes).hexdigest(),
                    json.loads((OUT/'validation_v19.json').read_text())['profiles'][profile]['sha256'])
                allowed = bytearray(len(self.rom))
                actual_changes = 0
                for ident, french in self.translations.items():
                    e = self.candidates[ident]
                    pos = int(ident, 16)
                    n = e['text_length']
                    old_raw = self.rom[pos+1:pos+1+n]
                    self.assertEqual(self.rom[pos], 0x70)
                    self.assertEqual(old_raw, bytes(ord(ch)+48 for ch in e['english']))
                    self.assertEqual(new_rom[pos], 0x70)
                    self.assertEqual(new_rom[pos+1+n:pos+3+n], self.rom[pos+1+n:pos+3+n])
                    self.assertEqual(new_rom[pos+1+n:pos+3+n].hex(), e['suffix'])
                    actual = decode_text(new_rom[pos+1:pos+1+n])
                    expected = french if profile == 'accents' else ''.join(
                        ch for ch in unicodedata.normalize('NFD', french)
                        if not unicodedata.combining(ch))
                    self.assertEqual(actual, expected, ident)
                    self.assertNotEqual(old_rom[pos+1:pos+1+n], new_rom[pos+1:pos+1+n], ident)
                    allowed[pos+1:pos+1+n] = b'\x01'*n
                    actual_changes += 1
                self.assertEqual(actual_changes, 119)
                outside = sum(a != b for a,b,allowed_byte in zip(old_rom,new_rom,allowed) if not allowed_byte)
                self.assertEqual(outside, 0, f'Unexpected changes outside V19 text: {outside}')

    def test_excluded_prior_pointer_invalidations(self):
        # V18 Work deliberately overwrote these source literal references.
        # Replacing their former target strings in V19 would not make them reachable.
        for ident, addr in [('35AD8D', 0x35AD84), ('35AFD1', 0x35AFC8)]:
            self.assertNotIn(ident, self.translations)
            self.assertEqual(self.rom[addr:addr+4],
                             (0xC00000 + int(ident,16)).to_bytes(4,'little'))
            for profile in ('accents', 'ascii'):
                with self.subTest(ident=ident, profile=profile):
                    prior, _ = independent_ips(
                        (REPO/'patches'/f'EarthBound_Beginnings_FR_v18_work_{profile}.ips').read_bytes(), self.rom)
                    self.assertEqual(prior[addr:addr+4], b'\x00'*4)

    def test_literal_pointer_targets_not_rewritten(self):
        built = {profile: independent_ips((OUT/f'EarthBound_Beginnings_FR_v19_{profile}.ips').read_bytes(), self.rom)[0]
                 for profile in ('accents','ascii')}
        for ident in self.translations:
            e = self.candidates[ident]
            pos = int(ident,16)
            for addr_hex in e['refs']:
                addr = int(addr_hex,16)
                expected = (0xC00000 + pos).to_bytes(4,'little')
                self.assertEqual(self.rom[addr:addr+4],expected)
                for profile in ('accents','ascii'):
                    self.assertEqual(built[profile][addr:addr+4],expected)


if __name__ == '__main__':
    unittest.main()
