#!/usr/bin/env python3
"""Build autonomous V20 IPS profiles on top of validated local V19.

Only an original user-supplied ROM is accepted; it is never included in output.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/v19'))
from build_v19 import (ROM_SHA, SIZE, encode, read_translations, pointer_index,
                       records, apply, append, sha)

V19_SHA = {
    'accents':'6a1794d1ea8f0fca7ef73f6e244e54de92ca4ae3207b81d29d3fc83374f38c18',
    'ascii':'9b9edf7a1af355881dc6396553d0bb2916813717d33f71a470ac98c7a912c403',
}

def get_candidates():
    return {x['id']:x for x in json.loads((ROOT/'tools/v18_work/sources/v18_work_candidates.json').read_text(encoding='utf-8'))}

def validate_and_build(rom_path, output_dir, translations_path=None):
    rom=Path(rom_path).read_bytes()
    if len(rom)!=SIZE or sha(rom)!=ROM_SHA:
        raise ValueError('ROM originale USA 1.2 requise (taille et SHA-256)')
    translations=read_translations(Path(translations_path) if translations_path else ROOT/'tools/v20/translations_v20.tsv')
    candidates=get_candidates()
    already={x['id'] for x in json.loads((ROOT/'tools/v18_work/v18_work_dialogues_fr.json').read_text())['entries']}
    already.update(x['id'] for x in json.loads((ROOT/'tools/v19/v19_dialogues_fr.json').read_text())['entries'])
    if set(translations)&already:
        raise ValueError('Déjà traduit dans V18 Work ou V19')
    refs=pointer_index(rom)
    results={}
    for profile in ('accents','ascii'):
        ips19=(ROOT/f'patches/EarthBound_Beginnings_FR_v19_{profile}.ips').read_bytes()
        if sha(ips19)!=V19_SHA[profile]:
            raise ValueError('IPS V19 non conforme: '+profile)
        old=records(ips19)
        baseline=apply(rom,old)
        occupied=bytearray(SIZE)
        for p,payload in old:
            if any(occupied[p:p+len(payload)]):
                # Some historical records intentionally overlap; do not change them.
                pass
            occupied[p:p+len(payload)]=b'\x01'*len(payload)
        changed=bytearray(SIZE)
        additions=[]
        for ident,french in translations.items():
            if ident not in candidates:
                raise ValueError('Identifiant hors catalogue: '+ident)
            e=candidates[ident]
            p=int(ident,16); n=e['text_length'];end=p+1+n
            if not (0<=p<end+2<=SIZE):
                raise ValueError('Débordement ROM: '+ident)
            if any(occupied[p:end]) or any(changed[p:end]):
                raise ValueError('Collision V19 ou V20: '+ident)
            if rom[p]!=0x70 or rom[p+1:end]!=bytes(ord(c)+48 for c in e['english']):
                raise ValueError('Texte anglais original différent: '+ident)
            if rom[end:end+2].hex()!=e['suffix']:
                raise ValueError('Commande de fin différente: '+ident)
            if p not in refs and rom[p-2:p] not in (b'\x03\x00',b'\x13\x02'):
                raise ValueError('Frontière de segment incertaine: '+ident)
            if [f'{q:06X}' for q in refs.get(p,[])]!=e['refs']:
                raise ValueError('Références HiROM différentes: '+ident)
            if any(baseline[q:q+4]!=rom[q:q+4] for q in refs.get(p,[])):
                raise ValueError('Pointeur altéré dans V19: '+ident)
            if any(q in refs for q in range(p+1,end)):
                raise ValueError('Pointeur littéral intérieur: '+ident)
            if french==e['english']:
                raise ValueError('Segment inchangé: '+ident)
            payload=encode(french,profile)
            if len(payload)>n:
                raise ValueError(f'Dépassement de longueur: {ident} ({len(payload)}>{n})')
            padded=payload.ljust(n,b'\x50')
            if baseline[p+1:end]==padded:
                raise ValueError('Segment déjà identique en V19: '+ident)
            additions.append((p+1,padded))
            changed[p+1:end]=b'\x01'*n
        ips20=append(ips19,additions)
        if records(ips20)!=old+additions or ips20[:len(ips19)-3]!=ips19[:-3]:
            raise ValueError('Erreur de structure IPS ou régression des enregistrements V19')
        result=apply(rom,records(ips20))
        expected=apply(baseline,additions)
        if result!=expected:
            raise ValueError('Roundtrip IPS divergent: '+profile)
        if any(result[p:p+len(payload)]!=baseline[p:p+len(payload)] for p,payload in old):
            raise ValueError('Régression des enregistrements V19: '+profile)
        if any(a!=b for a,b,m in zip(result,baseline,changed) if not m):
            raise ValueError('Modification hors segments V20: '+profile)
        if any(result[p:p+len(payload)]!=payload for p,payload in additions):
            raise ValueError('Lecture de texte V20 divergente: '+profile)
        results[profile]={'v19_records':len(old),'v20_additions':len(additions),
                          'v20_records':len(records(ips20)), 'sha256':sha(ips20),
                          'target_rom_sha256':sha(result),'rom_roundtrip':True,
                          'no_prior_regression':True,'outside_additions_unchanged':True}
        output_dir.mkdir(parents=True,exist_ok=True)
        (output_dir/f'EarthBound_Beginnings_FR_v20_{profile}.ips').write_bytes(ips20)
    manifest={'version':'v20','base':'v19_local','entries':[
        {**candidates[ident],'fr':french} for ident,french in translations.items()]}
    (ROOT/'tools/v20/v20_dialogues_fr.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'source_rom_sha256':sha(rom),'base':'v19_local','new_segments':len(translations),
            'profiles':results}
    (ROOT/'tools/v20/validation_v20.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--rom',required=True,type=Path)
    ap.add_argument('--out',type=Path,default=ROOT/'build_v20')
    ap.add_argument('--translations',type=Path)
    args=ap.parse_args()
    print(json.dumps(validate_and_build(args.rom,args.out,args.translations),indent=2))
