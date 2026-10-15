"""Build V38: relocate and translate the active enemy-description bank."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools/v19"), str(ROOT / "tools/v33"),
                str(ROOT / "atelier/outils")]
from build_v19 import ROM_SHA, SIZE, append, apply, pointer_index, records, sha
from build_v33 import pointer, transform
from extraire import parse, render

BASE_SHA = {
    "accents": "ce710fbd9e1869aacee7cc9f19f933a249e60e83805ca3c793710458ce29ccfc",
    "ascii": "aeb99653aa960e48dbfbf98059bca1ad1fcb4e0657b8933c22b88d0d349eb10d",
}
TABLE_START, TABLE_END = 0x3633EA, 0x3635F2
RESERVES = (
    (0x328A80, 0x328DE0), (0x328E90, 0x329030),
    (0x329040, 0x3292F0), (0x329390, 0x3296E0),
    (0x3296F0, 0x329800), (0x329830, 0x329C30),
    (0x329C40, 0x329D70), (0x329D80, 0x329F50),
    (0x32A030, 0x32A0E0), (0x32A0F0, 0x32A450),
    (0x32A460, 0x32A670), (0x32A770, 0x32A850),
    (0x32A910, 0x32AA70), (0x32AAF0, 0x32AB70),
    (0x32ABE0, 0x32ADA0), (0x32ADB0, 0x32AEA0),
    (0x32AEB0, 0x32B000), (0x32B010, 0x32B1B0),
    (0x32B1C0, 0x32B270), (0x32B280, 0x32B420),
    (0x32B4F0, 0x32B610),
)


def translations():
    return json.loads((ROOT / "tools/v38/translations_v38.json").read_text())


def command_operand_proof(data, operand, target):
    """Prove a non-table reference as the operand of a closed jump script."""
    if operand == 0 or data[operand - 1] not in (0x08, 0x0A):
        return False
    parsed = parse(data, operand - 1, 8192, extra_glyphs=range(0xB0, 0xC0))
    return (not parsed["error"] and parsed["terminal"] and
            (operand, target) in parsed["refs"])


def fixtures_from_baselines(original, baselines):
    french = translations()
    if len(french) != 114:
        raise ValueError("Le lot V38 doit contenir exactement 114 descriptions")
    refs = {profile: pointer_index(data) for profile, data in baselines.items()}
    scripts = []
    for ident, fr in sorted(french.items()):
        start = int(ident, 16)
        parsed = parse(original, start, 8192)
        if parsed["error"] or not parsed["terminal"] or not parsed["spans"]:
            raise ValueError("Description source non close: " + ident)
        end = parsed["end"]
        spans = [(a - start, b - start) for a, b in parsed["spans"]]
        if len(fr) != len(spans):
            raise ValueError("Nombre de fragments incorrect: " + ident)
        active = {p: refs[p].get(start, []) for p in baselines}
        if active["accents"] != active["ascii"] or not active["accents"]:
            raise ValueError("Appels actifs divergents ou absents: " + ident)
        table_refs, parsed_refs = [], []
        for q in active["accents"]:
            if TABLE_START <= q < TABLE_END and (q - TABLE_START) % 4 == 0:
                table_refs.append(q)
            elif all(command_operand_proof(data, q, start) for data in baselines.values()):
                parsed_refs.append(q)
            else:
                raise ValueError(f"Opérande non prouvé: {ident} à {q:06X}")
        if not table_refs:
            raise ValueError("Description absente de la table: " + ident)
        baseline_hex = {}
        for profile, data in baselines.items():
            if data[start:end] != original[start:end]:
                raise ValueError("Description source déjà modifiée: " + ident)
            baseline_hex[profile] = data[start:end].hex()
        scripts.append({
            "id": ident, "end": f"{end:06X}",
            "english": [render(original[a:b]) for a, b in parsed["spans"]],
            "fr": fr, "spans": [list(x) for x in spans],
            "original_hex": original[start:end].hex(),
            "baseline_hex": baseline_hex,
            "table_refs": [f"{q:06X}" for q in table_refs],
            "parser_proven_alias_refs": [f"{q:06X}" for q in parsed_refs],
            "entry_refs": [f"{q:06X}" for q in active["accents"]],
        })
    return {"version": "v38", "base": "v37", "scripts": scripts}


def allocate(fixtures, profile):
    region = 0
    cursor = RESERVES[0][0]
    built = []
    for entry in fixtures["scripts"]:
        raw = bytes.fromhex(entry["baseline_hex"][profile])
        out, mapping = transform(raw, entry["spans"], entry["fr"], cursor, profile)
        while cursor + len(out) > RESERVES[region][1]:
            region += 1
            if region >= len(RESERVES):
                raise ValueError("Réserves V38 épuisées")
            cursor = RESERVES[region][0]
        built.append((entry, cursor, bytes(out), mapping))
        cursor = (cursor + len(out) + 3) & ~3
    return built, region, cursor


def build(rom_path, out):
    original = Path(rom_path).read_bytes()
    if len(original) != SIZE or sha(original) != ROM_SHA:
        raise ValueError("ROM originale USA 1.2 requise")
    baselines, priors, prior_records = {}, {}, {}
    original_refs = pointer_index(original)
    for profile in ("accents", "ascii"):
        prior = (ROOT / f"patches/EarthBound_Beginnings_FR_v37_{profile}.ips").read_bytes()
        if sha(prior) != BASE_SHA[profile]:
            raise ValueError("IPS V37 non conforme: " + profile)
        rec = records(prior)
        baseline = apply(original, rec)
        refs = pointer_index(baseline)
        for a, b in RESERVES:
            if original[a:b] != bytes(b - a) or baseline[a:b] != bytes(b - a):
                raise ValueError(f"Réserve non nulle: {a:06X}-{b:06X}")
            if any(a <= target < b for target in original_refs) or any(a <= target < b for target in refs):
                raise ValueError(f"Réserve ciblée: {a:06X}-{b:06X}")
            if any(p < b and p + len(raw) > a for p, raw in rec):
                raise ValueError(f"Collision IPS V37: {a:06X}-{b:06X}")
        priors[profile], prior_records[profile], baselines[profile] = prior, rec, baseline

    fixtures = fixtures_from_baselines(original, baselines)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    common_layout = None
    for profile, baseline in baselines.items():
        built, last_region, cursor = allocate(fixtures, profile)
        changes, relocated, rewritten = [], [], []
        for entry, dest, raw, mapping in built:
            old = bytes.fromhex(entry["baseline_hex"][profile])
            checked = parse(raw, 0, len(raw) + 1, extra_glyphs=range(0xB0, 0xC0))
            if checked["error"] or not checked["terminal"] or checked["end"] != len(raw):
                raise ValueError("Copie française non close: " + entry["id"])
            textual = {q for a, b in entry["spans"] for q in range(a, b)}
            for q, byte in enumerate(old):
                if q not in textual and raw[mapping[q]] != byte:
                    raise ValueError("Commande altérée: " + entry["id"])
            changes.append((dest, raw))
            relocated.append({
                "id": entry["id"], "offset": f"{dest:06X}",
                "old_length": len(old), "new_length": len(raw),
                "fragments": len(entry["fr"]),
            })
            for ref in entry["entry_refs"]:
                q = int(ref, 16)
                changes.append((q, pointer(dest)))
                rewritten.append({
                    "offset": ref, "old_target": entry["id"],
                    "new_target": f"{dest:06X}",
                    "proof": "description_table" if entry["table_refs"] and ref in entry["table_refs"]
                             else "parsed_jump_operand",
                })
        spans = sorted((p, p + len(raw)) for p, raw in changes)
        if any(b > c for (_, b), (c, _) in zip(spans, spans[1:])):
            raise ValueError("Écritures V38 en chevauchement")
        ips = append(priors[profile], changes)
        target = apply(original, records(ips))
        if records(ips) != prior_records[profile] + changes or target != apply(baseline, changes):
            raise ValueError("Chaîne IPS V38 non autonome")
        mask = bytearray(SIZE)
        for p, raw in changes:
            mask[p:p + len(raw)] = b"\1" * len(raw)
        if any(a != b for a, b, marked in zip(baseline, target, mask) if not marked):
            raise ValueError("Écriture hors zones V38")
        for entry in fixtures["scripts"]:
            a, b = int(entry["id"], 16), int(entry["end"], 16)
            if target[a:b] != baseline[a:b]:
                raise ValueError("Ancien script modifié: " + entry["id"])
        path = out / f"EarthBound_Beginnings_FR_v38_{profile}.ips"
        path.write_bytes(ips)
        layout = [(e["id"], f"{d:06X}", len(raw)) for e, d, raw, _ in built]
        if common_layout is None:
            common_layout = layout
        elif layout != common_layout:
            raise ValueError("Implantation divergente entre profils")
        results[profile] = {
            "sha256": sha(ips), "target_rom_sha256": sha(target),
            "prior_records_preserved": len(prior_records[profile]),
            "records_added": len(changes), "independent_rom_roundtrip": True,
            "outside_declared_ranges_unchanged": True,
            "last_reserve": last_region, "used_end": f"{cursor:06X}",
            "relocated": relocated, "entry_refs_rewritten": rewritten,
        }

    (ROOT / "tools/v38/v38_descriptions_fr.json").write_text(
        json.dumps(fixtures, ensure_ascii=False, indent=2) + "\n")
    report = {
        "base": "V37", "source_sha256": sha(original),
        "scripts_revised": len(fixtures["scripts"]),
        "newly_translated_descriptions": len(fixtures["scripts"]),
        "newly_translated_fragments": sum(len(e["fr"]) for e in fixtures["scripts"]),
        "already_french_fragments": 0, "unchanged_empty_alias_scripts": 16,
        "source_bank": ["361DB7", "3631F2"],
        "description_table": [f"{TABLE_START:06X}", f"{TABLE_END:06X}"],
        "reservations": [[f"{a:06X}", f"{b:06X}"] for a, b in RESERVES],
        "source_scripts_preserved": True, "all_active_refs_proven": True,
        "profiles": results, "new_scene_emulator_tested": False,
    }
    (ROOT / "tools/v38/validation_v38.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "patches")
    args = parser.parse_args()
    result = build(args.rom, args.out)
    print(json.dumps({k: v for k, v in result.items() if k != "profiles"},
                     ensure_ascii=False, indent=2))
