#!/usr/bin/env python3
"""V18 : contrôle des pointeurs déclarés sur ROM originale, sans écrire la ROM."""
import argparse
import hashlib
import json
from pathlib import Path

SHA = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
ROOT = Path(__file__).resolve().parents[1]

def verify(rom, preselection, catalogue):
    if len(rom) != 4194304 or hashlib.sha256(rom).hexdigest() != SHA:
        raise ValueError('ROM USA 1.2 originale requise')
    by_id = {e['id']: e for e in catalogue['entries']}
    checks = 0
    for ident in preselection['ids']:
        e = by_id[ident]
        ptr = (0xC00000 + int(ident, 16)).to_bytes(4, 'little')
        for ref in e['pointer_refs_declared']:
            at = int(ref, 16)
            if rom[at:at+4] != ptr:
                raise ValueError(f'Pointeur incorrect {ident} à {ref}')
            checks += 1
    return len(preselection['ids']), checks

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('rom', type=Path)
    args = p.parse_args()
    pre = json.loads((ROOT/'traduction/v18_preselection.json').read_text())
    cat = json.loads((ROOT/'traduction/v17_priorites_non_verifiees.json').read_text())
    print('OK V18 : %d scripts et %d pointeurs littéraux déclarés' % verify(args.rom.read_bytes(), pre, cat))

if __name__ == '__main__':
    main()
