#!/usr/bin/env python3
"""Prépare des candidats V17 non traduits depuis la ROM personnelle.

Aucun IPS n'est généré. Seuls les scripts dont les octets, les pointeurs
littéraux HiROM et l'absence de collision V16 sont démontrés sont retenus.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROM_SHA = "e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c"
ROM_SIZE = 4 * 1024 * 1024
PARTS = re.compile(r"(\[[0-9A-Fa-f ]+\]|@|\n)")


def parse_ips(data):
    if not data.startswith(b"PATCH"):
        raise ValueError("IPS sans en-tête PATCH")
    i = 5
    while i < len(data):
        if data[i:i+3] == b"EOF":
            if i + 3 != len(data):
                raise ValueError("Octets après EOF IPS")
            return
        if i + 5 > len(data):
            raise ValueError("Enregistrement IPS tronqué")
        at = int.from_bytes(data[i:i+3], "big")
        size = int.from_bytes(data[i+3:i+5], "big")
        i += 5
        if size:
            if i + size > len(data):
                raise ValueError("Données IPS tronquées")
            i += size
        else:
            if i + 3 > len(data):
                raise ValueError("RLE IPS tronqué")
            size = int.from_bytes(data[i:i+2], "big")
            i += 3
        if size == 0 or at + size > ROM_SIZE:
            raise ValueError("Enregistrement IPS vide ou hors ROM")
        yield at, at + size
    raise ValueError("IPS sans EOF")


def _merge_intervals(spans):
    merged = []
    for lo, hi in sorted(spans):
        if merged and lo <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged


def occupied_spans(ips):
    return _merge_intervals(parse_ips(ips))


def overlaps(lo, hi, spans):
    import bisect
    i = bisect.bisect_left(spans, (lo, -1))
    return (i < len(spans) and spans[i][0] < hi or
            i > 0 and spans[i-1][1] > lo)


def decode_layout(source, start, english):
    """Reconstitue les commandes et les retours 00 / 03 00."""
    if (not english.endswith("[02]") or "@" not in english or
            english.count("\n") > 12 or len(english) > 900 or
            len(re.findall(r"\[[0-9A-Fa-f ]+\]", english)) > 40):
        return None
    parts = [p for p in PARTS.split(english) if p]
    choices = [(start, 0, [])]  # offset, masque de retours, segments texte
    newline_index = 0
    for part in parts:
        next_choices = []
        if part == "\n":
            for pos, mask, spans in choices:
                for marker, short in ((b"\x00", True), (b"\x03\x00", False)):
                    if source[pos:pos+len(marker)] == marker:
                        next_choices.append((pos+len(marker),
                                             mask | ((1 << newline_index) if short else 0),
                                             spans))
            newline_index += 1
        else:
            if part == "@":
                payload = b"\x70"
            elif part.startswith("[") and part.endswith("]"):
                try:
                    payload = bytes.fromhex(part[1:-1])
                except ValueError:
                    return None
                if not payload:
                    return None
            else:
                if any(not 32 <= ord(c) <= 122 or c in "[]" for c in part):
                    return None
                payload = bytes(ord(c) + 48 for c in part)
            for pos, mask, spans in choices:
                if source[pos:pos+len(payload)] == payload:
                    new_spans = spans if (part == "@" or part.startswith("[")) else spans + [(pos, pos+len(payload))]
                    next_choices.append((pos+len(payload), mask, new_spans))
        choices = next_choices
        if not choices:
            return None
    if len(choices) != 1:
        return None
    end, mask, spans = choices[0]
    return (end, mask, spans) if spans and end > start else None


def pointer_map(source):
    refs = {}
    for i in range(len(source)-3):
        if source[i+3] == 0 and 0xC0 <= source[i+2] <= 0xFF:
            target = int.from_bytes(source[i:i+4], "little") - 0xC00000
            if 0 <= target < len(source):
                refs.setdefault(target, []).append(i)
    return refs


def prepare(source, catalogue, ips_accents, ips_ascii=None, limit=120):
    if not 1 <= limit <= 500:
        raise ValueError("Limite attendue : 1 à 500")
    if len(source) != ROM_SIZE:
        raise ValueError("ROM source : 4 Mio sans en-tête attendus")
    if not isinstance(catalogue.get("entries"), list):
        raise ValueError("Catalogue sans entries")
    refs = pointer_map(source)
    occupied = occupied_spans(ips_accents)
    if ips_ascii is not None:
        occupied = _merge_intervals(occupied + occupied_spans(ips_ascii))
    reasons = Counter()
    candidates = []
    used = set()
    selected_ranges = []
    for row in catalogue["entries"]:
        if row.get("category") != "script" or row.get("status") != "a_examiner":
            continue
        reasons["examines"] += 1
        try:
            start = int(row["id"], 16)
        except (ValueError, TypeError, KeyError):
            reasons["id_invalide"] += 1
            continue
        if start in used:
            reasons["id_duplique"] += 1
            continue
        used.add(start)
        layout = decode_layout(source, start, row.get("english", ""))
        if layout is None:
            reasons["format_ou_source_non_conforme"] += 1
            continue
        end, mask, spans = layout
        if overlaps(start, end, occupied) or overlaps(start, end, selected_ranges):
            reasons["collision_ips_ou_candidat"] += 1
            continue
        declared = row.get("incoming_literal_candidates") or []
        actual = refs.get(start, [])
        if not actual or not declared:
            reasons["pointeur_debut_absent"] += 1
            continue
        try:
            declared_int = {int(s, 16) for s in declared}
        except (ValueError, TypeError):
            reasons["pointeur_declare_invalide"] += 1
            continue
        if not declared_int.issubset(set(actual)):
            reasons["pointeur_declare_non_conforme"] += 1
            continue
        if any(any(at in refs for at in range(lo+1, hi)) for lo, hi in spans):
            reasons["pointeur_interieur"] += 1
            continue
        translations = [p for p in PARTS.split(row["english"])
                        if p and p not in ("@", "\n") and
                        not (p.startswith("[") and p.endswith("]")) and
                        re.search("[A-Za-z]", p)]
        if not translations:
            reasons["segment_non_linguistique"] += 1
            continue
        reasons["eligibles"] += 1
        if len(candidates) < limit:
            candidates.append({"id": f"{start:06X}", "english": row["english"],
                               "translations": translations,
                               "pointer_refs": [f"{p:06X}" for p in actual],
                               "newline_one_byte_mask": mask,
                               "status": "a_traduire_et_revalider"})
            selected_ranges.append((start, end))
            selected_ranges.sort()
    reasons["selectionnes"] = len(candidates)
    return {"version": "v17-preparation", "base": "v16",
            "notes": "Candidats anglais inchangés, non intégrés. Relire et tester avant tout IPS.",
            "entries": candidates}, dict(reasons)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom_originale", type=Path)
    p.add_argument("--catalogue", type=Path, default=Path("catalogue/catalogue.json"))
    p.add_argument("--ips-v16-accents", type=Path,
                   default=Path("patches/EarthBound_Beginnings_FR_v16_accents.ips"))
    p.add_argument("--ips-v16-ascii", type=Path,
                   default=Path("patches/EarthBound_Beginnings_FR_v16_ascii.ips"))
    p.add_argument("--sortie", type=Path, default=Path("build_v17/candidats.json"))
    p.add_argument("--rapport", type=Path, default=Path("build_v17/audit.json"))
    p.add_argument("--limite", type=int, default=120)
    a = p.parse_args()
    rom = a.rom_originale.read_bytes()
    if len(rom) == ROM_SIZE + 512:
        rom = rom[512:]
    digest = hashlib.sha256(rom).hexdigest()
    if digest != ROM_SHA:
        p.error("ROM USA 1.2 originale requise : SHA-256 incorrect")
    catalogue = json.loads(a.catalogue.read_text(encoding="utf-8-sig"))
    ips_accents = a.ips_v16_accents.read_bytes()
    ips_ascii = a.ips_v16_ascii.read_bytes()
    manifest, stats = prepare(rom, catalogue, ips_accents, ips_ascii, a.limite)
    report = {"rom_sha256": digest,
              "ips_v16_accents_sha256": hashlib.sha256(ips_accents).hexdigest(),
              "ips_v16_ascii_sha256": hashlib.sha256(ips_ascii).hexdigest(),
              "statistiques": stats, "patch_v17_publie": False,
              "avertissement": "Contrôle des pointeurs littéraux uniquement ; pointeurs indirects et rendu restent à vérifier."}
    for path, data in ((a.sortie, manifest), (a.rapport, report)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
