"""Published relocation fixtures and bytecode tests without the ROM."""
import copy,json,unittest
from build_v31 import *

class OfflineV31(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures=json.loads((ROOT/'tools/v31/v31_dialogues_fr.json').read_text())
        cls.report=json.loads((ROOT/'tools/v31/validation_v31.json').read_text())

    def test_french_complete_fixtures(self):
        source=json.loads((ROOT/'tools/v31/dialogues_fr.json').read_text())
        self.assertEqual(len(source),16)
        self.assertEqual(sum(len(x) for x in source.values()),132)
        for e in self.fixtures['scripts']:
            self.assertEqual(source[e['id']],e['fr'])
            for profile in ('accents','ascii'):
                raw=bytes.fromhex(e['baseline_hex'][profile])
                self.assertEqual(len(raw),int(e['end'],16)-int(e['id'],16))
                self.assertEqual(len(e['spans']),len(e['fr']))
                for fr in e['fr']:encode(fr,profile)
        # All inline choices in the selected scripts have proper French labels.
        for ident in ('33C4A0','35001E','3542ED'):
            self.assertIn('Oui',source[ident]);self.assertIn('Non',source[ident])

    def test_published_ips_exact_records_and_hashes(self):
        for profile in ('accents','ascii'):
            prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v30_{profile}.ips').read_bytes()
            current=(ROOT/f'patches/EarthBound_Beginnings_FR_v31_{profile}.ips').read_bytes()
            extra,_,_,_=build_from_fixtures(self.fixtures,profile)
            self.assertEqual(current[:len(prior)-3],prior[:-3])
            self.assertEqual(records(current),records(prior)+extra)
            self.assertEqual(sha(current),self.report['profiles'][profile]['sha256'])

    def test_actual_bytecode_and_branch_operands(self):
        for profile in ('accents','ascii'):
            prior=records((ROOT/f'patches/EarthBound_Beginnings_FR_v30_{profile}.ips').read_bytes())
            actual=dict(records((ROOT/f'patches/EarthBound_Beginnings_FR_v31_{profile}.ips').read_bytes())[len(prior):])
            mapping={};old_scripts={}
            for row,e in zip(self.report['profiles'][profile]['relocated'],self.fixtures['scripts']):
                old=bytes.fromhex(e['baseline_hex'][profile]);start=int(e['id'],16);dest=int(row['offset'],16)
                _,m=transform(old,e['spans'],e['fr'],dest,profile)
                mapping.update({start+o:dest+n for o,n in m.items()});old_scripts[start]=(old,m)
            for row,e in zip(self.report['profiles'][profile]['relocated'],self.fixtures['scripts']):
                start=int(e['id'],16);dest=int(row['offset'],16);old,m=old_scripts[start];new=actual[dest]
                parsed=parse(new,0,len(new)+1,extra_glyphs=range(0xb0,0xc0))
                self.assertEqual(parsed['error'],'');self.assertTrue(parsed['terminal']);self.assertEqual(parsed['end'],len(new))
                # Every glyph byte is the declared French, with no capacity padding.
                for (a,b),fr in zip(e['spans'],e['fr']):self.assertEqual(new[m[a]:m[b]],encode(fr,profile))
                # Compare all command bytes with only declared pointer operands normalized.
                normalized=bytearray(new)
                for ref,target in parsed['refs']:
                    inverse={v:k for k,v in mapping.items()}
                    if target in inverse:normalized[ref:ref+4]=pointer(inverse[target])
                text={q for a,b in e['spans'] for q in range(a,b)}
                for q,byte in enumerate(old):
                    if q not in text:self.assertEqual(normalized[m[q]],byte)

    def test_allocations_do_not_overlap_or_leave_reservations(self):
        for profile in ('accents','ascii'):
            extra,relocated,refs,cursor=build_from_fixtures(self.fixtures,profile)
            spans=sorted((p,p+len(raw)) for p,raw in extra)
            self.assertTrue(all(b<=c for (a,b),(c,d) in zip(spans,spans[1:])))
            for e in relocated:
                p=int(e['offset'],16)
                self.assertTrue(any(a<=p<p+e['new_length']<=b for a,b in RESERVES))
            self.assertEqual(len(refs),19)

    def test_bad_branch_into_replaced_text_is_rejected(self):
        fixture=copy.deepcopy(self.fixtures)
        e=next(x for x in fixture['scripts'] if x['id']=='34A807')
        raw=bytearray.fromhex(e['baseline_hex']['accents']);parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xb0,0xc0))
        ref,_=parsed['refs'][0];raw[ref:ref+4]=pointer(int(e['id'],16)+e['spans'][0][0]+1)
        e['baseline_hex']['accents']=raw.hex()
        with self.assertRaisesRegex(ValueError,'text interior'):build_from_fixtures(fixture,'accents')

    def test_span_count_and_overflow_are_rejected(self):
        fixture=copy.deepcopy(self.fixtures);fixture['scripts'][0]['fr'].pop()
        with self.assertRaisesRegex(ValueError,'span count'):build_from_fixtures(fixture,'accents')
        fixture=copy.deepcopy(self.fixtures);fixture['scripts'][0]['fr'][0]='A'*20000
        with self.assertRaisesRegex(ValueError,'Reservation exhausted'):build_from_fixtures(fixture,'accents')

if __name__=='__main__':unittest.main()
