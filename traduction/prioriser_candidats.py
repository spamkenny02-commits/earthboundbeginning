#!/usr/bin/env python3
"""Classe les blocs non intégrés pour relecture humaine, sans présumer de leur usage.

Entrée : catalogue/catalogue.json généré par `atelier.py cataloguer`.
Sorties : CSV UTF-8 BOM pour tableur + rapport JSON. Aucun fichier source modifié.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

CONTROL = re.compile(r'\[[0-9A-Fa-f ]+\]')
WORD = re.compile(r"[A-Za-z][A-Za-z']+")
FIELDS = ['priorite', 'score_indicatif', 'id', 'anglais', 'texte_lisible',
          'preuve', 'pointeurs_litteraux', 'risques', 'statut_relecture', 'traduction_proposee']


def readable(raw):
    return CONTROL.sub('', raw).replace('@', ' ').strip()


def rank(row, duplicates):
    original = row.get('english', '')
    clean = readable(original)
    evidence = str(row.get('evidence', ''))
    pointers = row.get('incoming_literal_candidates') or []
    tokens = WORD.findall(clean)
    score = 0
    risks = []
    if 'literal_pointer' in evidence:
        score += 50
    elif 'sequential' in evidence or 'inline' in evidence:
        score += 10
        risks.append('frontiere_a_verifier')
    else:
        risks.append('preuve_insuffisante')
    if pointers:
        score += min(len(pointers), 5) * 8
    else:
        risks.append('aucun_pointeur_litteral')
    if len(tokens) >= 6:
        score += 15
    elif len(tokens) >= 3:
        score += 8
    else:
        risks.append('texte_court')
    if original.count('@') >= 2:
        score += 6
    if duplicates[clean] > 1 and clean:
        score -= 12
        risks.append('doublon_texte')
    if not clean or len(tokens) < 2:
        score -= 25
    if re.match(r'^[A-Za-z0-9]{2,4}@', original):
        score -= 25
        risks.append('prefixe_suspect')
    if '\ufffd' in original or '\x00' in original:
        score -= 30
        risks.append('encodage_suspect')
    priority = 'haute' if score >= 65 else 'moyenne' if score >= 35 else 'basse'
    return {'priorite': priority, 'score_indicatif': score, 'id': row['id'],
            'anglais': original, 'texte_lisible': clean, 'preuve': evidence,
            'pointeurs_litteraux': ','.join(map(str, pointers)),
            'risques': ','.join(risks), 'statut_relecture': 'a_verifier',
            'traduction_proposee': ''}


def produce(source, csv_path, report_path):
    data = json.loads(source.read_text(encoding='utf-8-sig'))
    if not isinstance(data.get('entries'), list):
        raise ValueError('Catalogue invalide : entries manquant.')
    candidates = [row for row in data['entries']
                  if row.get('category') == 'script' and row.get('status') == 'a_examiner']
    ids = [r['id'] for r in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError('Identifiants de candidats dupliqués.')
    duplicates = Counter(readable(r.get('english', '')) for r in candidates)
    ranked = [rank(r, duplicates) for r in candidates]
    order = {'haute': 0, 'moyenne': 1, 'basse': 2}
    ranked.sort(key=lambda r: (order[r['priorite']], -r['score_indicatif'], r['id']))
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open('w', encoding='utf-8-sig', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=FIELDS, delimiter=';')
        writer.writeheader()
        writer.writerows(ranked)
    summary = {'catalogue': str(source), 'version_source': data.get('summary', {}).get('artifact_stem'),
               'total_a_examiner': len(ranked), 'priorites': dict(Counter(r['priorite'] for r in ranked)),
               'avertissement': 'Score heuristique, non une preuve de présence en jeu. Vérifier frontières, pointeurs, commandes et rendu avant intégration.'}
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('catalogue', type=Path)
    p.add_argument('--csv', type=Path, required=True)
    p.add_argument('--rapport', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(produce(a.catalogue, a.csv, a.rapport), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
