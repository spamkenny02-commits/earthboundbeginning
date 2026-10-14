"""CI checks using extracted source fixtures; full ROM checks are separate."""
import json
import sys
import unittest
from pathlib import Path
from audit_v25 import ROOT, commands_preserved
from build_v25 import rendered
from build_v19 import encode, records, read_translations

class OfflineV25(unittest.TestCase):
    def test_sources_and_lengths(self):
        entries=json.loads((ROOT/'tools/v25/v25_dialogues_fr.json').read_text())['entries']
        translations=read_translations(ROOT/'tools/v25/translations_v25.tsv')
        self.assertEqual(len(entries),165)
        self.assertEqual(set(translations),{e['id'] for e in entries})
        for e in entries:
            self.assertEqual(translations[e['id']],e['fr'])
            self.assertEqual(rendered(e['fr'],e['english']),e['rendered_fr'])
            for p in ('accents','ascii'):self.assertLessEqual(len(encode(e['rendered_fr'],p)),e['text_length'])

    def test_extracted_parent_scripts(self):
        scripts={s['id']:s for s in json.loads((ROOT/'atelier/extraction/dialogues.json').read_text())}
        for e in json.loads((ROOT/'tools/v25/v25_dialogues_fr.json').read_text())['entries']:
            s=scripts[e['script_id']];raw=bytes.fromhex(s['raw_hex'])
            p=int(e['id'],16)-int(e['script_id'],16)
            self.assertEqual(raw[p:p+e['text_length']],bytes(ord(c)+48 for c in e['english']))
            self.assertEqual(s['literal_pointer_offsets'],e['script_refs'])

    def test_ips_preserve_base_and_manifest(self):
        entries=json.loads((ROOT/'tools/v25/v25_dialogues_fr.json').read_text())['entries']
        for profile in ('accents','ascii'):
            prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v24_{profile}.ips').read_bytes()
            current=(ROOT/f'patches/EarthBound_Beginnings_FR_v25_{profile}.ips').read_bytes()
            old=records(prior);new=records(current)
            self.assertEqual(current[:len(prior)-3],prior[:-3])
            self.assertEqual(new[:len(old)],old)
            self.assertEqual(new[len(old):],[(int(e['id'],16),encode(e['rendered_fr'],profile).ljust(e['text_length'],b'\x50')) for e in entries])

    def test_command_mask(self):
        self.assertTrue(commands_preserved(b'XabcY',b'XdefY',0,5,[(1,4)]))
        self.assertFalse(commands_preserved(b'XabcY',b'ZabcY',0,5,[(1,4)]))

if __name__=='__main__':unittest.main()
