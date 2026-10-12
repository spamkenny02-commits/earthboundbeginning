#!/usr/bin/env python3
"""Entrée isolée dans un dialogue intégré ; aucune validation de quête."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('rom', type=Path)
parser.add_argument('rapport', type=Path)
parser.add_argument('sortie', type=Path)
parser.add_argument('--id', required=True, help='Identifiant de dialogue accepté dans le rapport')
args = parser.parse_args()
source = args.rom.read_bytes()
report = json.loads(args.rapport.read_text(encoding='utf-8'))
assert hashlib.sha256(source).hexdigest() == report['target_sha256']
entry = next(row for row in report['accepted']
             if row['id'] == args.id and row['type'] in ('dialogue','relocated_dialogue'))
target = int(entry['offset'] if entry['type']=='relocated_dialogue' else entry['id'], 16)
offset = 0x07c588
result = bytearray(source)
result[offset:offset + 6] = b'\x0a' + (0xc00000 + target).to_bytes(4, 'little') + b'\x02'
assert all(a == b for i, (a, b) in enumerate(zip(source, result))
           if not offset <= i < offset + 6)
args.sortie.parent.mkdir(parents=True, exist_ok=True)
args.sortie.write_bytes(result)
metadata = {'scope': 'Dialogue déclenché directement ; parcours et conditions de quête non validés',
            'base_rom_sha256': report['target_sha256'],
            'test_rom_sha256': hashlib.sha256(result).hexdigest(),
            'entry_id': args.id, 'resolved_target': f'{target:06X}', 'entry_type': entry['type'], 'changed_interval': ['07C588', '07C58E']}
args.sortie.with_suffix('.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2),
                                        encoding='utf-8')
print(json.dumps(metadata, ensure_ascii=False))
