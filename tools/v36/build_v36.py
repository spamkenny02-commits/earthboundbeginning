"""Build V36: replace the compressed battle banner YOU WON! with VICTOIRE."""
import argparse
import array
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/v19"))
from build_v19 import ROM_SHA, SIZE, append, apply, pointer_index, records, sha

BASE_SHA = {
    "accents": "37e8e61a7b3716cc65c455e0f6941269b2b41a757733d9d073850e2694e7457c",
    "ascii": "fb06451543f80f413a9a3a423caf9ba0b46394b14ba06ec6e922447b483f859e",
}
COILSNAKE_COMMIT = "346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a"
SOURCE_OFFSET = 0x217EC1
DESTINATION = 0x177800
RESERVATION_END = 0x177FD0
POINTER_OFFSET = 0x47C47
RAW_SIZE = 416 * 16
GLYPH_TOP = 384
GLYPH_BOTTOM = 400

GLYPHS = {
    "V": ("10001", "10001", "10001", "10001", "01010", "01010", "00100"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
}


def load_coilsnake(path):
    path = Path(path).resolve()
    if not (path / "coilsnake/modules/eb/WindowGraphicsModule.py").is_file():
        raise ValueError("Arborescence CoilSnake introuvable")
    sys.path.insert(0, str(path))
    from coilsnake.model.common.blocks import Block
    from coilsnake.model.eb.blocks import EbCompressibleBlock
    from coilsnake.modules.eb.WindowGraphicsModule import ARRANGEMENT_1, WindowGraphicsModule
    from coilsnake.util.eb.pointer import from_snes_address, read_asm_pointer
    return Block, EbCompressibleBlock, ARRANGEMENT_1, WindowGraphicsModule, from_snes_address, read_asm_pointer


def block_from_bytes(Block, data):
    block = Block()
    block.from_array(array.array("B", data))
    return block


def pointer_structure(data):
    region = data[POINTER_OFFSET:POINTER_OFFSET + 10]
    if len(region) != 10 or region[0] not in (0xA9, 0xA2, 0xA0) or region[3] not in (0x85, 0x86, 0x84):
        return False
    if region[5] not in (0xA9, 0xA2, 0xA0) or region[8] not in (0x85, 0x86, 0x84):
        return False
    return region[4] + 2 == region[9]


def set_banner(tiles):
    """Replace exactly 16 tiles (8 glyphs x 2 rows), preserving all others."""
    for index, letter in enumerate("VICTOIRE"):
        canvas = [[3] * 8 for _ in range(16)]
        for y, row in enumerate(GLYPHS[letter], 4):
            for x, bit in enumerate(row, 1):
                if bit == "1":
                    canvas[y][x] = 2
        tiles[GLYPH_TOP + index] = canvas[:8]
        tiles[GLYPH_BOTTOM + index] = canvas[8:]


def graphic_payload(baseline, api):
    Block, EbCompressibleBlock, _, WindowGraphicsModule, _, _ = api
    rom = block_from_bytes(Block, baseline)
    module = WindowGraphicsModule()
    module.read_from_rom(rom)
    original_tiles = [[row[:] for row in tile] for tile in module.graphics_1.tiles]
    set_banner(module.graphics_1.tiles)
    changed = [i for i, (a, b) in enumerate(zip(original_tiles, module.graphics_1.tiles)) if a != b]
    if changed != list(range(GLYPH_TOP, GLYPH_TOP + 8)) + list(range(GLYPH_BOTTOM, GLYPH_BOTTOM + 8)):
        raise ValueError("Tuiles modifiées inattendues")
    raw_block = Block(RAW_SIZE)
    module.graphics_1.to_block(raw_block, bpp=2)
    raw = bytes(raw_block.to_array())
    packed = EbCompressibleBlock(RAW_SIZE)
    packed.from_array(array.array("B", raw))
    packed.compress()
    return bytes(packed.to_array()), raw, module


def decompress(data, offset, api):
    Block, EbCompressibleBlock, _, _, _, _ = api
    rom = block_from_bytes(Block, data)
    block = EbCompressibleBlock()
    block.from_compressed_block(rom, offset)
    return bytes(block.to_array())


def build(rom_path, out, coilsnake_path):
    api = load_coilsnake(coilsnake_path)
    Block, _, arrangement, _, from_snes_address, read_asm_pointer = api
    original = Path(rom_path).read_bytes()
    if len(original) != SIZE or sha(original) != ROM_SHA:
        raise ValueError("ROM originale USA 1.2 requise")
    original_block = block_from_bytes(Block, original)
    if not pointer_structure(original) or from_snes_address(read_asm_pointer(original_block, POINTER_OFFSET)) != SOURCE_OFFSET:
        raise ValueError("Pointeur graphique source inattendu")
    results = {}
    common_payload = common_raw = None
    preview_module = None
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for profile in ("accents", "ascii"):
        prior = (ROOT / f"patches/EarthBound_Beginnings_FR_v35_{profile}.ips").read_bytes()
        if sha(prior) != BASE_SHA[profile]:
            raise ValueError("IPS V35 non conforme: " + profile)
        old_records = records(prior)
        baseline = apply(original, old_records)
        if original[DESTINATION:RESERVATION_END] != bytes(RESERVATION_END - DESTINATION):
            raise ValueError("Réserve originale non nulle")
        if baseline[DESTINATION:RESERVATION_END] != bytes(RESERVATION_END - DESTINATION):
            raise ValueError("Réserve V35 non nulle")
        if any(pos < RESERVATION_END and pos + len(raw) > DESTINATION for pos, raw in old_records):
            raise ValueError("Collision IPS V35")
        for image in (original, baseline):
            if any(DESTINATION <= target < RESERVATION_END for target in pointer_index(image)):
                raise ValueError("Réserve déjà ciblée par un pointeur HiROM")
        baseline_block = block_from_bytes(Block, baseline)
        if not pointer_structure(baseline) or from_snes_address(read_asm_pointer(baseline_block, POINTER_OFFSET)) != SOURCE_OFFSET:
            raise ValueError("Pointeur V35 inattendu")
        payload, raw, module = graphic_payload(baseline, api)
        if len(payload) > RESERVATION_END - DESTINATION:
            raise ValueError("Graphisme compressé trop grand pour la réserve")
        if common_payload is None:
            common_payload, common_raw, preview_module = payload, raw, module
        elif payload != common_payload or raw != common_raw:
            raise ValueError("Graphisme divergent entre profils")
        additions = [(DESTINATION, payload), (POINTER_OFFSET + 1, b"\x00\x78"), (POINTER_OFFSET + 6, b"\xd7\x00")]
        ips = append(prior, additions)
        target = apply(original, records(ips))
        if records(ips) != old_records + additions or target != apply(baseline, additions):
            raise ValueError("Chaîne IPS non autonome")
        target_block = block_from_bytes(Block, target)
        if from_snes_address(read_asm_pointer(target_block, POINTER_OFFSET)) != DESTINATION:
            raise ValueError("Pointeur relocalisé incorrect")
        if decompress(target, DESTINATION, api) != raw:
            raise ValueError("Roundtrip compression incorrect")
        mask = bytearray(SIZE)
        for pos, data in additions:
            mask[pos:pos + len(data)] = b"\1" * len(data)
        if any(a != b for a, b, marked in zip(baseline, target, mask) if not marked):
            raise ValueError("Modification hors zones déclarées")
        path = out / f"EarthBound_Beginnings_FR_v36_{profile}.ips"
        path.write_bytes(ips)
        results[profile] = {
            "sha256": sha(ips), "target_rom_sha256": sha(target),
            "prior_records_preserved": len(old_records), "records_added": len(additions),
            "independent_rom_roundtrip": True, "outside_declared_ranges_unchanged": True,
        }
    preview = arrangement.image(preview_module.graphics_1, preview_module.flavor_palettes[0])
    preview_path = ROOT / "tools/v36/victoire_preview.png"
    preview.save(preview_path, "PNG")
    report = {
        "base": "V35", "source_sha256": sha(original), "coilsnake_commit": COILSNAKE_COMMIT,
        "new_dialogue_fragments": 0, "scripts_revised": 0, "graphics_translated": 1,
        "source_label": "YOU WON!", "french_label": "VICTOIRE",
        "compressed_source_offset": f"{SOURCE_OFFSET:06X}", "compressed_destination": f"{DESTINATION:06X}",
        "reservation_end": f"{RESERVATION_END:06X}", "compressed_length": len(common_payload),
        "compressed_sha256": sha(common_payload), "uncompressed_length": len(common_raw),
        "uncompressed_sha256": sha(common_raw), "tiles_replaced": 16,
        "pointer_instruction": f"{POINTER_OFFSET:06X}", "pointer_structure_verified": True,
        "source_and_v35_reserve_null": True, "no_prior_ips_collision": True,
        "no_hirom_target_in_reserve": True, "profiles": results,
    }
    (ROOT / "tools/v36/validation_v36.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "patches")
    parser.add_argument("--coilsnake", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.rom, args.out, args.coilsnake), ensure_ascii=False, indent=2))
