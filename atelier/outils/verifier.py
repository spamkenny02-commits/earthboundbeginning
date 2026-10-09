#!/usr/bin/env python3
"""Audit indépendant des plages sauvegardées et des phrases lisibles dans la zone du remake."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from extraire import encode, render, EXPECTED, ROOT

FILES=['dialogues.json','champs_menus_objets_ennemis.json',
       'dictionnaire_compression.json','textes_banques_origine.json',
       'textes_defilants.json','textes_integres_autre_bytecode.json']

def audit(rom, output):
    data=rom.read_bytes()
    if len(data)%0x8000==512:data=data[512:]
    assert hashlib.sha256(data).hexdigest()==EXPECTED,'ROM différente'
    intervals=[]
    counts={}
    for filename in FILES:
        rows=json.loads((output/filename).read_text())
        counts[filename]=len(rows)
        for row in rows:
            p=int(row['offset'],16)
            raw=bytes.fromhex(row['raw_hex'])
            assert len(raw)==row['length'],(filename,row['id'],'taille')
            assert data[p:p+len(raw)]==raw,(filename,row['id'],'octets')
            assert encode(row['text_en'])==raw,(filename,row['id'],'encodage')
            intervals.append((p,p+len(raw)))
    merged=[]
    for p,q in sorted(intervals):
        if merged and p<=merged[-1][1]:merged[-1]=(merged[-1][0],max(q,merged[-1][1]))
        else:merged.append((p,q))
    def covered(p,q):return any(a<=p and q<=z for a,z in merged)
    missing=[]
    prose_count=0
    # Independent from extractor's candidate seeds and stored coverage booleans.
    for m in re.finditer(rb'[\x50-\xae]{4,}',data[0x339A82:0x3A0000]):
        text=render(m[0])
        if ' ' in text and len(re.findall('[a-z]',text))>=12:
            p=m.start()+0x339A82;q=m.end()+0x339A82
            prose_count+=1
            if not covered(p,q):missing.append(dict(offset=f'{p:06X}',text=text))
    # Regression checks for known omissions from v01, including late ROM text and callbacks.
    probes=["And don't let the bed bugs bite.","I had loved him as if he were my own child, too...",
            'you music-loving adventurer!',"Mimmie doesn't work here any more.",
            'In the early 1900s, a dark shadow','80 years have passed since then...',
            "Listen to what I've got to say!",'Enemies enabled.',"(EVE can't fit through.)",
            'PK Fire ','PK Freeze ','Mary','Giygas']
    probe_results=[]
    for text in probes:
        raw=bytes(ord(c)+48 for c in text)
        locations=[m.start() for m in re.finditer(re.escape(raw),data)]
        found=[p for p in locations if covered(p,p+len(raw))]
        assert found,('Passage absent des exports',text)
        probe_results.append(dict(text=text,covered_offsets=[f'{p:06X}' for p in found]))
    # Callback parameters are kept in the same token, so they cannot become bogus script commands.
    combined='\n'.join(r['text_en'] for r in json.loads((output/'dialogues.json').read_text()))
    assert '[1A 0C 34 AA F8 00 1D 03]' in combined,'Paramètres de palette perdus'
    assert '[1A 0C E5 95 F8 00 01]' in combined,'Paramètre de cinématique perdu'
    assert not missing,missing
    result=dict(status='passed',rom_unchanged_sha256=hashlib.sha256(data).hexdigest(),
                byte_and_encoding_records_checked=sum(counts.values()),record_counts=counts,
                long_prose_fragments_checked_in_remake=prose_count,
                long_prose_fragments_missing_from_exports=len(missing),
                regression_probes=probe_results,
                all_rom_text_proven=False,
                limits='Audit limité aux encodages reconnus et aux plages analysées ; pas de preuve de couverture des textes graphiques ou de tous les chemins en jeu.')
    (output/'audit_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('regression_probes','record_counts')},ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('rom',type=Path)
    p.add_argument('--sortie',type=Path,default=ROOT/'extraction')
    args=p.parse_args()
    audit(args.rom,args.sortie)
