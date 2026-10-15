import json,os,sys,unittest,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/v41'),str(ROOT/'tools/v38')]
import build_v41 as build
from build_v19 import ACCENTS,ROM_SHA,SIZE,sha,records,apply,pointer_index
from extraire import parse,length
from test_v38 import independent_apply


def commands(data):
    p=0;out=[]
    while p<len(data):
        if 0x50<=data[p]<=0xAE or 0xB0<=data[p]<0xC0:
            p+=1;continue
        n=length(data,p);out.append((p,data[p:p+n]));p+=n
    return out


class V41Rom(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=Path(os.environ['ROM_PATH']).read_bytes()
        cls.fixtures=json.loads((ROOT/'tools/v41/v41_dialogues_fr.json').read_text())
        cls.plan=json.loads((ROOT/'tools/v41/validation_v41.json').read_text())
        cls.data={}
        for p in ('accents','ascii'):
            old=(ROOT/f'patches/EarthBound_Beginnings_FR_v40_{p}.ips').read_bytes()
            new=(ROOT/f'patches/EarthBound_Beginnings_FR_v41_{p}.ips').read_bytes()
            cls.data[p]={'old':old,'new':new,'base':independent_apply(cls.source,old),
                         'target':independent_apply(cls.source,new)}

    def test_source_and_fixture_provenance(self):
        self.assertEqual(len(self.source),SIZE);self.assertEqual(sha(self.source),ROM_SHA)
        self.assertEqual(build.fixtures_from_baselines(self.source,{p:d['base'] for p,d in self.data.items()}),self.fixtures)

    def test_all_reference_proofs(self):
        for p,d in self.data.items():
            for e in self.fixtures['scripts']:
                for ref in e['references']:
                    self.assertEqual(build.reference_proof(d['base'],int(ref['offset'],16),int(ref['target'],16)),ref['proof'])

    def test_safe_reservations(self):
        source_refs=pointer_index(self.source)
        for p,d in self.data.items():
            refs=pointer_index(d['base'])
            for a,b in build.RESERVES:
                self.assertEqual(self.source[a:b],bytes(b-a));self.assertEqual(d['base'][a:b],bytes(b-a))
                self.assertFalse(any(a<=t<b for t in source_refs));self.assertFalse(any(a<=t<b for t in refs))
                self.assertFalse(any(q<b and q+len(v)>a for q,v in records(d['old'])))

    def test_independent_autonomous_ips(self):
        for p,d in self.data.items():
            self.assertEqual(sha(d['old']),build.BASE_SHA[p])
            self.assertEqual(sha(d['new']),self.plan['profiles'][p]['sha256'])
            self.assertEqual(sha(d['target']),self.plan['profiles'][p]['target_rom_sha256'])
            self.assertEqual(d['target'],apply(self.source,records(d['new'])))

    def test_previous_records_and_sources_preserved(self):
        for p,d in self.data.items():
            old,new=records(d['old']),records(d['new'])
            self.assertEqual(new[:len(old)],old)
            allowed=set()
            for r in self.plan['profiles'][p]['prior_record_pointer_updates']:
                q=int(r['offset'],16);allowed.update(range(q,q+4))
                self.assertEqual(d['base'][q:q+4],(int(r['old_target'],16)+0xC00000).to_bytes(4,'little'))
                self.assertEqual(d['target'][q:q+4],(int(r['new_target'],16)+0xC00000).to_bytes(4,'little'))
            for a,raw in old:
                self.assertTrue(all(d['target'][q]==d['base'][q] for q in range(a,a+len(raw)) if q not in allowed))
            for e in self.fixtures['scripts']:
                a,b=int(e['id'],16),int(e['end'],16)
                self.assertEqual(d['target'][a:b],d['base'][a:b])

    def test_exhaustive_diff(self):
        for p,d in self.data.items():
            mask=bytearray(SIZE)
            for a,raw in records(d['new'])[len(records(d['old'])):]:mask[a:a+len(raw)]=b'\1'*len(raw)
            self.assertTrue(all(a==b for a,b,m in zip(d['target'],d['base'],mask) if not m))

    def test_independent_decoding_and_complete_scripts(self):
        entries={e['id']:e for e in self.fixtures['scripts']}
        for p,d in self.data.items():
            for moved in self.plan['profiles'][p]['relocated']:
                a=int(moved['offset'],16);raw=d['target'][a:a+moved['new_length']]
                parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
                self.assertFalse(parsed['error']);self.assertTrue(parsed['terminal']);self.assertEqual(parsed['end'],len(raw))
                actual=[''.join(ACCENTS[x-0xB0] if 0xB0<=x<0xC0 else chr(x-48) for x in raw[a:b]) for a,b in parsed['spans']]
                expected=[t for t in entries[moved['id']]['fr'] if t]
                if p=='ascii':expected=[''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c)) for s in expected]
                self.assertEqual(actual,expected)

    def test_commands_are_preserved_except_declared_targets(self):
        entries={e['id']:e for e in self.fixtures['scripts']}
        for p,d in self.data.items():
            for moved in self.plan['profiles'][p]['relocated']:
                a=int(moved['offset'],16);raw=d['target'][a:a+moved['new_length']]
                source=bytes.fromhex(entries[moved['id']]['original_hex'])
                restored=bytearray(raw)
                for r in moved['internal_refs']:
                    at=int(r['offset'],16)-a
                    restored[at:at+4]=(int(r['old_target'],16)+0xC00000).to_bytes(4,'little')
                self.assertEqual([v for _,v in commands(source)],[v for _,v in commands(restored)])

    def test_external_internal_and_interior_alias_targets(self):
        for p,d in self.data.items():
            plan=self.plan['profiles'][p]
            all_refs=plan['external_refs_rewritten']+[r for e in plan['relocated'] for r in e['internal_refs']]
            for r in all_refs:
                q=int(r['offset'],16)
                self.assertEqual(d['target'][q:q+4],(int(r['new_target'],16)+0xC00000).to_bytes(4,'little'))
            aliases={r['old_target'] for r in plan['external_refs_rewritten']}
            self.assertIn('349C64',aliases)
            self.assertEqual(len(plan['prior_record_pointer_updates']),9)
            self.assertTrue(any(r['offset']=='167B55' and r['old_target']=='351D12' for r in plan['prior_record_pointer_updates']))

    def test_profiles_share_layout(self):
        a=self.plan['profiles']['accents']['relocated'];b=self.plan['profiles']['ascii']['relocated']
        self.assertEqual([(e['id'],e['offset'],e['new_length']) for e in a],[(e['id'],e['offset'],e['new_length']) for e in b])

if __name__=='__main__':unittest.main()
