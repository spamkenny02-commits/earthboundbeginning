#!/usr/bin/env python3
"""V30 read-only candidate audit. Never edits ROM, pointers or IPS files.

Candidates are NOT translated or integrated. Requires the user's original
USA 1.2 ROM and the published V29 accents/ASCII IPS files.
"""
import argparse
import json
import sys
from collections import Counter
from bisect import bisect_left
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def span_reason(source, baselines, occupied, ref_maps, start, end):
    """Conservative safety gate for a *text* span, with exclusive end."""
    if not 0 <= start < end <= len(source):
        return 'invalid_bounds'
    if any(len(base) != len(source) for base in baselines):
        return 'wrong_baseline_size'
    if any(occupied[start:end]):
        return 'ips_collision'
    if any(base[start:end] != source[start:end] for base in baselines):
        return 'baseline_changed'
    # Even a pointer to the beginning is deferred until its semantics are known.
    for refs in ref_maps:
        keys = refs if isinstance(refs, list) else sorted(refs)
        i = bisect_left(keys, start)
        if i < len(keys) and keys[i] < end:
            return 'interior_or_direct_pointer'
    if any(not 0x50 <= x <= 0xAA for x in source[start:end]):
        return 'not_plain_ascii_text'
    return None


def commands_preserved(source, baselines, start, end, spans):
    if not 0 <= start < end <= len(source):
        return False
    mask = bytearray(end - start)
    for a, b in spans:
        if not start <= a < b <= end:
            return False
        mask[a-start:b-start] = b'\1' * (b-a)
    return all(all(src == base[i] for base in baselines)
               for i, src in enumerate(source[start:end], start)
               if not mask[i-start])


def audit(rom_path, repo=ROOT, limit=200):
    if not 1 <= limit <= 500:
        raise ValueError('limit must be 1..500')
    repo = Path(repo)
    sys.path.insert(0, str(repo/'tools/v19'))
    sys.path.insert(0, str(repo/'traduction'))
    from build_v19 import ROM_SHA, SIZE, sha, records, apply, pointer_index
    from preparer_v17 import decode_layout

    source = Path(rom_path).read_bytes()
    if len(source) != SIZE or sha(source) != ROM_SHA:
        raise ValueError('Original unheadered USA 1.2 ROM required')
    report = json.loads((repo/'tools/v29/validation_v29.json').read_text(encoding='utf-8'))
    baselines = []
    occupied = bytearray(SIZE)
    for profile in ('accents', 'ascii'):
        ips = (repo/f'patches/EarthBound_Beginnings_FR_v29_{profile}.ips').read_bytes()
        if sha(ips) != report['profiles'][profile]['sha256']:
            raise ValueError('V29 IPS SHA mismatch: '+profile)
        rec = records(ips)
        baselines.append(apply(source, rec))
        for pos, payload in rec:
            occupied[pos:pos+len(payload)] = b'\1' * len(payload)
    ref_maps = [pointer_index(data) for data in [source, *baselines]]
    ref_targets = [sorted(refs) for refs in ref_maps]
    catalogue = json.loads((repo/'catalogue/catalogue.json').read_text(encoding='utf-8'))
    counts = Counter()
    candidates = []
    seen = set()
    for row in catalogue['entries']:
        if row.get('category') != 'script' or row.get('status') != 'a_examiner':
            continue
        counts['scripts_examined'] += 1
        try:
            start = int(row['id'], 16)
        except (KeyError, TypeError, ValueError):
            counts['bad_script_id'] += 1
            continue
        layout = decode_layout(source, start, row.get('english', ''))
        if layout is None:
            counts['unverified_layout'] += 1
            continue
        end, _, spans = layout
        incoming = ref_maps[0].get(start, [])
        if not incoming:
            counts['no_literal_script_entry'] += 1
            continue
        if any(refs.get(start, []) != incoming for refs in ref_maps[1:]):
            counts['script_entry_refs_changed'] += 1
            continue
        if any(any(base[p:p+4] != source[p:p+4] for base in baselines)
               for p in incoming):
            counts['script_entry_bytes_changed'] += 1
            continue
        if not commands_preserved(source, baselines, start, end, spans):
            counts['script_commands_changed'] += 1
            continue
        for index, (a, b) in enumerate(spans):
            if (a, b) in seen:
                counts['duplicate_span'] += 1
                continue
            seen.add((a, b))
            reason = span_reason(source, baselines, occupied, ref_targets, a, b)
            if reason:
                counts[reason] += 1
                continue
            english = ''.join(chr(x-48) for x in source[a:b])
            if len(english.strip()) < 8 or not any(c.isalpha() for c in english):
                counts['short_or_nonverbal'] += 1
                continue
            candidates.append({
                'id': f'{a:06X}', 'english': english, 'text_length': b-a,
                'script_id': f'{start:06X}', 'script_span_index': index,
                'script_span_count': len(spans),
                'script_refs': [f'{p:06X}' for p in incoming],
                'source_sha256': ROM_SHA,
                'status': 'untranslated_candidate',
            })
    candidates.sort(key=lambda item: int(item['id'], 16))
    return {
        'base': 'V29', 'status': 'candidates_only', 'integrated_blocks': 0,
        'source_rom_sha256': ROM_SHA,
        'audited_candidate_count': len(candidates),
        'returned_candidate_count': min(limit, len(candidates)),
        'counts': dict(sorted(counts.items())),
        'candidates': candidates[:limit],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--limit', type=int, default=200)
    args = parser.parse_args()
    result = audit(args.rom, args.repo, args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'candidates'}, indent=2))


if __name__ == '__main__':
    main()
