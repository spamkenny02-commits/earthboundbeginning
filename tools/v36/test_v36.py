"""ROM-backed structural, compression and regression tests for V36."""
import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_v36 import *
sys.path.insert(0, str(ROOT / "tools/v23"))
from test_v23 import independent_ips


class V36Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = Path(os.environ["ROM_PATH"]).read_bytes()
        cls.api = load_coilsnake(os.environ["COILSNAKE_PATH"])
        cls.report = json.loads((ROOT / "tools/v36/validation_v36.json").read_text())
        cls.baselines = {}
        cls.targets = {}
        for profile in ("accents", "ascii"):
            cls.baselines[profile] = independent_ips((ROOT / f"patches/EarthBound_Beginnings_FR_v35_{profile}.ips").read_bytes(), cls.original)[0]
            cls.targets[profile] = independent_ips((ROOT / f"patches/EarthBound_Beginnings_FR_v36_{profile}.ips").read_bytes(), cls.original)[0]

    def test_original_and_dependency_provenance(self):
        self.assertEqual(len(self.original), SIZE)
        self.assertEqual(sha(self.original), ROM_SHA)
        self.assertTrue(pointer_structure(self.original))

    def test_reserve_is_null_unreferenced_and_unoccupied(self):
        for profile, baseline in self.baselines.items():
            self.assertEqual(self.original[DESTINATION:RESERVATION_END], bytes(RESERVATION_END - DESTINATION))
            self.assertEqual(baseline[DESTINATION:RESERVATION_END], bytes(RESERVATION_END - DESTINATION))
            self.assertFalse(any(DESTINATION <= target < RESERVATION_END for target in pointer_index(self.original)))
            self.assertFalse(any(DESTINATION <= target < RESERVATION_END for target in pointer_index(baseline)))
            self.assertFalse(any(pos < RESERVATION_END and pos + len(raw) > DESTINATION for pos, raw in records((ROOT / f"patches/EarthBound_Beginnings_FR_v35_{profile}.ips").read_bytes())))

    def test_asm_pointer_structure_and_relocation(self):
        Block, _, _, _, from_snes_address, read_asm_pointer = self.api
        self.assertEqual(from_snes_address(read_asm_pointer(block_from_bytes(Block, self.original), POINTER_OFFSET)), SOURCE_OFFSET)
        for baseline in self.baselines.values():
            self.assertTrue(pointer_structure(baseline))
            self.assertEqual(from_snes_address(read_asm_pointer(block_from_bytes(Block, baseline), POINTER_OFFSET)), SOURCE_OFFSET)
        for target in self.targets.values():
            self.assertEqual(from_snes_address(read_asm_pointer(block_from_bytes(Block, target), POINTER_OFFSET)), DESTINATION)

    def test_independent_ips_and_exhaustive_diff(self):
        for profile, baseline in self.baselines.items():
            current = (ROOT / f"patches/EarthBound_Beginnings_FR_v36_{profile}.ips").read_bytes()
            additions = records(current)[-3:]
            self.assertEqual(self.targets[profile], apply(baseline, additions))
            self.assertEqual(sha(self.targets[profile]), self.report["profiles"][profile]["target_rom_sha256"])
            mask = bytearray(SIZE)
            for pos, raw in additions:
                mask[pos:pos + len(raw)] = b"\1" * len(raw)
            self.assertFalse(any(a != b for a, b, marked in zip(baseline, self.targets[profile], mask) if not marked))

    def test_compressed_graphic_roundtrip_and_profile_identity(self):
        raws = []
        for profile, target in self.targets.items():
            raw = decompress(target, DESTINATION, self.api)
            self.assertEqual(len(raw), RAW_SIZE)
            self.assertEqual(sha(raw), self.report["uncompressed_sha256"])
            raws.append(raw)
        self.assertEqual(raws[0], raws[1])

    def test_only_sixteen_declared_tiles_change(self):
        for baseline, target in zip(self.baselines.values(), self.targets.values()):
            _, source_raw, _ = graphic_payload(baseline, self.api)
            self.assertEqual(decompress(target, DESTINATION, self.api), source_raw)

    def test_prior_ips_records_and_boy_girl_bytes_survive(self):
        for profile, baseline in self.baselines.items():
            old = records((ROOT / f"patches/EarthBound_Beginnings_FR_v35_{profile}.ips").read_bytes())
            new = records((ROOT / f"patches/EarthBound_Beginnings_FR_v36_{profile}.ips").read_bytes())
            self.assertEqual(new[:len(old)], old)
            for offset in (0x33FAA8, 0x33FC1F, 0x352FE6):
                self.assertEqual(self.targets[profile][offset:offset + 4], baseline[offset:offset + 4])
            self.assertEqual(self.targets[profile][0x3FF990:0x3FF9E0], baseline[0x3FF990:0x3FF9E0])


if __name__ == "__main__":
    unittest.main()
