"""Rebuild the Work V18 extension from the supplied original ROM and frozen V18 base.

Usage: python3 sources/build_work.py /absolute/path/to/source.sfc
"""
from pathlib import Path
import argparse
import json
import unicodedata
from ips import ROM_SHA, sha, records, apply, append

ROOT = Path(__file__).resolve().parents[1]
ACCENTS = 'éèêëàâîïôùûüçÉÀÇ'
BASE_SHA = {
    'accents': '57d51063d9f809846312862dfcf0737887c475750de42b0b6a967d2b21c61c7b',
    'ascii': 'fb45610ef36547fffdbc4a2102a6e56ae25459605135983090ef7e6ab2a5778c',
}

def encode(text, profile):
    if profile == 'ascii':
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if not unicodedata.combining(c))
    result = bytearray()
    for c in text:
        if profile == 'accents' and c in ACCENTS:
            result.append(0xB0 + ACCENTS.index(c))
        elif 32 <= ord(c) <= 122 and c not in '"[\\]^':
            result.append(ord(c) + 48)
        else:
            raise ValueError(f'Unsupported character {c!r}')
    return bytes(result)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def pointer_index(rom):
    refs = {}
    for p in range(len(rom)-3):
        if rom[p+3] == 0 and 0xC0 <= rom[p+2] <= 0xFF:
            t = int.from_bytes(rom[p:p+4], 'little') - 0xC00000
            if 0 <= t < len(rom):
                refs.setdefault(t, []).append(p)
    return refs

def build(rom_path):
    rom = Path(rom_path).read_bytes()
    require(sha(rom) == ROM_SHA, 'Wrong source ROM SHA-256')
    candidates = {e['id']: e for e in json.loads((ROOT/'sources/v18_work_candidates.json').read_text())}
    translations = []
    seen = set()
    for line in (ROOT/'sources/translations_work.tsv').read_text().splitlines():
        ident, french = line.split('\t')
        require(ident not in seen, 'Duplicate translation ID')
        seen.add(ident)
        require(ident in candidates, f'Missing candidate {ident}')
        translations.append({**candidates[ident], 'fr': french})
    refs = pointer_index(rom)
    report = {'source_sha256': sha(rom), 'new_segments': len(translations), 'profiles': {}}
    for profile in ('accents', 'ascii'):
        prior = (ROOT/'base'/f'EarthBound_Beginnings_FR_v18_{profile}.ips').read_bytes()
        require(sha(prior) == BASE_SHA[profile], 'Wrong base IPS SHA-256')
        old = records(prior)
        baseline = apply(rom, old)
        occupied = bytearray(len(rom))
        for p, b in old:
            occupied[p:p+len(b)] = b'\1'*len(b)
        changed = bytearray(len(rom))
        additions = []
        for e in translations:
            p = int(e['id'], 16)
            n = e['text_length']
            end = p+1+n
            require(rom[p] == 0x70, f'Missing text marker {e["id"]}')
            require(rom[p+1:end] == bytes(ord(c)+48 for c in e['english']), 'Source text mismatch')
            require(rom[end:end+2].hex() == e['suffix'], 'Command mismatch')
            require(p in refs or rom[p-2:p] in (b'\x03\x00', b'\x13\x02'), 'Unverified text boundary')
            require([f'{x:06X}' for x in refs.get(p, [])] == e['refs'], 'Pointer reference mismatch')
            require(not any(t in refs for t in range(p+1, end)), 'Interior literal pointer')
            require(not any(occupied[p:end]), 'Base collision')
            require(not any(changed[p:end]), 'New translation collision')
            encoded = encode(e['fr'], profile)
            require(len(encoded) <= n, f'Text too long {e["id"]}')
            payload = encoded.ljust(n, b'\x50')
            require(payload != rom[p+1:end], 'Unchanged translation')
            additions.append((p+1, payload))
            changed[p+1:end] = b'\1'*n
        merged = append(prior, additions)
        parsed = records(merged)
        require(parsed == old+additions, 'IPS records not preserved')
        target = apply(rom, parsed)
        expected = apply(baseline, additions)
        require(target == expected, 'IPS reconstruction mismatch')
        require(all(a == b for a,b,m in zip(target, baseline, changed) if not m), 'Unexpected change outside additions')
        require(all(target[p:p+len(b)] == baseline[p:p+len(b)] for p,b in old), 'Base regression')
        # Every text marker, suffix and recorded pointer source remains byte-identical.
        for e in translations:
            p = int(e['id'],16); end = p+1+e['text_length']
            require(target[p] == baseline[p], 'Text marker changed')
            require(target[end:end+2] == baseline[end:end+2], 'Command changed')
            for reference in e['refs']:
                q = int(reference,16)
                require(target[q:q+4] == baseline[q:q+4], 'Pointer bytes changed')
        dest = ROOT/f'EarthBound_Beginnings_FR_v18_work_{profile}.ips'
        dest.write_bytes(merged)
        report['profiles'][profile] = {
            'base_records': len(old), 'added_records': len(additions),
            'patch_sha256': sha(merged), 'target_rom_sha256': sha(target),
            'preserved_base_record_bytes': sum(len(b) for p,b in old),
            'roundtrip': True, 'outside_additions_unchanged': True,
            'commands_and_recorded_pointers_preserved': True,
        }
    (ROOT/'v18_work_dialogues_fr.json').write_text(json.dumps({'version':'v18_work','entries':translations}, ensure_ascii=False,indent=2)+'\n')
    (ROOT/'validation_work.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rom')
    args = parser.parse_args()
    print(json.dumps(build(args.rom), indent=2))
