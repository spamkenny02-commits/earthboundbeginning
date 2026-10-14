#!/usr/bin/env python3
"""V24 IPS builder: verified multisegment lines inside pointer-backed scripts.

Requires an original user-owned USA 1.2 ROM; never outputs a ROM.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/v19'))
from build_v19 import ROM_SHA, SIZE, encode, pointer_index, records, apply, append, sha

V23_SHA = {
    'accents': '583556b9f375eb8e4dcec93a09397c38eef88a78cdf3b4667cd22732b7cedbae',
    'ascii': '3d9d4920dd85f2de1f6e176ad8a8c311e92e7cc3094e1429300ab3c74170b056',
}


def load_manifest():
    m = json.loads((ROOT / 'tools/v24/manifest_v24.json').read_text(encoding='utf-8'))
    entries = m['entries']
    if not entries or len({e['id'] for e in entries}) != len(entries):
        raise ValueError('Manifeste vide ou doublons')
    return entries


def verify_entries(rom, entries, extraction):
    refs = pointer_index(rom)
    scripts = {s['id']: s for s in extraction}
    checked = []
    for e in entries:
        ident = e['id']
        p = int(ident, 16)
        n = e['text_length']
        end = p + 1 + n
        if not (0 <= p < end + 2 <= SIZE):
            raise ValueError('Limites ROM: ' + ident)
        if rom[p] != 0x70 or rom[p+1:end] != bytes(ord(c)+48 for c in e['english']):
            raise ValueError('Texte original différent: ' + ident)
        if rom[end:end+2].hex() != e['suffix']:
            raise ValueError('Commande originale différente: ' + ident)
        if any(q in refs for q in range(p+1, end)):
            raise ValueError('Pointeur littéral potentiel intérieur: ' + ident)
        s = scripts[e['script']]
        start = int(s['id'], 16)
        if s['evidence'] != 'literal_pointer' or not (start <= p < end <= start+s['length']):
            raise ValueError('Script parent non attesté: ' + ident)
        raw = bytes.fromhex(s['raw_hex'])
        if rom[start:start+s['length']] != raw:
            raise ValueError('Octets du script parent différents: ' + ident)
        if s['literal_pointer_offsets'] != e['script_refs']:
            raise ValueError('Références du script parent différentes: ' + ident)
        for profile in ('accents', 'ascii'):
            if len(encode(e['fr'], profile)) > n:
                raise ValueError('Dépassement de longueur: ' + ident)
        if e['fr'] == e['english']:
            raise ValueError('Texte inchangé: ' + ident)
        checked.append((p, end, e))
    checked.sort()
    for (a, b, _), (c, d, _) in zip(checked, checked[1:]):
        if b > c:
            raise ValueError(f'Chevauchement interne: {a:06X}/{c:06X}')
    return checked


def build(rom_path, out_dir, *, base_dir=None, expected_base=None):
    rom = Path(rom_path).read_bytes()
    if len(rom) != SIZE or sha(rom) != ROM_SHA:
        raise ValueError('ROM originale USA 1.2 incorrecte')
    entries = load_manifest()
    extraction = json.loads((ROOT/'atelier/extraction/dialogues.json').read_text(encoding='utf-8'))
    checked = verify_entries(rom, entries, extraction)
    output = {}
    for profile in ('accents', 'ascii'):
        base_path = ((Path(base_dir) if base_dir else ROOT/'patches') /
                     f'EarthBound_Beginnings_FR_v23_{profile}.ips')
        old_ips = base_path.read_bytes()
        expected = (expected_base or V23_SHA)[profile]
        if sha(old_ips) != expected:
            raise ValueError('IPS de base non conforme: ' + profile)
        old = records(old_ips)
        baseline = apply(rom, old)
        occupied = bytearray(SIZE)
        for p, payload in old:
            occupied[p:p+len(payload)] = b'\x01'*len(payload)
        changed = bytearray(SIZE)
        additions = []
        for p, end, e in checked:
            if any(occupied[p:end]) or any(changed[p:end]):
                raise ValueError('Collision IPS: ' + e['id'])
            s = next(s for s in extraction if s['id'] == e['script'])
            for q in s['literal_pointer_offsets']:
                q = int(q, 16)
                if baseline[q:q+4] != rom[q:q+4]:
                    raise ValueError('Pointeur de script modifié par la base: ' + e['id'])
            payload = encode(e['fr'], profile).ljust(e['text_length'], b'\x50')
            additions.append((p+1, payload))
            changed[p:end] = b'\x01'*(end-p)
        new_ips = append(old_ips, additions)
        if records(new_ips) != old+additions or new_ips[:len(old_ips)-3] != old_ips[:-3]:
            raise ValueError('Structure IPS / préfixe invalide: ' + profile)
        target = apply(rom, records(new_ips))
        if target != apply(baseline, additions):
            raise ValueError('Roundtrip IPS invalide: ' + profile)
        if any(a != b for a,b,m in zip(target,baseline,changed) if not m):
            raise ValueError('Modification hors lot: ' + profile)
        if any(target[p:p+len(data)] != baseline[p:p+len(data)] for p,data in old):
            raise ValueError('Régression de la base: ' + profile)
        output[profile] = (new_ips, {
            'prior_records': len(old), 'new_segments': len(additions),
            'sha256': sha(new_ips), 'target_rom_sha256': sha(target),
            'roundtrip': True, 'no_regression': True})
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for profile,(ips,meta) in output.items():
        (out_dir/f'EarthBound_Beginnings_FR_v24_{profile}.ips').write_bytes(ips)
    return {'base':'v23','source_rom_sha256':sha(rom),'new_segments':len(entries),
            'profiles':{p:v[1] for p,v in output.items()}}


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--rom',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args()
    print(json.dumps(build(args.rom,args.out),indent=2))