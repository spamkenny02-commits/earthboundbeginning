"""ROM-backed structural, compression and regression tests for V37."""
import json, os, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_v37 import *
sys.path.insert(0,str(ROOT/'tools/v23'))
from test_v23 import independent_ips

class V37Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=Path(os.environ['ROM_PATH']).read_bytes();cls.api=load_coilsnake(os.environ['COILSNAKE_PATH'])
        cls.report=json.loads((ROOT/'tools/v37/validation_v37.json').read_text())
        cls.baselines={};cls.targets={}
        for p in ('accents','ascii'):
            cls.baselines[p]=independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v36_{p}.ips').read_bytes(),cls.original)[0]
            cls.targets[p]=independent_ips((ROOT/f'patches/EarthBound_Beginnings_FR_v37_{p}.ips').read_bytes(),cls.original)[0]

    def test_provenance_and_pointer(self):
        self.assertEqual(sha(self.original),ROM_SHA);Block,_,_,_,from_snes,read_pointer=self.api
        for base,target in zip(self.baselines.values(),self.targets.values()):
            self.assertTrue(pointer_structure(base));self.assertTrue(pointer_structure(target))
            self.assertEqual(from_snes(read_pointer(block_from_bytes(Block,base),POINTER_OFFSET)),DESTINATION)
            self.assertEqual(from_snes(read_pointer(block_from_bytes(Block,target),POINTER_OFFSET)),DESTINATION)

    def test_v36_is_exactly_owned_before_replacement(self):
        for p in ('accents','ascii'):
            old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v36_{p}.ips').read_bytes())
            owners=[(q,b) for q,b in old if q<RESERVATION_END and q+len(b)>DESTINATION]
            self.assertEqual(len(owners),1);self.assertEqual(owners[0][0],DESTINATION)
            self.assertEqual(sha(owners[0][1]),V36_PAYLOAD_SHA)

    def test_independent_application_and_exhaustive_diff(self):
        for p,base in self.baselines.items():
            current=(ROOT/f'patches/EarthBound_Beginnings_FR_v37_{p}.ips').read_bytes();addition=records(current)[-1]
            self.assertEqual(self.targets[p],apply(base,[addition]))
            self.assertEqual(sha(self.targets[p]),self.report['profiles'][p]['target_rom_sha256'])
            q,raw=addition;self.assertEqual(self.targets[p][:q],base[:q]);self.assertEqual(self.targets[p][q+len(raw):],base[q+len(raw):])

    def test_compression_roundtrip_and_profile_identity(self):
        raws=[decompress(t,DESTINATION,self.api) for t in self.targets.values()]
        self.assertEqual(raws[0],raws[1]);self.assertEqual(len(raws[0]),RAW_SIZE)
        self.assertEqual(sha(raws[0]),self.report['uncompressed_sha256'])

    def test_exact_twenty_tiles_change(self):
        Block,_,_,Window,_,_=self.api;expected=self.report['tile_indexes']
        for base,target in zip(self.baselines.values(),self.targets.values()):
            a=Window();a.read_from_rom(block_from_bytes(Block,base));b=Window();b.read_from_rom(block_from_bytes(Block,target))
            changed=[i for i,(x,y) in enumerate(zip(a.graphics_1.tiles,b.graphics_1.tiles)) if x!=y]
            self.assertEqual(changed,expected)

    def test_prior_bytes_and_boy_girl_survive(self):
        for p,base in self.baselines.items():
            old=records((ROOT/f'patches/EarthBound_Beginnings_FR_v36_{p}.ips').read_bytes());new=records((ROOT/f'patches/EarthBound_Beginnings_FR_v37_{p}.ips').read_bytes())
            self.assertEqual(new[:-1],old)
            for q in (0x33FAA8,0x33FC1F,0x352FE6):self.assertEqual(self.targets[p][q:q+4],base[q:q+4])
            self.assertEqual(self.targets[p][0x3FF990:0x3FF9E0],base[0x3FF990:0x3FF9E0])

if __name__=='__main__':unittest.main()
