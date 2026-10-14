"""Full source ROM required; independent IPS application and collision checks."""
import os
import unittest
from build_v29 import *
sys.path.insert(0,str(ROOT/'tools/v23'))
from test_v23 import independent_ips

class RomV29(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=Path(os.environ['ROM_PATH']).read_bytes()
        cls.data={}
        for profile in ('accents','ascii'):
            prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v28_{profile}.ips').read_bytes()
            baseline=independent_ips(prior,cls.original)[0]
            current=(ROOT/f'patches/EarthBound_Beginnings_FR_v29_{profile}.ips').read_bytes()
            cls.data[profile]=(prior,baseline,independent_ips(current,cls.original)[0])

    def test_audit_source_and_all_aliases(self):
        for profile,(prior,baseline,target) in self.data.items():audit(self.original,baseline,prior,profile)

    def test_independent_roundtrip_and_outside_mask(self):
        for profile,(prior,baseline,target) in self.data.items():
            self.assertEqual(target,apply(baseline,additions(profile)))
            mask=bytearray(SIZE)
            for p,raw in additions(profile):mask[p:p+len(raw)]=b'\1'*len(raw)
            self.assertFalse(any(a!=b for a,b,m in zip(target,baseline,mask) if not m))
            self.assertEqual(target[START:END],self.original[START:END])
            report=json.loads((ROOT/'tools/v29/validation_v29.json').read_text())
            self.assertEqual(sha(target),report['profiles'][profile]['target_rom_sha256'])

    def test_no_hidden_references_to_new_routines(self):
        for profile,(prior,baseline,target) in self.data.items():
            refs=pointer_index(target)
            self.assertEqual(refs.get(0x3FF990),[0x33FAA8,0x33FC1F])
            self.assertEqual(refs.get(0x3FF9B0),[0x352FE6])
            self.assertIsNone(refs.get(START))
            self.assertEqual(refs.get(GIRL),[START+7])
            for start,words in ROUTINES.items():
                inner=int.from_bytes(target[start+7:start+11],'little')-0xC00000
                self.assertEqual(refs.get(inner),[start+7])

    def test_occupied_reservation_is_rejected(self):
        prior,baseline,target=self.data['accents'];bad=bytearray(baseline);bad[RESERVE[0]]=1
        with self.assertRaisesRegex(ValueError,'not free'):audit(self.original,bytes(bad),prior,'accents')

    def test_extra_incoming_call_is_rejected(self):
        prior,baseline,target=self.data['accents'];bad=bytearray(baseline);bad[0x3FF800:0x3FF804]=pointer(START)
        with self.assertRaisesRegex(ValueError,'Caller set'):audit(self.original,bytes(bad),prior,'accents')

    def test_school_commands_and_call_opcodes_preserved(self):
        for profile,(prior,baseline,target) in self.data.items():
            for p in CALLERS:self.assertEqual(target[p-1],8)
            self.assertEqual(target[0x352FEA:0x352FED],baseline[0x352FEA:0x352FED]) # comma, 10 0F
            self.assertEqual(target[0x352FF9:0x352FFB],b'\x13\x02')

if __name__=='__main__':unittest.main()
