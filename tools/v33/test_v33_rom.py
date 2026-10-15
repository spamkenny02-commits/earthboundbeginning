"""Independent IPS application, references and exhaustive preservation checks."""
import os,unittest
from build_v33 import *
sys.path.insert(0,str(ROOT/'tools/v23'))
from test_v23 import independent_ips

class RomV33(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=Path(os.environ['ROM_PATH']).read_bytes()
        cls.fixtures=json.loads((ROOT/'tools/v33/v33_dialogues_fr.json').read_text())
        cls.report=json.loads((ROOT/'tools/v33/validation_v33.json').read_text())
        cls.baselines={};cls.targets={}
        for profile in ('accents','ascii'):
            cls.baselines[profile]=independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v32_{profile}.ips').read_bytes(),cls.original)[0]
            cls.targets[profile]=independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v33_{profile}.ips').read_bytes(),cls.original)[0]

    def test_complete_source_provenance(self):
        self.assertEqual(sha(self.original),ROM_SHA)
        self.assertEqual(fixtures_from_rom(self.original,self.baselines),self.fixtures)

    def test_free_reservations(self):
        original_refs=pointer_index(self.original)
        for profile,base in self.baselines.items():
            refs=pointer_index(base)
            old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v32_{profile}.ips').read_bytes())
            for a,b in RESERVES:
                self.assertEqual(self.original[a:b],bytes(b-a));self.assertEqual(base[a:b],bytes(b-a))
                self.assertFalse(any(a<=t<b for t in refs));self.assertFalse(any(a<=t<b for t in original_refs))
                self.assertFalse(any(p<b and p+len(raw)>a for p,raw in old))

    def test_independent_roundtrip_and_exhaustive_diff(self):
        for profile,base in self.baselines.items():
            extra,_,_,_=build_from_fixtures(self.fixtures,profile);target=self.targets[profile]
            self.assertEqual(apply(base,extra),target)
            self.assertEqual(sha(target),self.report['profiles'][profile]['target_rom_sha256'])
            mask=bytearray(SIZE)
            for p,raw in extra:mask[p:p+len(raw)]=b'\1'*len(raw)
            self.assertFalse(any(a!=b for a,b,m in zip(base,target,mask) if not m))

    def test_old_scripts_and_interior_aliases_preserved(self):
        for profile,base in self.baselines.items():
            target=self.targets[profile]
            for e in self.fixtures['scripts']:
                s=int(e['id'],16);end=int(e['end'],16)
                self.assertEqual(target[s:end],base[s:end])
                for alias in e['preserved_aliases']:
                    p=int(alias['offset'],16);self.assertEqual(target[p:p+4],base[p:p+4])

    def test_external_entry_references_and_internal_targets(self):
        for profile,target in self.targets.items():
            report=self.report['profiles'][profile]
            for r in report['entry_refs_rewritten']:
                p=int(r['offset'],16);self.assertEqual(target[p:p+4],pointer(int(r['new_target'],16)))
            for e in report['relocated']:
                for r in e['internal_refs']:
                    p=int(r['offset'],16);self.assertEqual(target[p:p+4],pointer(int(r['new_target'],16)))

    def test_prior_versions_and_boy_girl_preserved(self):
        for profile,base in self.baselines.items():
            target=self.targets[profile];normalized=bytearray(target)
            for r in self.report['profiles'][profile]['entry_refs_rewritten']:
                a=int(r['offset'],16);normalized[a:a+4]=base[a:a+4]
            for version in ('31','32'):
                prior=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text())
                old=json.loads((ROOT/f'tools/v{version}/v{version}_dialogues_fr.json').read_text())
                for e in old['scripts']:
                    a=int(e['id'],16);b=int(e['end'],16);self.assertEqual(target[a:b],base[a:b])
                for e in prior['profiles'][profile]['relocated']:
                    a=int(e['offset'],16);b=a+e['new_length'];self.assertEqual(normalized[a:b],base[a:b])
                for r in prior['profiles'][profile]['entry_refs_rewritten']:
                    a=int(r['offset'],16);self.assertEqual(target[a:a+4],base[a:a+4])
            for a in (0x33FAA8,0x33FC1F,0x352FE6):self.assertEqual(target[a:a+4],base[a:a+4])
            self.assertEqual(target[0x3FF990:0x3FF9E0],base[0x3FF990:0x3FF9E0])

    def test_verified_v31_continuation_is_redirected(self):
        e=next(e for e in self.fixtures['scripts'] if e['id']=='33C628')
        self.assertEqual(e['verified_prior_copy_refs'],['2929EA'])
        for profile,target in self.targets.items():
            dest=next(e['offset'] for e in self.report['profiles'][profile]['relocated'] if e['id']=='33C628')
            self.assertEqual(target[0x2929EA:0x2929EE],pointer(int(dest,16)))
            refs=self.report['profiles'][profile]['entry_refs_rewritten']
            self.assertTrue(any(r['offset']=='2929EA' and r['old_target']=='33C628' for r in refs))

    def test_unknown_entry_and_command_change_rejected(self):
        bad=dict(self.baselines);data=bytearray(bad['accents']);data[0x3FF700:0x3FF704]=pointer(0x33CAA1);bad['accents']=bytes(data)
        with self.assertRaisesRegex(ValueError,'reference set'):fixtures_from_rom(self.original,bad)
        bad=dict(self.baselines);data=bytearray(bad['accents']);data[0x33CAA1]=0x71;bad['accents']=bytes(data)
        with self.assertRaisesRegex(ValueError,'commands changed'):fixtures_from_rom(self.original,bad)

if __name__=='__main__':unittest.main()
