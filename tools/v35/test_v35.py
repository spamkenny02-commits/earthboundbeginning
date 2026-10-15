"""V35 structural, independent IPS and ROM regression tests."""
import copy, json, os, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_v35 import *
sys.path.insert(0,str(ROOT/'tools/v23'))
from test_v23 import independent_ips

class V35Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=Path(os.environ['ROM_PATH']).read_bytes()
        cls.fixtures=json.loads((ROOT/'tools/v35/v35_dialogues_fr.json').read_text())
        cls.report=json.loads((ROOT/'tools/v35/validation_v35.json').read_text())
        cls.baselines={p:independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v34_{p}.ips').read_bytes(),cls.original)[0] for p in ('accents','ascii')}
        cls.targets={p:independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v35_{p}.ips').read_bytes(),cls.original)[0] for p in ('accents','ascii')}

    def test_counts_and_source_provenance(self):
        self.assertEqual(sha(self.original),ROM_SHA)
        self.assertEqual(len(SCRIPTS),31); self.assertEqual(len(OVERRIDES),32)
        self.assertEqual(sum(len(e['fr']) for e in self.fixtures['scripts']),141)
        self.assertEqual(make_fixtures(self.original,self.baselines),self.fixtures)

    def test_reservations_are_null_unreferenced_and_unoccupied(self):
        original_refs=pointer_index(self.original)
        for profile,base in self.baselines.items():
            refs=pointer_index(base); old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v34_{profile}.ips').read_bytes())
            for a,b in RESERVES:
                self.assertEqual(self.original[a:b],bytes(b-a)); self.assertEqual(base[a:b],bytes(b-a))
                self.assertFalse(any(a<=t<b for t in refs)); self.assertFalse(any(a<=t<b for t in original_refs))
                self.assertFalse(any(p<b and p+len(raw)>a for p,raw in old))

    def test_exact_ips_records_hashes_and_independent_application(self):
        for profile,base in self.baselines.items():
            prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v34_{profile}.ips').read_bytes()
            current=(ROOT/f'patches/EarthBound_Beginnings_FR_v35_{profile}.ips').read_bytes()
            extra,_,_,_=build_from_fixtures(self.fixtures,profile)
            self.assertEqual(records(current),records(prior)+extra)
            self.assertEqual(sha(current),self.report['profiles'][profile]['sha256'])
            self.assertEqual(apply(base,extra),self.targets[profile])
            self.assertEqual(sha(self.targets[profile]),self.report['profiles'][profile]['target_rom_sha256'])

    def test_relocated_bytecode_text_and_internal_refs(self):
        for profile,target in self.targets.items():
            extra,relocated,rewritten,_=build_from_fixtures(self.fixtures,profile); actual=dict(extra)
            for row,e in zip(relocated,self.fixtures['scripts']):
                dest=int(row['offset'],16); raw=actual[dest]
                parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xb0,0xc0))
                self.assertEqual(parsed['error'],''); self.assertTrue(parsed['terminal']); self.assertEqual(parsed['end'],len(raw))
                old=bytes.fromhex(e['baseline_hex'][profile]); _,mapping=build_v33.transform(old,e['spans'],e['fr'],dest,profile)
                for (a,b),fr in zip(e['spans'],e['fr']): self.assertEqual(raw[mapping[a]:mapping[b]],encode(fr,profile))
                for ref in row['internal_refs']:
                    p=int(ref['offset'],16); self.assertEqual(target[p:p+4],build_v33.pointer(int(ref['new_target'],16)))
            for ref in rewritten:
                p=int(ref['offset'],16); self.assertEqual(target[p:p+4],build_v33.pointer(int(ref['new_target'],16)))

    def test_exhaustive_diff_and_original_aliases(self):
        for profile,base in self.baselines.items():
            target=self.targets[profile]; extra,_,_,_=build_from_fixtures(self.fixtures,profile); mask=bytearray(SIZE)
            for p,raw in extra: mask[p:p+len(raw)]=b'\1'*len(raw)
            self.assertFalse(any(a!=b for a,b,m in zip(base,target,mask) if not m))
            for e in self.fixtures['scripts']:
                a=int(e['id'],16); b=int(e['end'],16); self.assertEqual(target[a:b],base[a:b])

    def test_prior_copies_and_boy_girl_preserved_except_proven_calls(self):
        for profile,base in self.baselines.items():
            normalized=bytearray(self.targets[profile])
            for r in self.report['profiles'][profile]['entry_refs_rewritten']:
                a=int(r['offset'],16); normalized[a:a+4]=base[a:a+4]
            for version in ('31','32','33'):
                plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text())
                for e in plan['profiles'][profile]['relocated']:
                    a=int(e['offset'],16); b=a+e['new_length']; self.assertEqual(normalized[a:b],base[a:b])
            target=self.targets[profile]
            for a in (0x33FAA8,0x33FC1F,0x352FE6): self.assertEqual(target[a:a+4],base[a:a+4])
            self.assertEqual(target[0x3FF990:0x3FF9E0],base[0x3FF990:0x3FF9E0])

    def test_fail_closed_on_bad_fixture(self):
        bad=copy.deepcopy(self.fixtures); bad['scripts'][0]['fr'].pop()
        with self.assertRaisesRegex(ValueError,'span count'): build_from_fixtures(bad,'accents')
        bad=copy.deepcopy(self.fixtures); bad['scripts'][0]['fr'][0]='A'*20000
        with self.assertRaisesRegex(ValueError,'Reservation exhausted'): build_from_fixtures(bad,'accents')

if __name__=='__main__': unittest.main()
