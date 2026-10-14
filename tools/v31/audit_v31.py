"""Audit source-verified text spans inside explicitly referenced scripts."""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/v19'))
sys.path.insert(0, str(ROOT/'traduction'))
from build_v19 import ROM_SHA, SIZE, sha, records, apply, pointer_index
from layout_v31 import decode_layout

BASE_SHA = {
    'accents': 'dbaccd952adfe31db296c501c6933e65de38c8a2112c1764bc0998cad0dd9870',
    'ascii': '92c1d2e59cca515e69e956f706306f4f63a031ac3347806dfc36b0451b7cc3d8',
}

def commands_preserved(source, baseline, start, end, spans):
    mask = bytearray(end-start)
    for a,z in spans:
        mask[a-start:z-start] = b'\1'*(z-a)
    return all(x==y for x,y,m in zip(source[start:end],baseline[start:end],mask) if not m)

def audit(rom):
    if len(rom)!=SIZE or sha(rom)!=ROM_SHA:
        raise ValueError('ROM originale USA 1.2 requise')
    refs=pointer_index(rom)
    occupied=bytearray(SIZE)
    baselines={}
    for profile in ('accents','ascii'):
        ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v30_{profile}.ips').read_bytes()
        if sha(ips)!=BASE_SHA[profile]:
            raise ValueError('IPS V30 non conforme: '+profile)
        rec=records(ips)
        baselines[profile]=apply(rom,rec)
        for p,b in rec:
            occupied[p:p+len(b)]=b'\1'*len(b)
    candidates=[];seen=set();counts=Counter()
    for row in json.loads((ROOT/'catalogue/catalogue.json').read_text())['entries']:
        if row['category']!='script':
            continue
        start=int(row['id'],16)
        layout=decode_layout(rom,start,row['english'])
        if not layout:
            counts['layout_rejected']+=1;continue
        end,mask,spans=layout
        if not refs.get(start):
            counts['unreferenced_script']+=1;continue
        if any(b[q:q+4]!=rom[q:q+4] for b in baselines.values() for q in refs[start]):
            counts['changed_entry_pointer']+=1;continue
        if not all(commands_preserved(rom,b,start,end,spans) for b in baselines.values()):
            counts['changed_commands']+=1;continue
        for a,z in spans:
            if (a,z) in seen:
                continue
            seen.add((a,z))
            if any(occupied[a:z]):
                counts['occupied']+=1;continue
            if any(p in refs for p in range(a,z)):
                counts['interior_ref']+=1;continue
            english=''.join(chr(x-48) for x in rom[a:z])
            if len(english.strip())<3 or not any(c.isalpha() for c in english):
                counts['small']+=1;continue
            candidates.append({
                'id':f'{a:06X}','english':english,'text_length':z-a,
                'script_id':row['id'],'script_end':f'{end:06X}',
                'script_english':row['english'],
                'script_refs':[f'{q:06X}' for q in refs[start]],
                'prefix':rom[max(start,a-4):a].hex(),
                'suffix':rom[z:min(end,z+4)].hex(),
            })
    return candidates,baselines,occupied,dict(counts)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    candidates,_,_,counts=audit(args.rom.read_bytes())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps({'counts':counts,'candidates':candidates},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'candidates':len(candidates),'counts':counts},indent=2))
