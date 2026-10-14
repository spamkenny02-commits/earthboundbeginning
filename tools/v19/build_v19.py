#!/usr/bin/env python3
"""Construct V19 from the *published* V18 Work IPS; no commercial ROM is shipped.

Example (inside a checkout of spamkenny02-commits/earthboundbeginning):
python tools/v19/build_v19.py --repo . --rom '/path/original.sfc' --out build_v19
python tools/v19/build_v19.py --repo . --check-only

This script is prepared locally, not yet published to the repository.
"""
import argparse
import hashlib
import json
from pathlib import Path
import unicodedata

ROM_SHA = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
BASE_SHA = {
    'accents': '26939d61747b15515538ccfce7abcf09fec44abfc368f18064c7f75c13e5f285',
    'ascii': 'ba5cd811c809b312f9ba88bb0c5f8a0791a3a95b10e7f5ece8e5c5b9598b8f2f',
}
ACCENTS = 'éèêëàâîïôùûüçÉÀÇ'
SIZE = 4 * 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(text, profile):
    if profile == 'ascii':
        text = ''.join(c for c in unicodedata.normalize('NFD', text)
                       if not unicodedata.combining(c))
    out = bytearray()
    for ch in text:
        if profile == 'accents' and ch in ACCENTS:
            out.append(0xB0 + ACCENTS.index(ch))
        elif 32 <= ord(ch) <= 122 and ch not in '"[\\]^':
            out.append(ord(ch) + 48)
        else:
            raise ValueError(f'Unsupported glyph: {ch!r}')
    return bytes(out)


def records(data):
    if data[:5] != b'PATCH':
        raise ValueError('Bad IPS header')
    out, i = [], 5
    while True:
        if i + 3 > len(data):
            raise ValueError('Truncated IPS')
        if data[i:i+3] == b'EOF':
            if i + 3 != len(data):
                raise ValueError('Unsupported IPS trailer')
            return out
        if i + 5 > len(data):
            raise ValueError('Truncated IPS record header')
        pos = int.from_bytes(data[i:i+3], 'big')
        n = int.from_bytes(data[i+3:i+5], 'big')
        i += 5
        if n:
            if i + n > len(data):
                raise ValueError('Truncated IPS payload')
            payload = data[i:i+n]
            i += n
        else:
            if i + 3 > len(data):
                raise ValueError('Truncated IPS RLE')
            count = int.from_bytes(data[i:i+2], 'big')
            if not count:
                raise ValueError('Zero IPS RLE')
            payload = data[i+2:i+3] * count
            i += 3
        if pos + len(payload) > SIZE:
            raise ValueError('IPS out of ROM')
        out.append((pos, payload))


def apply(data, entries):
    out = bytearray(data)
    for pos, payload in entries:
        if pos + len(payload) > len(out):
            raise ValueError('IPS out of bounds')
        out[pos:pos+len(payload)] = payload
    return bytes(out)


def append(prior, additions):
    records(prior)
    result = bytearray(prior[:-3])
    for pos, payload in additions:
        if not payload or len(payload) > 65535 or pos == 0x454F46:
            raise ValueError('Unrepresentable IPS record')
        result.extend(pos.to_bytes(3, 'big'))
        result.extend(len(payload).to_bytes(2, 'big'))
        result.extend(payload)
    return bytes(result + b'EOF')


def read_translations(path):
    out = {}
    for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        if line.count('\t') != 1:
            raise ValueError(f'Line {line_no}: expected one tab')
        ident, french = line.split('\t')
        if len(ident) != 6 or any(c not in '0123456789ABCDEF' for c in ident):
            raise ValueError(f'Line {line_no}: invalid hex ID')
        if ident in out or not french or french != french.strip():
            raise ValueError(f'Line {line_no}: duplicate, empty or padded text')
        out[ident] = french
    if not out:
        raise ValueError('No translations')
    return out


def pointer_index(rom):
    refs = {}
    for p in range(len(rom) - 3):
        if rom[p+3] == 0 and 0xC0 <= rom[p+2] <= 0xFF:
            target = int.from_bytes(rom[p:p+4], 'little') - 0xC00000
            if 0 <= target < len(rom):
                refs.setdefault(target, []).append(p)
    return refs


def build(repo, translations_file, rom_path=None, out_dir=None):
    candidates = {e['id']: e for e in json.loads(
        (repo/'tools/v18_work/sources/v18_work_candidates.json').read_text(encoding='utf-8'))}
    previous = {e['id'] for e in json.loads(
        (repo/'tools/v18_work/v18_work_dialogues_fr.json').read_text(encoding='utf-8'))['entries']}
    translations = read_translations(translations_file)
    if previous.intersection(translations):
        raise ValueError('Already integrated in V18 Work')
    rom = Path(rom_path).read_bytes() if rom_path else None
    if rom is not None and (len(rom) != SIZE or sha(rom) != ROM_SHA):
        raise ValueError('Original ROM SHA-256 mismatch')
    refs = pointer_index(rom) if rom is not None else None
    output, planned = {}, []
    for profile in ('accents', 'ascii'):
        prior = (repo/f'patches/EarthBound_Beginnings_FR_v18_work_{profile}.ips').read_bytes()
        if sha(prior) != BASE_SHA[profile]:
            raise ValueError(f'Wrong V18 Work IPS: {profile}')
        old = records(prior)
        prior_rom = apply(rom, old) if rom is not None else None
        occupied = bytearray(SIZE)
        for pos, payload in old:
            occupied[pos:pos+len(payload)] = b'\x01'*len(payload)
        added, changed = [], bytearray(SIZE)
        for ident, french in translations.items():
            if ident not in candidates:
                raise ValueError(f'Unknown candidate: {ident}')
            e = candidates[ident]
            pos, n = int(ident, 16), e['text_length']
            encoded = encode(french, profile)
            if len(encoded) > n:
                raise ValueError(f'Overlong translation: {ident} ({len(encoded)} > {n})')
            if french == e['english']:
                raise ValueError(f'Unchanged: {ident}')
            if any(occupied[pos:pos+1+n]) or any(changed[pos:pos+1+n]):
                raise ValueError(f'IPS overlap: {ident}')
            if rom is not None:
                end = pos + 1 + n
                if rom[pos] != 0x70 or rom[pos+1:end] != bytes(ord(c)+48 for c in e['english']):
                    raise ValueError(f'Original English mismatch: {ident}')
                if rom[end:end+2].hex() != e['suffix']:
                    raise ValueError(f'Command suffix mismatch: {ident}')
                if pos not in refs and rom[pos-2:pos] not in (b'\x03\x00', b'\x13\x02'):
                    raise ValueError(f'Unverified text boundary: {ident}')
                if [f'{p:06X}' for p in refs.get(pos, [])] != e['refs']:
                    raise ValueError(f'HiROM literal pointer mismatch: {ident}')
                # The base IPS may deliberately zero or rewrite an original pointer.
                # Never count unreachable text as a safely integrated dialogue.
                for pointer_at in refs.get(pos, []):
                    if prior_rom[pointer_at:pointer_at+4] != rom[pointer_at:pointer_at+4]:
                        raise ValueError(f'Base IPS altered pointer to candidate: {ident} at {pointer_at:06X}')
                if any(i in refs for i in range(pos+1, end)):
                    raise ValueError(f'Interior literal pointer: {ident}')
            payload = encoded.ljust(n, b'\x50')
            added.append((pos+1, payload))
            changed[pos:pos+1+n] = b'\x01'*(n+1)
        if len(added) != len(translations):
            raise ValueError('Translation count mismatch')
        merged = append(prior, added)
        if records(merged) != old+added or merged[:len(prior)-3] != prior[:-3]:
            raise ValueError('IPS roundtrip or base regression')
        if rom is not None:
            baseline = apply(rom, old)
            result = apply(rom, records(merged))
            if result != apply(baseline, added):
                raise ValueError('ROM roundtrip mismatch')
            if any(result[pos:pos+len(data)] != baseline[pos:pos+len(data)] for pos,data in old):
                raise ValueError('Prior IPS bytes changed')
            if any(a != b for a,b,m in zip(result,baseline,changed) if not m):
                raise ValueError('Unexpected ROM difference')
        output[profile] = (merged, {'prior_records':len(old),'added_records':len(added),
                                     'sha256':sha(merged),'rom_verified':rom is not None})
        planned = list(translations)
    if rom is not None and out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        for profile,(ips,_) in output.items():
            (out_dir/f'EarthBound_Beginnings_FR_v19_{profile}.ips').write_bytes(ips)
        (out_dir/'validation_v19.json').write_text(json.dumps({
            'base':'v18_work','new_segments':len(planned),
            'source_rom_sha256':sha(rom),'profiles':{k:v[1] for k,v in output.items()},
        },indent=2)+'\n',encoding='utf-8')
    return {'base':'v18_work','segments':len(planned),
            'rom_verified':rom is not None,'profiles':{k:v[1] for k,v in output.items()}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--rom',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--translations',type=Path,default=Path(__file__).with_name('translations_v19.tsv'))
    parser.add_argument('--check-only',action='store_true')
    args = parser.parse_args()
    if not args.check_only and (args.rom is None or args.out is None):
        parser.error('Supply --rom and --out to build IPS, or --check-only to validate without ROM')
    print(json.dumps(build(args.repo,args.translations,None if args.check_only else args.rom,
                           None if args.check_only else args.out),indent=2))
