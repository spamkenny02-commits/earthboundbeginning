#!/usr/bin/env python3
"""Tests du brouillon v10 sans ROM ni modification des sources."""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from verifier_brouillon_v10 import audit


def main():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / 'draft.json'
        c = Path(tmp) / 'catalogue.json'
        rom = Path(tmp) / 'fake.sfc'
        base = {'id': '123456', 'english': '@Hello there.[13][02]',
                'francais_propose': '@Salut à toi.[13][02]'}
        catalogue = {'summary': {'artifact_stem': 'EarthBound_Beginnings_FR_v09'},
                     'entries': [{'id': '123456', 'category': 'script', 'status': 'a_examiner',
                                  'english': base['english'], 'incoming_literal_candidates': ['010000']}]}
        def write(row):
            d.write_text(json.dumps({'blocks': [row]}), encoding='utf-8')
        c.write_text(json.dumps(catalogue), encoding='utf-8')
        write(base)
        assert audit(d, c)['blocs_controles'] == 1
        for field, changed in [
            ('english', '@Goodbye.[13][02]'),
            ('francais_propose', '@Salut.[02]'),
            ('francais_propose', '@Salut.[13][02]@'),
            ('francais_propose', '@Salut ☺.[13][02]')]:
            bad = dict(base, **{field: changed})
            write(bad)
            try:
                audit(d, c)
            except ValueError:
                pass
            else:
                raise AssertionError('Brouillon invalide accepté : ' + field)
        write(base)
        rom.write_bytes(b'\0' * 0x8000)
        try:
            audit(d, c, rom)
        except ValueError as exc:
            assert 'SHA-256' in str(exc)
        else:
            raise AssertionError('ROM non reconnue acceptée')
    print('V10 : audit du brouillon et 5 refus vérifiés.')


if __name__ == '__main__':
    main()
