"""Build V37 by translating the remaining English battle-window labels."""
import argparse
import array
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools/v36"), str(ROOT / "tools/v19")]
from build_v19 import ROM_SHA, SIZE, append, apply, pointer_index, records, sha
from build_v36 import (
    COILSNAKE_COMMIT, DESTINATION, POINTER_OFFSET, RAW_SIZE, RESERVATION_END,
    block_from_bytes, decompress, load_coilsnake, pointer_structure,
)

BASE_SHA = {
    "accents": "b8717a595aba9cf6fcec192162191544cb5c538e86a54a05a1cb4292c6c7efd9",
    "ascii": "3dab73807169ffe364374885c0e7b19f1ebe72a149b55c9f30b6ee70758411e4",
}
V36_PAYLOAD_SHA = "bc38971e7f9ea944736d346dfe17aa0a389fb91ae22ab1387855515bbf0ade54"
CRITICAL_TOP, CRITICAL_BOTTOM = 352, 368

GLYPHS = {
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    " ": ("00000",) * 7,
}


def put_label(tiles, text, top, bottom):
    for index, letter in enumerate(text):
        canvas = [[3] * 8 for _ in range(16)]
        for y, row in enumerate(GLYPHS[letter], 4):
            for x, bit in enumerate(row, 1):
                if bit == "1":
                    canvas[y][x] = 2
        tiles[top + index] = canvas[:8]
        tiles[bottom + index] = canvas[8:]


def translated_payload(baseline, api):
    Block, EbCompressibleBlock, _, WindowGraphicsModule, _, _ = api
    module = WindowGraphicsModule()
    module.read_from_rom(block_from_bytes(Block, baseline))
    before = [[row[:] for row in tile] for tile in module.graphics_1.tiles]
    put_label(module.graphics_1.tiles, "COUP CRIT!", CRITICAL_TOP, CRITICAL_BOTTOM)
    changed = [i for i, (a, b) in enumerate(zip(before, module.graphics_1.tiles)) if a != b]
    expected = list(range(352, 362)) + list(range(368, 378))
    if changed != expected:
        raise ValueError("Tuiles V37 modifiées inattendues")
    raw_block = Block(RAW_SIZE)
    module.graphics_1.to_block(raw_block, bpp=2)
    raw = bytes(raw_block.to_array())
    packed = EbCompressibleBlock(RAW_SIZE)
    packed.from_array(array.array("B", raw))
    packed.compress()
    return bytes(packed.to_array()), raw, module, changed


def build(rom_path, out, coilsnake_path):
    api = load_coilsnake(coilsnake_path)
    Block, _, arrangement, _, from_snes_address, read_asm_pointer = api
    original = Path(rom_path).read_bytes()
    if len(original) != SIZE or sha(original) != ROM_SHA:
        raise ValueError("ROM originale USA 1.2 requise")
    results = {}
    common_payload = common_raw = None
    preview_module = None
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    for profile in ("accents", "ascii"):
        prior = (ROOT / f"patches/EarthBound_Beginnings_FR_v36_{profile}.ips").read_bytes()
        if sha(prior) != BASE_SHA[profile]:
            raise ValueError("IPS V36 non conforme: " + profile)
        old_records = records(prior)
        baseline = apply(original, old_records)
        if not pointer_structure(baseline):
            raise ValueError("Structure du pointeur V36 invalide")
        pointer = from_snes_address(read_asm_pointer(block_from_bytes(Block, baseline), POINTER_OFFSET))
        if pointer != DESTINATION:
            raise ValueError("Le pointeur V36 ne vise pas sa copie")
        owners = [(p, raw) for p, raw in old_records if p < RESERVATION_END and p + len(raw) > DESTINATION]
        if len(owners) != 1 or owners[0][0] != DESTINATION or sha(owners[0][1]) != V36_PAYLOAD_SHA:
            raise ValueError("Propriété V36 de la réserve non prouvée")
        if any(DESTINATION <= target < RESERVATION_END for target in pointer_index(baseline) if target != DESTINATION):
            raise ValueError("Cible HiROM concurrente dans la réserve")
        payload, raw, module, changed = translated_payload(baseline, api)
        if len(payload) > RESERVATION_END - DESTINATION:
            raise ValueError("Bloc V37 trop grand")
        if common_payload is None:
            common_payload, common_raw, preview_module = payload, raw, module
        elif payload != common_payload or raw != common_raw:
            raise ValueError("Graphisme divergent entre profils")
        additions = [(DESTINATION, payload)]
        ips = append(prior, additions)
        target = apply(original, records(ips))
        if records(ips) != old_records + additions or target != apply(baseline, additions):
            raise ValueError("Chaîne IPS non autonome")
        if decompress(target, DESTINATION, api) != raw:
            raise ValueError("Roundtrip de compression incorrect")
        if target[:DESTINATION] != baseline[:DESTINATION] or target[DESTINATION + len(payload):] != baseline[DESTINATION + len(payload):]:
            raise ValueError("Écriture hors du bloc V37")
        path = out / f"EarthBound_Beginnings_FR_v37_{profile}.ips"
        path.write_bytes(ips)
        results[profile] = {
            "sha256": sha(ips), "target_rom_sha256": sha(target),
            "prior_records_preserved": len(old_records), "records_added": 1,
            "controlled_v36_record_replacement": True, "independent_rom_roundtrip": True,
            "outside_new_payload_unchanged": True,
        }
    arrangement.image(preview_module.graphics_1, preview_module.flavor_palettes[0]).save(ROOT / "tools/v37/v37_preview.png", "PNG")
    report = {
        "base": "V36", "source_sha256": sha(original), "coilsnake_commit": COILSNAKE_COMMIT,
        "new_dialogue_fragments": 0, "scripts_revised": 0, "graphics_translated": 1,
        "labels": [{"source": "SMAAAASH!!", "french": "COUP CRIT!"}],
        "compressed_destination": f"{DESTINATION:06X}", "reservation_end": f"{RESERVATION_END:06X}",
        "compressed_length": len(common_payload), "compressed_sha256": sha(common_payload),
        "uncompressed_length": len(common_raw), "uncompressed_sha256": sha(common_raw),
        "tiles_replaced": 20, "tile_indexes": changed, "v36_pointer_preserved": True,
        "hp_to_pv_excluded_shared_tiles": [8, 9, 24, 25],
        "v36_payload_owner_verified": True, "other_ips_collisions": 0, "profiles": results,
    }
    (ROOT / "tools/v37/validation_v37.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "patches")
    parser.add_argument("--coilsnake", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.rom, args.out, args.coilsnake), ensure_ascii=False, indent=2))
