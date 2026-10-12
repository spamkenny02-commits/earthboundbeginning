#!/usr/bin/env python3
"""Catalogue des exports candidats, sans inventer un pourcentage de traduction."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def catalogue(report_path, output):
    report=json.loads(report_path.read_text(encoding='utf-8'))
    current={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted((ROOT/'traduction').glob('*_fr.json'))}
    if current!=report.get('translation_sources_sha256'):
        raise ValueError('Rapport périmé : reconstruire avant de mesurer la couverture.')
    original=ROOT/'atelier/extraction'
    scripts=json.loads((original/'dialogues.json').read_text(encoding='utf-8'))
    fields=json.loads((original/'champs_menus_objets_ennemis.json').read_text(encoding='utf-8'))
    supplement=json.loads((ROOT/'traduction/sources_complementaires.json').read_text(encoding='utf-8'))
    by_id={r['id']:dict(r) for r in scripts}
    # Une entrée vérifiée de quête commence après le faux candidat de l'extracteur.
    replaced=by_id.pop('3601F7',None)
    for row in supplement['blocks']:
        if row['id']=='3601FC':by_id[row['id']]=dict(row)
    accepted={r['id']:r for r in report['accepted']}
    rejected={r['id']:r for r in report['rejected']}
    prepared={r['id'] for r in json.loads((ROOT/'traduction/dialogues_fr.json').read_text(encoding='utf-8'))}
    prepared|={r['id'] for r in json.loads((ROOT/'traduction/textes_relocalises_fr.json').read_text(encoding='utf-8'))['blocks']}
    prepared|={r['id'] for r in json.loads((ROOT/'traduction/menus_objets_fr.json').read_text(encoding='utf-8'))}
    rows=[]
    for family,source in [('script',sorted(by_id.values(),key=lambda r:r['offset'])),('field',fields)]:
        for row in source:
            id=row['id']
            status='integre' if id in accepted else 'exclu' if id in rejected else 'prepare' if id in prepared else 'a_examiner'
            rows.append({'id':id,'category':family,'status':status,
                         'english':row.get('reading_en',row['text_en']),
                         'evidence':row.get('evidence',row['source']),
                         'incoming_literal_candidates':row.get('literal_pointer_offsets',[]),
                         'note':rejected.get(id,{}).get('reason','')})
    summary={'artifact_stem':report['artifact_stem'],'integrated_entries_all_sources':report['accepted_count'],
             'export_counts':{family:dict(Counter(r['status'] for r in rows if r['category']==family)) for family in ['script','field']},
             'candidate_blocks_replaced':[{'old_id':'3601F7','verified_id':'3601FC'}] if replaced else [],
             'scope':'Catalogue des exports candidats. Les noms conservés et les fragments anglais internes ne sont pas un taux de traduction. Textes hérités, graphismes, générique et frontières de script restent à valider.'}
    output.mkdir(parents=True,exist_ok=True)
    (output/'couverture.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (output/'catalogue.json').write_text(json.dumps({'summary':summary,'entries':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (output/'textes_a_examiner.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['id','category','status','english','evidence','note'],delimiter=';',extrasaction='ignore')
        writer.writeheader();writer.writerows(r for r in rows if r['status']!='integre')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rapport',type=Path);parser.add_argument('--sortie',type=Path,required=True)
    args=parser.parse_args();catalogue(args.rapport,args.sortie)
