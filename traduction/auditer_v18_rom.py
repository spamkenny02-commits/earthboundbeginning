#!/usr/bin/env python3
"""Audit V18 sur ROM originale : octets anglais, commandes et pointeurs intérieurs."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from construire_v11 import parse_ips

SHA = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
SPLIT = re.compile(r'(\[[0-9A-Fa-f ]+\]|\n|@)')

def spans_for_script(rom, entry):
    at = start = int(entry['id'], 16)
    english = entry['english']
    spans = []
    if english.startswith('\n\n'):
        if rom[at] != 1:
            raise ValueError('Préfixe 01 manquant ' + entry['id'])
        at += 1
        english = english[2:]
    for part in filter(None, SPLIT.split(english)):
        if part == '\n':
            if rom[at] == 0:
                at += 1
            elif rom[at:at+2] == b'\x03\x00':
                at += 2
            else:
                raise ValueError('Retour de ligne incorrect ' + entry['id'])
            continue
        if part == '@':
            raw = b'\x70'
        elif part.startswith('['):
            raw = bytes.fromhex(part[1:-1])
        else:
            raw = bytes(ord(c)+48 for c in part)
            if re.search('[A-Za-z]', part):
                spans.append((at, len(raw)))
        if rom[at:at+len(raw)] != raw:
            raise ValueError('Source anglaise incorrecte ' + entry['id'] + f' {at:06X}')
        at += len(raw)
    for ref in entry['pointer_refs_declared']:
        pos = int(ref, 16)
        if rom[pos:pos+4] != (0xC00000+start).to_bytes(4, 'little'):
            raise ValueError('Pointeur incorrect ' + entry['id'] + ' ' + ref)
    return spans

def audit(rom, entries, patches):
    if len(rom) != 4194304 or hashlib.sha256(rom).hexdigest() != SHA:
        raise ValueError('ROM USA 1.2 originale requise')
    occupied = bytearray(len(rom))
    for patch in patches:
        for pos, raw in parse_ips(patch):
            occupied[pos:pos+len(raw)] = b'\x01'*len(raw)
    interiors = {}
    lengths = {}
    for e in entries:
        spans = spans_for_script(rom, e)
        lengths[e['id']] = len(spans)
        for pos, n in spans:
            if any(occupied[pos:pos+n]):
                raise ValueError('Collision V17 ' + e['id'])
            for p in range(pos+1, pos+n):
                interiors[p] = e['id']
    unsafe = {}
    for at in range(len(rom)-3):
        if rom[at+3] == 0 and 0xC0 <= rom[at+2] <= 0xFF:
            target = int.from_bytes(rom[at:at+4], 'little') - 0xC00000
            if target in interiors:
                unsafe.setdefault(interiors[target], []).append([f'{at:06X}', f'{target:06X}'])
    safe = [e['id'] for e in entries if e['id'] not in unsafe]
    return {'scripts':len(entries), 'segments':sum(lengths.values()),
            'safe_scripts':len(safe), 'safe_segments':sum(lengths[x] for x in safe),
            'unsafe_scripts':len(unsafe), 'interior_refs':sum(map(len,unsafe.values())),
            'safe_ids':safe, 'unsafe_refs':unsafe}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    parser.add_argument('--sortie', type=Path)
    args = parser.parse_args()
    pre = json.loads((ROOT/'traduction/v18_preselection.json').read_text())
    catalogue = json.loads((ROOT/'traduction/v17_priorites_non_verifiees.json').read_text())
    by_id = {e['id']:e for e in catalogue['entries']}
    patches = [(ROOT/f'patches/EarthBound_Beginnings_FR_v17_{p}.ips').read_bytes()
               for p in ('accents','ascii')]
    result = audit(args.rom.read_bytes(), [by_id[x] for x in pre['ids']], patches)
    if args.sortie:
        args.sortie.write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if isinstance(v,int)})

if __name__ == '__main__':
    main()
