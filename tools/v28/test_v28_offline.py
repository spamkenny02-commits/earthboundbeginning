import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import encode,records,sha,read_translations
from build_v28 import entries,BASE_SHA,FINAL_SHA

class V28Offline(unittest.TestCase):
    def test_manifest(self):
        rows=entries()
        trans=read_translations(ROOT/'tools/v28/translations_v28.tsv')
        self.assertEqual(len(rows),49)
        self.assertEqual(set(trans),{e['id'] for e in rows})
        for e in rows:
            self.assertEqual(e['fr'],trans[e['id']])
            self.assertNotEqual(e['english'],e['fr'])
            for profile in ('accents','ascii'):
                self.assertLessEqual(len(encode(e['fr'],profile)),e['text_length'])

    def test_ips_records(self):
        rows=entries()
        for profile in ('accents','ascii'):
            old=(ROOT/f'patches/EarthBound_Beginnings_FR_v27_{profile}.ips').read_bytes()
            new=(ROOT/f'patches/EarthBound_Beginnings_FR_v28_{profile}.ips').read_bytes()
            self.assertEqual(sha(old),BASE_SHA[profile])
            self.assertEqual(sha(new),FINAL_SHA[profile])
            self.assertEqual(new[:len(old)-3],old[:-3])
            prev=records(old);current=records(new)
            self.assertEqual(current[:len(prev)],prev)
            self.assertEqual(len(current)-len(prev),49)
            for e,(p,b) in zip(rows,current[len(prev):]):
                self.assertEqual(p,int(e['id'],16))
                self.assertEqual(b,encode(e['fr'],profile).ljust(e['text_length'],bytes([80])))
if __name__=='__main__':unittest.main()
