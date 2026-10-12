#!/usr/bin/env python3
"""Refus d'import dangereux et aller-retour CSV sans modifier les sources."""
import copy
import csv
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
import atelier


def main():
    before = {name: hashlib.sha256((ROOT / 'traduction' / name).read_bytes()).hexdigest()
              for name in atelier.FILES.values()}
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / 'traductions.csv'
        atelier.export_csv(path)
        atelier.import_csv(path, apply=True)
        with path.open(encoding='utf-8-sig', newline='') as source:
            rows = list(csv.DictReader(source, delimiter=';'))

        def write(data):
            with path.open('w', encoding='utf-8-sig', newline='') as output:
                writer = csv.DictWriter(output, fieldnames=atelier.COLUMNS, delimiter=';')
                writer.writeheader(); writer.writerows(data)

        def refused(data):
            write(data)
            try:
                atelier.import_csv(path, apply=True)
            except ValueError:
                return
            raise AssertionError('Import invalide accepté')

        # Une modification valable au début ne doit pas être écrite si la suite échoue.
        for column, value in [('original', 'faux original'), ('id', 'FFFFFF'),
                              ('segment', '999999'), ('francais', '[1F 02 74]')]:
            changed = copy.deepcopy(rows)
            changed[0]['francais'] = 'Essai'
            changed[-1][column] = value
            refused(changed)
        refused([*rows, rows[0]])
        changed = copy.deepcopy(rows)
        psi = next(row for row in changed if atelier.NATIVE.search(row['original']))
        psi['francais'] = atelier.NATIVE.sub('', psi['francais'])
        refused(changed)

        # Un import partiel valide met à jour seulement le texte français.
        changed = [copy.deepcopy(rows[0])]
        changed[0]['francais'] = 'Essai'
        write(changed)
        sample = atelier.load()
        with patch.object(atelier, 'load', return_value=sample):
            atelier.import_csv(path)
        first = next(atelier.entries(sample))
        assert first[2] == 'Essai' and first[1] == rows[0]['original']

        # Un audit ancien ne doit pas donner un statut fiable à des sources modifiées.
        report_path = Path(folder) / 'rapport.json'
        output = Path(folder) / 'audit.json'
        report = {'artifact_stem': 'essai', 'target_sha256': 'essai',
                  'accepted_count': 1, 'accepted': [{'id': 'FFFFFF'}], 'rejected': [],
                  'translation_sources_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in sorted((ROOT / 'traduction').glob('*_fr.json'))}}
        report_path.write_text(json.dumps(report), encoding='utf-8')
        audit_fixture = {'field': [{'id': 'FFFFFF', 'text_en': 'No', 'text_fr': 'No'}],
                         'dialogue': []}
        with patch.object(atelier, 'load', return_value=audit_fixture):
            atelier.audit(report_path, output)
        found = json.loads(output.read_text())['fragments_identiques_a_relire']
        assert any(row['text'] == 'No' and row['id'] == 'FFFFFF' for row in found)
        report['translation_sources_sha256']['dialogues_fr.json'] = 'perime'
        report_path.write_text(json.dumps(report), encoding='utf-8')
        output.unlink()
        try:
            atelier.audit(report_path, output)
        except ValueError:
            pass
        else:
            raise AssertionError('Audit périmé accepté')
        assert not output.exists()

        # Écriture réelle dans une copie isolée : sauvegarde et plan de déplacement conservés.
        isolated=Path(folder)/'projet';(isolated/'traduction').mkdir(parents=True)
        for name in atelier.FILES.values():
            shutil.copy2(ROOT/'traduction'/name,isolated/'traduction'/name)
        moved=next(row for row in rows if row['type']=='relocated')
        moved=copy.deepcopy(moved);moved['francais']='@Essai'
        write([moved])
        original_plan=json.loads((isolated/'traduction/textes_relocalises_fr.json').read_text())
        with patch.object(atelier,'ROOT',isolated):
            atelier.import_csv(path,apply=True)
        modified_plan=json.loads((isolated/'traduction/textes_relocalises_fr.json').read_text())
        for key in original_plan:
            if key!='blocks':assert original_plan[key]==modified_plan[key]
        saved=list((isolated/'sauvegardes_import').glob('*/textes_relocalises_fr.json'))
        assert len(saved)==1 and json.loads(saved[0].read_text())==original_plan
    after = {name: hashlib.sha256((ROOT / 'traduction' / name).read_bytes()).hexdigest()
             for name in atelier.FILES.values()}
    assert before == after, 'Sources modifiées pendant les refus ou l’aller-retour'
    print('Atelier : import CSV, 6 refus, audit des fragments et refus de rapport périmé OK.')


if __name__ == '__main__':
    main()
