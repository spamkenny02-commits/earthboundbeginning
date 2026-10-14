import os
import unittest
from pathlib import Path
from audit_boy_girl import *

class BoyGirlAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=Path(os.environ['ROM_PATH']).read_bytes()
        cls.result=audit(Path(os.environ['ROM_PATH']))

    def test_original_fingerprint(self):
        self.assertEqual(sha(self.rom),ROM_SHA)

    def test_exact_routine_and_both_returns(self):
        self.assertEqual(self.rom[START:END],RAW)
        self.assertEqual(self.rom[GIRL-1],2)
        self.assertEqual(self.rom[END-1],2)

    def test_internal_girl_branch(self):
        self.assertEqual(int.from_bytes(self.rom[START+7:START+11],'little'),0xc00000+GIRL)
        self.assertEqual(pointer_index(self.rom)[GIRL],[START+7])

    def test_three_literal_callers(self):
        self.assertEqual(pointer_index(self.rom)[START],list(CALLERS))
        self.assertTrue(all(self.rom[p-1]==8 for p in CALLERS))

    def test_modeled_branch_for_four_ids(self):
        self.assertEqual([probe(self.rom,i) for i in (1,2,3,4)],['boy','girl','boy','boy'])

    def test_four_published_profiles_unchanged(self):
        for p in self.result['profiles'].values():
            self.assertTrue(p['routine_unchanged'])
            self.assertEqual(p['modeled_outputs'],{'1':'boy','2':'girl','3':'boy','4':'boy'})

    def test_inplace_french_would_destroy_return(self):
        for text,pos,space in [('garçon',START+11,3),('fille',GIRL,4)]:
            payload=encode(text,'accents')
            self.assertGreater(len(payload),space)
            trial=bytearray(self.rom)
            trial[pos:pos+len(payload)]=payload
            self.assertNotEqual(trial[pos+space],2)

    def test_school_not_partially_translated(self):
        for profile in self.result['profiles'].values():
            school=next(c for c in profile['callers'] if c['scene']=='school')
            self.assertEqual([t['text'] for t in school['texts']],['You are a school'," aren't you?"])
        self.assertFalse(self.result['native_boy_girl_emulator_tested'])
        self.assertFalse(self.result['rom_modified'])

if __name__=='__main__':unittest.main()
