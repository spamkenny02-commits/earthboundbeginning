"""Independent binary regression and audit boundary checks for V30."""
import hashlib
import json
import os
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path
from audit_v30 import ROOT, commands_preserved, audit
from build_v30 import rendered, build
from build_v19 import ROM_SHA, read_translations, encode, pointer_index
sys.path.insert(0,str(ROOT/'tools/v25'))
from test_v25 import independent_ips
from preparer_v17 import decode_layout

ACCENTS='éèêëàâîïôùûüçÉÀÇ'
def decode(data):
    return ''.join(ACCENTS[x-0xb0] if 0xb0<=x<0xb0+len(ACCENTS) else chr(x-48) for x in data).rstrip(' ')

class V30Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.environ.get('ROM_PATH'):
            raise RuntimeError('ROM_PATH requis: les contrôles ROM ne doivent pas être ignorés')
        cls.rom=Path(os.environ['ROM_PATH']).read_bytes()
        cls.entries=json.loads((ROOT/'tools/v30/v30_dialogues_fr.json').read_text())['entries']
        cls.translations=read_translations(ROOT/'tools/v30/translations_v30.tsv')
        cls.validation=json.loads((ROOT/'tools/v30/validation_v30.json').read_text())
        cls.out=Path(os.environ.get('V30_OUT',str(ROOT/'build_v30')))

    def test_count_and_real_changes(self):
        self.assertEqual(len(self.entries),121)
        self.assertEqual(len(self.translations),121)
        self.assertEqual(set(self.translations),{e['id'] for e in self.entries})
        self.assertTrue(all(e['fr'].strip()!=e['english'].strip() for e in self.entries))

    def test_source_and_manifest(self):
        self.assertEqual(hashlib.sha256(self.rom).hexdigest(),ROM_SHA)
        for e in self.entries:
            p=int(e['id'],16);n=e['text_length']
            self.assertEqual(self.rom[p:p+n],bytes(ord(c)+48 for c in e['english']))
            self.assertEqual(e['fr'],self.translations[e['id']])
            self.assertEqual(e['rendered_fr'],rendered(e['fr'],e['english']))

    def test_script_provenance(self):
        refs=pointer_index(self.rom)
        for e in self.entries:
            p=int(e['id'],16);s=int(e['script_id'],16)
            end,mask,spans=decode_layout(self.rom,s,e['script_english'])
            self.assertEqual(end,int(e['script_end'],16))
            self.assertIn((p,p+e['text_length']),spans)
            self.assertEqual(e['script_refs'],[f'{q:06X}' for q in refs[s]])
            self.assertTrue(e['script_refs'])
            self.assertFalse(any(q in refs for q in range(p,p+e['text_length'])))

    def test_lengths_both_profiles(self):
        for e in self.entries:
            for profile in ('accents','ascii'):
                self.assertLessEqual(len(encode(e['rendered_fr'],profile)),e['text_length'])

    def test_spacing_at_dynamic_boundaries(self):
        self.assertEqual(rendered('nouveau','  old '),'  nouveau ')
        self.assertEqual(rendered('fin','old'),'fin')
        self.assertEqual(rendered("et s'éveille.","'s presence and awoke.")," et s'éveille.")

    def test_control_mask_rejects_changed_commands(self):
        source=b'XabcY'
        self.assertTrue(commands_preserved(source,b'XdefY',0,5,[(1,4)]))
        self.assertFalse(commands_preserved(source,b'ZabcY',0,5,[(1,4)]))
        self.assertFalse(commands_preserved(source,b'XabcZ',0,5,[(1,4)]))

    def test_no_overlapping_text_spans(self):
        spans=sorted((int(e['id'],16),int(e['id'],16)+e['text_length']) for e in self.entries)
        self.assertTrue(all(b<=c for (a,b),(c,d) in zip(spans,spans[1:])))

    def test_independent_roundtrip_and_text_decode(self):
        for profile in ('accents','ascii'):
            prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v29_{profile}.ips').read_bytes()
            ips=(self.out/f'EarthBound_Beginnings_FR_v30_{profile}.ips').read_bytes()
            base,old=independent_ips(prior,self.rom)
            result,new=independent_ips(ips,self.rom)
            self.assertEqual(ips[:len(prior)-3],prior[:-3])
            self.assertEqual(new[:len(old)],old)
            self.assertEqual(len(new)-len(old),121)
            self.assertEqual(hashlib.sha256(ips).hexdigest(),self.validation['profiles'][profile]['sha256'])
            if self.validation['profiles'][profile].get('target_rom_sha256'):
                self.assertEqual(hashlib.sha256(result).hexdigest(),self.validation['profiles'][profile]['target_rom_sha256'])
            for e in self.entries:
                p=int(e['id'],16);expected=e['rendered_fr'].rstrip(' ')
                if profile=='ascii':
                    expected=''.join(c for c in unicodedata.normalize('NFD',expected) if not unicodedata.combining(c))
                self.assertEqual(decode(result[p:p+e['text_length']]),expected)

    def test_prior_bytes_outside_spans_and_commands(self):
        allowed=bytearray(len(self.rom))
        for e in self.entries:
            p=int(e['id'],16);allowed[p:p+e['text_length']]=b'\1'*e['text_length']
        for profile in ('accents','ascii'):
            base,old=independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v29_{profile}.ips').read_bytes(),self.rom)
            target,new=independent_ips((self.out/f'EarthBound_Beginnings_FR_v30_{profile}.ips').read_bytes(),self.rom)
            self.assertFalse(any(a!=b for a,b,m in zip(base,target,allowed) if not m))
            for p,b in old:self.assertEqual(target[p:p+len(b)],base[p:p+len(b)])
            for e in self.entries:
                s=int(e['script_id'],16);z,_,spans=decode_layout(self.rom,s,e['script_english'])
                self.assertTrue(commands_preserved(self.rom,target,s,z,spans))
                for q in e['script_refs']:
                    q=int(q,16);self.assertEqual(target[q:q+4],self.rom[q:q+4])

    def test_bad_rom_rejected(self):
        with self.assertRaises(ValueError):audit(b'not a ROM')

    def test_non_audited_span_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            f=Path(folder)/'bad.tsv';f.write_text('000001\tInterdit\n')
            with self.assertRaisesRegex(ValueError,'Plage non auditée'):
                build(Path(os.environ['ROM_PATH']),Path(folder)/'out',f)

    def test_oversized_translation_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            f=Path(folder)/'bad.tsv';e=self.entries[0]
            f.write_text(e['id']+'\t'+'A'*(e['text_length']+1)+'\n')
            with self.assertRaisesRegex(ValueError,'Longueur'):
                build(Path(os.environ['ROM_PATH']),Path(folder)/'out',f)

if __name__=='__main__':unittest.main()
