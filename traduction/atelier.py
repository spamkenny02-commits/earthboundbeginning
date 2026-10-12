#!/usr/bin/env python3
"""Atelier CLI : CSV éditable et reconstruction vérifiée des deux variantes."""
import argparse
import hashlib
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from integrer import ROOT, encode_fr

FILES = {'field': 'menus_objets_fr.json', 'dialogue': 'dialogues_fr.json'}
COLUMNS = ['type', 'id', 'segment', 'original', 'francais', 'octets_fr', 'etat_integration']
NATIVE = re.compile(r'\[(?:8B|8C|8D|8E|AB|AC|AD|AE)\]')


def load():
    return {kind: json.loads((ROOT / 'traduction' / name).read_text(encoding='utf-8'))
            for kind, name in FILES.items()}


def entries(data):
    for kind, rows in data.items():
        for row in rows:
            if kind == 'field':
                yield (kind, row['id'], '0'), row['text_en'], row['text_fr'], row
            else:
                for index, seg in enumerate(row['text_fr_segments']):
                    yield (kind, row['id'], str(index)), seg['original'], seg['french'], seg


def export_csv(path, report_path=None):
    status = {}
    if report_path:
        report = json.loads(report_path.read_text(encoding='utf-8'))
        status.update({r['id']: 'integre' for r in report['accepted']})
        status.update({r['id']: 'exclu: ' + r['reason'] for r in report['rejected']})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(COLUMNS)
        for key, original, french, _ in entries(load()):
            writer.writerow([*key, original, french, len(encode_fr(french)),
                             status.get(key[1], 'non verifie')])
    print('CSV exporté : ' + str(path))


def import_csv(path, apply=False):
    data = load()
    reference = {key: (original, french, target)
                 for key, original, french, target in entries(data)}
    seen = set()
    changed = set()
    with path.open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source, delimiter=';')
        if reader.fieldnames != COLUMNS:
            raise ValueError('Colonnes CSV différentes de l’export attendu.')
        for line, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'Ligne {line} : nombre de colonnes incorrect.')
            key = row['type'], row['id'], row['segment']
            if key not in reference or key in seen:
                raise ValueError(f'Ligne {line} : identifiant inconnu ou dupliqué : {key}')
            seen.add(key)
            original, old, target = reference[key]
            french = row['francais']
            if row['original'] != original:
                raise ValueError(f'Ligne {line} : texte original modifié.')
            encode_fr(french)
            encode_fr(french, False)
            if NATIVE.findall(french) != NATIVE.findall(original):
                raise ValueError(f'Ligne {line} : suffixes PSI modifiés.')
            if french != old:
                target['text_fr' if key[0] == 'field' else 'french'] = french
                changed.add(key[0])
    # Tout est validé avant la première écriture. L'import partiel est autorisé.
    if apply:
        for kind in FILES:
            if kind not in changed:
                continue
            destination = ROOT / 'traduction' / FILES[kind]
            fd, name = tempfile.mkstemp(dir=destination.parent, prefix='.import-')
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as output:
                    json.dump(data[kind], output, ensure_ascii=False, indent=2)
                    output.write('\n')
                os.replace(name, destination)
            finally:
                if os.path.exists(name):
                    os.unlink(name)
    print(f'{len(seen)} fragments validés ; ' +
          ('sources mises à jour.' if apply and changed else 'aucun fichier modifié.'))
    print('Les capacités réelles doivent ensuite être vérifiées avec construire.')


def build(rom, output, version):
    if not re.fullmatch(r'v[0-9]{2,4}', version):
        raise ValueError('Version invalide : utiliser v07, v08...')
    for profile in ('accents', 'ascii'):
        command = [sys.executable, str(ROOT / 'traduction/integrer.py'), str(rom),
                   '--sortie', str(output), '--version', version]
        if profile == 'ascii':
            command.append('--sans-accents')
        subprocess.run(command, check=True)
    subprocess.run([sys.executable, str(ROOT / 'traduction/verifier_integration.py'),
                    str(rom), '--build', str(output)], check=True)
    export_csv(output / 'traductions.csv', output / 'rapport_accents.json')
    audit(output / 'rapport_accents.json', output / 'audit.json')
    report = json.loads((output / 'rapport_accents.json').read_text(encoding='utf-8'))
    print(f"{report['accepted_count']} entrées intégrées ; "
          f"{report['rejected_count']} exclues. Consulter les rapports avant de tester en jeu.")


def audit(report_path, output):
    report = json.loads(report_path.read_text(encoding='utf-8'))
    expected = report.get('translation_sources_sha256')
    current = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted((ROOT / 'traduction').glob('*_fr.json'))}
    if expected != current:
        raise ValueError('Rapport absent ou périmé : reconstruire avant d’auditer les sources.')
    accepted = {row['id']: row for row in report['accepted']}
    pending = []
    for key, original, french, _ in entries(load()):
        if key[1] not in accepted:
            continue
        # Les noms propres et les marqueurs restent souvent identiques à juste titre.
        if french == original and any(c.isalpha() for c in french) and not NATIVE.fullmatch(french):
            pending.append({'type': key[0], 'id': key[1], 'segment': key[2],
                            'text': french, 'source_bytes': len(encode_fr(original)),
                            'french_bytes': len(encode_fr(french))})
    result = {'artifact_stem': report['artifact_stem'],
              'target_sha256': report['target_sha256'],
              'accepted_count': report['accepted_count'],
              'rejected': report['rejected'],
              'fragments_identiques_a_relire': pending,
              'scope': 'Champs et dialogues ordinaires préparés uniquement ; noms propres et glyphes à relire manuellement.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Audit : {len(report['rejected'])} entrées exclues ; {len(pending)} fragments identiques à relire.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('exporter'); p.add_argument('csv', type=Path)
    p.add_argument('--rapport', type=Path)
    p = sub.add_parser('importer'); p.add_argument('csv', type=Path)
    p.add_argument('--appliquer', action='store_true')
    p = sub.add_parser('auditer'); p.add_argument('rapport', type=Path)
    p.add_argument('--sortie', type=Path, required=True)
    p = sub.add_parser('construire'); p.add_argument('rom', type=Path)
    p.add_argument('--sortie', type=Path, default=ROOT / 'build')
    p.add_argument('--version', default='v08')
    args = parser.parse_args()
    try:
        if args.action == 'exporter': export_csv(args.csv, args.rapport)
        elif args.action == 'importer': import_csv(args.csv, args.appliquer)
        elif args.action == 'auditer': audit(args.rapport, args.sortie)
        else: build(args.rom, args.sortie, args.version)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, 'Échec : ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
