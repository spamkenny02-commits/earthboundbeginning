import json,os,sys,unittest,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/v46'),str(ROOT/'tools/v38'),str(ROOT/'tools/v44')]
import build_v46 as b
from build_v19 import ACCENTS
from test_v38 import independent_apply
from test_v44 import commands

class V46Rom(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=Path(os.environ['ROM_PATH']).read_bytes()
        cls.f=json.loads((ROOT/'tools/v46/v46_fixtures.json').read_text())
        cls.plan=json.loads((ROOT/'tools/v46/validation_v46.json').read_text());cls.data={}
        for p in ('accents','ascii'):
            old=(ROOT/f'patches/EarthBound_Beginnings_FR_v45_{p}.ips').read_bytes();new=(ROOT/f'patches/EarthBound_Beginnings_FR_v46_{p}.ips').read_bytes()
            cls.data[p]={'old':old,'new':new,'base':independent_apply(cls.source,old),'target':independent_apply(cls.source,new)}

    def test_source_and_complete_fixture_provenance(self):
        self.assertEqual(b.sha(self.source),b.ROM_SHA);self.assertEqual(len(self.source),b.SIZE)
        self.assertEqual(b.make_fixtures(self.source,{p:d['base'] for p,d in self.data.items()}),self.f)

    def test_preparation_has_no_new_integration(self):
        for d in self.data.values():
            audit=b.audit_preparation(self.source,d['base'])
            self.assertEqual((audit['selected'],audit['already_modified'],audit['identical_drafts']),(100,98,2))
            self.assertEqual(audit['new_integrations_from_preparation'],0)
            self.assertEqual([e['id'] for e in audit['entries'] if e['status']=='identical_french_draft'],['3616AF','3619E9'])

    def test_reference_proofs_and_destinations(self):
        for p,d in self.data.items():
            for r in self.plan['profiles'][p]['references_rewritten']:
                q=int(r['offset'],16)
                self.assertEqual(b.reference_proof(d['base'],q,int(r['old_target'],16)),r['proof'])
                self.assertEqual(d['target'][q:q+4],b.pointer(int(r['new_target'],16)))

    def test_food_copy_decoding_and_control_commands(self):
        for p,d in self.data.items():
            sources={e['id']:e for e in self.f['profiles'][p]['foods']}
            for moved in self.plan['profiles'][p]['foods']:
                a=int(moved['offset'],16);raw=d['target'][a:a+moved['new_length']]
                parsed=b.parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
                self.assertFalse(parsed['error']);self.assertTrue(parsed['terminal']);self.assertEqual(parsed['end'],len(raw))
                words=[''.join(ACCENTS[v-0xB0] if v>=0xB0 else chr(v-48) for v in raw[x:y]) for x,y in parsed['spans']]
                expected=sources[moved['id']]['fr']
                if p=='ascii':expected=[''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c)) for s in expected]
                self.assertEqual(words,expected)
                restored=bytearray(raw)
                for r in moved['internal_refs']:
                    q=int(r['offset'],16)-a;restored[q:q+4]=b.pointer(int(r['old_target'],16))
                self.assertEqual([v for _,v in commands(restored)],[v for _,v in commands(bytes.fromhex(sources[moved['id']]['original_hex']))])

    def test_seven_contexts_reuse_exact_v45_helper(self):
        for p,d in self.data.items():
            for e in self.f['profiles'][p]['contexts']:
                q=int(e['pointer'],16);self.assertEqual(d['target'][q:q+4],b.pointer(b.HELPER))
                if e['replacement'] is not None:
                    a=int(e['text_offset'],16);z=a+e['text_capacity']
                    self.assertEqual(d['target'][a:z],b.encode(e['replacement'],p).ljust(z-a,b'\x50'))

    def test_other_global_helper_callers_and_sources_stay_untouched(self):
        for p,d in self.data.items():
            changed={int(e['pointer'],16) for e in self.f['profiles'][p]['contexts']}
            for q in b.pointer_index(d['base'])[0x7E6D7]:
                self.assertEqual(d['target'][q:q+4],b.pointer(b.HELPER) if q in changed else d['base'][q:q+4])
            self.assertEqual(d['target'][0x7E6D7:0x7E758],d['base'][0x7E6D7:0x7E758])
            plan=json.loads((ROOT/'tools/v45/validation_v45.json').read_text())
            for e in plan['profiles'][p]['relocated']:
                if int(e['id'],16)<0x80000:
                    a=int(e['offset'],16);self.assertEqual(d['target'][a:a+e['new_length']],d['base'][a:a+e['new_length']])

    def test_context_commands_are_unchanged_except_their_one_call(self):
        for p,d in self.data.items():
            for e in self.f['profiles'][p]['contexts']:
                a,z=int(e['start'],16),int(e['end'],16);q=int(e['pointer'],16)
                before=d['base'][a:z];restored=bytearray(d['target'][a:z]);restored[q-a:q-a+4]=b.pointer(0x7E6D7)
                self.assertEqual([v for _,v in commands(before)],[v for _,v in commands(restored)])
                self.assertEqual(d['base'][a:z].hex(),e['baseline_hex'])

    def test_existing_french_food_callback_is_fully_preserved(self):
        for p,d in self.data.items():
            self.assertEqual(d['target'][0x35ECFA:0x35ED61],d['base'][0x35ECFA:0x35ED61])
            self.assertEqual(d['base'][0x35ECFA:0x35ED61].hex(),self.f['profiles'][p]['food_group_callback_preserved_hex'])
            parsed=b.parse(d['target'],0x35ED2E,128)
            for target in parsed['targets'][2:]:
                end=d['target'].index(2,target)
                self.assertEqual(d['target'][target:end],b.encode(' ensemble.',p))

    def test_exhaustive_diff_and_previous_records(self):
        for p,d in self.data.items():
            old=b.records(d['old']);new=b.records(d['new']);self.assertEqual(new[:len(old)],old)
            mask=bytearray(b.SIZE)
            for a,raw in new[len(old):]:mask[a:a+len(raw)]=b'\1'*len(raw)
            self.assertTrue(all(a==z or m for a,z,m in zip(d['base'],d['target'],mask)))
            for a,raw in old:self.assertTrue(all(d['target'][i]==d['base'][i] or mask[i] for i in range(a,a+len(raw))))

    def test_independent_ips_and_pinned_hashes(self):
        for p,d in self.data.items():
            self.assertEqual(b.sha(d['old']),b.BASE_SHA[p]);self.assertEqual(b.sha(d['new']),self.plan['profiles'][p]['sha256'])
            self.assertEqual(b.sha(d['target']),self.plan['profiles'][p]['target_rom_sha256'])
            self.assertEqual(d['target'],b.apply(self.source,b.records(d['new'])))

    def test_reserve_is_null_unwritten_and_not_targeted(self):
        a,z=map(lambda x:int(x,16),self.f['reserve'])
        self.assertEqual(self.source[a:z],bytes(z-a))
        for d in self.data.values():
            self.assertEqual(d['base'][a:z],bytes(z-a))
            self.assertFalse(any(a<=q<z for q in b.pointer_index(d['base'])))
            self.assertFalse(any(q<z and q+len(raw)>a for q,raw in b.records(d['old'])))
        self.assertFalse(any(a<=q<z for q in b.pointer_index(self.source)))

    def test_dictionary_and_both_profile_layouts(self):
        for d in self.data.values():
            self.assertEqual(d['target'][0x8CDED:0x8D9ED],d['base'][0x8CDED:0x8D9ED])
            for word in b.dictionary_from_rom(self.source).values():
                a=int(word['offset'],16);n=len(bytes.fromhex(word['raw_hex']))+1
                self.assertEqual(d['target'][a:a+n],d['base'][a:a+n])
        a=self.plan['profiles']['accents']['foods'];z=self.plan['profiles']['ascii']['foods']
        self.assertEqual([(e['id'],e['offset'],e['new_length']) for e in a],[(e['id'],e['offset'],e['new_length']) for e in z])

    def test_v44_fourteen_pointer_repairs_are_preserved(self):
        plan=json.loads((ROOT/'tools/v44/validation_v44.json').read_text())
        for p,d in self.data.items():
            for r in plan['profiles'][p]['prior_pointer_repairs']:
                a=int(r['offset'],16);self.assertEqual(d['target'][a:a+4],b.pointer(int(r['new_target'],16)))

if __name__=='__main__':unittest.main()
