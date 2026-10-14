"""Requires ROM_PATH; never skipped or substituted."""
import os, tempfile, unittest
from pathlib import Path
from build_v28 import audit,build
class V28Rom(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.environ.get('ROM_PATH'):
            raise RuntimeError('ROM_PATH required')
        cls.path=Path(os.environ['ROM_PATH'])
    def test_original_source_and_references(self):
        self.assertEqual(set(audit(self.path.read_bytes())),{'accents','ascii'})
    def test_complete_roundtrip(self):
        with tempfile.TemporaryDirectory() as out:
            result=build(self.path,Path(out))
            self.assertTrue(all(v['rom_roundtrip'] for v in result.values()))
if __name__=='__main__':unittest.main()
