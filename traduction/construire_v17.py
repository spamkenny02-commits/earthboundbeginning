#!/usr/bin/env python3
"""V17: assemblage IPS autonome V16 + 195 segments vérifiés."""
import argparse
import hashlib
import json
from pathlib import Path
import construire_v17_core as core
from construire_v17_core import merge_sources, derive_mask, literal_refs, validate_and_spans
from construire_v11 import encode, apply_ips, parse_ips
ROOT = core.ROOT
ROM_SIZE = core.ROM_SIZE
ROM_SHA = core.ROM_SHA

def append_ips(source, previous, spans):
    results = {}
    for profile in ('accents', 'ascii'):
        prior = previous[profile]
        old_records = parse_ips(prior)
        occupied = sorted((p, p + len(raw)) for p, raw in old_records)
        old_rom = apply_ips(source, prior)
        target = bytearray(old_rom)
        extra = bytearray()
        for pos, english, french, ident in spans:
            end = pos + len(english)
            if any(a < end and b > pos for a, b in occupied):
                raise ValueError('Collision IPS V16 : ' + ident + ' / ' + profile)
            if old_rom[pos:end] != english:
                raise ValueError('ROM V16 non identique à la source : ' + ident)
            encoded = encode(french, profile == 'accents')
            if len(encoded) > len(english):
                raise ValueError('Texte trop long : ' + ident + ' / ' + profile)
            data = encoded.ljust(len(english), b'\x50')
            target[pos:end] = data
            extra += pos.to_bytes(3, 'big') + len(data).to_bytes(2, 'big') + data
        merged = prior[:-3] + extra + b'EOF'
        if parse_ips(merged)[:len(old_records)] != old_records:
            raise AssertionError('Régression IPS V16 : ' + profile)
        if apply_ips(source, merged) != bytes(target):
            raise AssertionError('Échec roundtrip IPS : ' + profile)
        results[profile] = (merged, hashlib.sha256(target).hexdigest())
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom_originale', type=Path)
    parser.add_argument('--candidats', type=Path, default=ROOT / 'traduction/v17_candidats_controles.json')
    parser.add_argument('--traductions', type=Path, default=ROOT / 'traduction/v17_traductions_117.json')
    parser.add_argument('--sortie', type=Path, default=ROOT / 'build_v17')
    args = parser.parse_args()
    source = args.rom_originale.read_bytes()
    if len(source) == ROM_SIZE + 512:
        source = source[512:]
    candidates = json.loads(args.candidats.read_text(encoding='utf-8'))
    translations = json.loads(args.traductions.read_text(encoding='utf-8'))
    entries = merge_sources(candidates, translations)
    spans, refs = validate_and_spans(source, entries)
    previous = {p: (ROOT / f'patches/EarthBound_Beginnings_FR_v16_{p}.ips').read_bytes()
                for p in ('accents', 'ascii')}
    results = append_ips(source, previous, spans)
    # N'écrire les sorties qu'après la validation complète des deux profils.
    args.sortie.mkdir(parents=True, exist_ok=True)
    for profile, (ips, target_sha) in results.items():
        filename = f'EarthBound_Beginnings_FR_v17_{profile}.ips'
        (args.sortie / filename).write_bytes(ips)
        print(profile, len(ips), 'octets; SHA-256 ROM cible', target_sha)
    print('V17 :', len(entries), 'scripts et', len(spans), 'segments français intégrés')


if __name__ == '__main__':
    main()