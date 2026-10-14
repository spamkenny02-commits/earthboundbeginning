"""No ROM required: independent routine interpreter and published IPS checks."""
import json
import unittest
from build_v29 import *

def execute(raw,start,identity):
    # Consume the actual 19/0B/1B bytecode. No hard-coded branch positions.
    p=0;flag=None;working=None;out=[]
    for _ in range(100):
        op=raw[p];p+=1
        if op==0x19:
            if raw[p:p+2]!=b'\x10\x01':raise ValueError('selector changed')
            working=identity;p+=2
        elif op==0x0B:
            flag=working==raw[p];p+=1
        elif op==0x1B:
            if raw[p]!=3 or flag is None:raise ValueError('invalid branch')
            target=int.from_bytes(raw[p+1:p+5],'little')-0xC00000
            p=target-start if flag else p+5
            if not 0<=p<len(raw):raise ValueError('branch outside routine')
        elif op==2:return ''.join(out)
        elif 0x50<=op<=0xAA:out.append(chr(op-48))
        elif 0xB0<=op<=0xBF:out.append('éèêëàâîïôùûüçÉÀÇ'[op-0xB0])
        else:raise ValueError('unexpected opcode')
    raise ValueError('missing return')

class OfflineV29(unittest.TestCase):
    def test_both_branches_from_published_bytes(self):
        expected={'accents':[('garçon','fille'),('un écolier','une écolière')],
                  'ascii':[('garcon','fille'),('un ecolier','une ecoliere')]}
        for profile in expected:
            old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v28_{profile}.ips').read_bytes())
            current=records((ROOT/f'patches/EarthBound_Beginnings_FR_v29_{profile}.ips').read_bytes())
            extra=dict(current[len(old):])
            for index,start in enumerate((0x3FF990,0x3FF9B0)):
                for identity in (1,2,3,4):
                    self.assertEqual(execute(extra[start],start,identity),expected[profile][index][identity==2])

    def test_bad_target_is_detected(self):
        raw=bytearray(routine(0x3FF990,'garçon','fille','accents'))
        raw[7:11]=pointer(0x3FF9E0)
        with self.assertRaises(ValueError):execute(raw,0x3FF990,2)

    def test_shared_selector_and_returns_preserved(self):
        for profile in ('accents','ascii'):
            for start,words in ROUTINES.items():
                raw=routine(start,*words,profile)
                self.assertEqual(raw[:7],RAW[:7])
                target=int.from_bytes(raw[7:11],'little')-0xC00000-start
                self.assertEqual(raw[target-1],2);self.assertEqual(raw[-1],2)

    def test_autonomous_ips_keeps_every_v28_record(self):
        for profile in ('accents','ascii'):
            prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v28_{profile}.ips').read_bytes()
            current=(ROOT/f'patches/EarthBound_Beginnings_FR_v29_{profile}.ips').read_bytes()
            self.assertEqual(current[:len(prior)-3],prior[:-3])
            self.assertEqual(records(current),records(prior)+additions(profile))
            report=json.loads((ROOT/'tools/v29/validation_v29.json').read_text())
            self.assertEqual(sha(current),report['profiles'][profile]['sha256'])

    def test_three_calls_and_school_separation(self):
        self.assertEqual(DESTINATIONS,{0x33FAA8:0x3FF990,0x33FC1F:0x3FF990,0x352FE6:0x3FF9B0})
        for profile in ('accents','ascii'):
            extra=dict(additions(profile))
            for p,target in DESTINATIONS.items():self.assertEqual(extra[p],pointer(target))
            self.assertEqual(extra[0x352FD5],encode('Tu es donc bien ',profile))
            self.assertTrue(extra[0x352FED].startswith(encode(' pas vrai?',profile)))

    def test_nonoverlap_and_allocation(self):
        for profile in ('accents','ascii'):
            spans=sorted((p,p+len(raw)) for p,raw in additions(profile))
            self.assertTrue(all(b<=c for (a,b),(c,d) in zip(spans,spans[1:])))
            for p,words in ROUTINES.items():self.assertLessEqual(p+len(routine(p,*words,profile)),RESERVE[1])

if __name__=='__main__':unittest.main()
