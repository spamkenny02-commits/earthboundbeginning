"""Build V25 autonomous IPS from individually audited text spans."""
import argparse
import json
from pathlib import Path
from audit_v25 import ROOT, audit, commands_preserved
from build_v19 import encode, read_translations, records, apply, append, sha

def rendered(french,english):
    # Preserve indentation and separation around dynamic commands.
    leading=english[:len(english)-len(english.lstrip(' '))]
    trailing=english[len(english.rstrip(' ')):]
    return leading+french+trailing

def build(rom_path,out,translations_path=None):
    rom=Path(rom_path).read_bytes()
    candidates,baselines,occupied,counts=audit(rom)
    catalog={e['id']:e for e in candidates}
    translations=read_translations(translations_path or ROOT/'tools/v25/translations_v25.tsv')
    entries=[]
    for ident,french in translations.items():
        if ident not in catalog:
            raise ValueError('Plage non auditée: '+ident)
        e=catalog[ident]
        text=rendered(french,e['english'])
        if text.strip()==e['english'].strip():
            raise ValueError('Texte inchangé: '+ident)
        entries.append({**e,'fr':french,'rendered_fr':text})
    spans=sorted((int(e['id'],16),int(e['id'],16)+e['text_length']) for e in entries)
    if any(b>c for (a,b),(c,d) in zip(spans,spans[1:])):
        raise ValueError('Plages V25 en chevauchement')
    results={};out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for profile in ('accents','ascii'):
        prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v24_{profile}.ips').read_bytes()
        baseline=baselines[profile];old=records(prior)
        additions=[];changed=bytearray(len(rom))
        for e in entries:
            p=int(e['id'],16);n=e['text_length']
            if any(occupied[p:p+n]) or any(changed[p:p+n]):
                raise ValueError('Collision: '+e['id'])
            payload=encode(e['rendered_fr'],profile)
            if len(payload)>n:
                raise ValueError(f"Longueur {e['id']}: {len(payload)}>{n}")
            padded=payload.ljust(n,b'\x50')
            if padded==baseline[p:p+n]:
                raise ValueError('Modification nulle: '+e['id'])
            additions.append((p,padded));changed[p:p+n]=b'\1'*n
        ips=append(prior,additions)
        target=apply(rom,records(ips))
        if target!=apply(baseline,additions) or records(ips)!=old+additions:
            raise ValueError('Aller-retour IPS divergent')
        if any(a!=b for a,b,m in zip(target,baseline,changed) if not m):
            raise ValueError('Modification hors plages V25')
        if any(target[p:p+len(b)]!=baseline[p:p+len(b)] for p,b in old):
            raise ValueError('Régression V24')
        (out/f'EarthBound_Beginnings_FR_v25_{profile}.ips').write_bytes(ips)
        results[profile]={
            'v24_records':len(old),'v25_additions':len(additions),
            'sha256':sha(ips),'target_rom_sha256':sha(target),
            'rom_roundtrip':True,'no_prior_regression':True,'outside_additions_unchanged':True,
        }
    report={'source_rom_sha256':sha(rom),'base':'v24','audited_candidates':len(candidates),
            'audit_counts':counts,'new_segments':len(entries),'profiles':results}
    (ROOT/'tools/v25/v25_dialogues_fr.json').write_text(json.dumps({'version':'v25','entries':entries},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'tools/v25/validation_v25.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--out',type=Path,default=ROOT/'build_v25')
    ap.add_argument('--translations',type=Path);a=ap.parse_args()
    print(json.dumps(build(a.rom,a.out,a.translations),indent=2))
