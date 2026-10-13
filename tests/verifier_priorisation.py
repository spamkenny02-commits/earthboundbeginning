#!/usr/bin/env python3
"""Vérifie le classement, les doublons et la conservation des commandes sources."""
import csv
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from prioriser_candidats import produce


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / 'catalogue.json'
        data = {'summary': {'artifact_stem': 'EarthBound_Beginnings_FR_v09'}, 'entries': [
            {'id': '000001', 'category': 'script', 'status': 'a_examiner',
             'english': '@Who are you? Come with me now.[13][02]',
             'evidence': 'literal_pointer', 'incoming_literal_candidates': ['001000']},
            {'id': '000002', 'category': 'script', 'status': 'a_examiner',
             'english': 'Ej0@Go to her.[13][02]', 'evidence': 'sequential_or_inline',
             'incoming_literal_candidates': []},
            {'id': '000003', 'category': 'script', 'status': 'integre',
             'english': '@Already done', 'evidence': 'literal_pointer'},
            {'id': '000004', 'category': 'script', 'status': 'a_examiner',
             'english': '@Who are you? Come with me now.[13][02]',
             'evidence': 'literal_pointer', 'incoming_literal_candidates': ['002000']}
        ]}
        source.write_text(json.dumps(data), encoding='utf-8')
        csv_out, report = root / 'priorites.csv', root / 'rapport.json'
        summary = produce(source, csv_out, report)
        with csv_out.open(encoding='utf-8-sig', newline='') as inp:
            rows = list(csv.DictReader(inp, delimiter=';'))
        assert len(rows) == 3 and summary['total_a_examiner'] == 3
        assert rows[-1]['id'] == '000002' and 'prefixe_suspect' in rows[-1]['risques']
        assert '[13][02]' in rows[0]['anglais']
        assert 'doublon_texte' in rows[0]['risques']
        assert all(not row['traduction_proposee'] for row in rows)
        assert json.loads(report.read_text())['version_source'].endswith('v09')
        data['entries'].append(dict(data['entries'][0]))
        source.write_text(json.dumps(data), encoding='utf-8')
        try:
            produce(source, csv_out, report)
        except ValueError as exc:
            assert 'dupliqués' in str(exc)
        else:
            raise AssertionError('Identifiants dupliqués acceptés')
    print('Priorisation v09 : tests OK')


if __name__ == '__main__':
    main()
