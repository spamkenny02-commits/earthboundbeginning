"""V28 autonomous IPS builder. Requires original USA 1.2 ROM, never ships it."""
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import ROM_SHA,SIZE,sha,encode,records,apply,append,pointer_index
BASE_SHA={'accents':'b48cbe0373f36408d545f8b0ad82e664725d0cf7877fb11c72668135593a27c6','ascii':'298d3bb4c54b6f1db62e835e952a095b99f69aec80296d92b022092dbbe9011a'}
FINAL_SHA={'accents':'3db0607030f931d5acb020fa7b9f9d6af8d157099bb958a887192edef005fbd9','ascii':'60a70dc688b491c5574d01e86856c3e06646545d46e1838183791ea6c50df7f5'}
def entries():
    data=json.loads((ROOT/'tools/v28/v28_dialogues_fr.json').read_text())
    if data['version']!='v28' or data['base']!='v27' or len(data['entries'])!=49:raise ValueError('Manifest invalid')
    return data['entries']
def audit(rom):
    if len(rom)!=SIZE or sha(rom)!=ROM_SHA:raise ValueError('Original USA 1.2 required')
    refs=pointer_index(rom);occupied=bytearray(SIZE);bases={}
    for profile in ('accents','ascii'):
        ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v27_{profile}.ips').read_bytes()
        if sha(ips)!=BASE_SHA[profile]:raise ValueError('V27 IPS hash mismatch')
        old=records(ips);base=apply(rom,old);bases[profile]=(ips,old,base)
        for p,b in old:occupied[p:p+len(b)]=b'\x01'*len(b)
    seen=set();spans=[]
    for e in entries():
        ident=e['id'];p=int(ident,16);n=e['text_length'];s=int(e['script_id'],16)
        if ident in seen or not (0<=s<p<p+n<=SIZE):raise ValueError('Duplicate or bounds: '+ident)
        seen.add(ident)
        if rom[s:p]!=bytes.fromhex(e['script_prefix_hex']):raise ValueError('Script commands/prefix: '+ident)
        if rom[p:p+n]!=bytes(ord(c)+48 for c in e['english']):raise ValueError('Original text: '+ident)
        declared=[int(x,16) for x in e['script_refs']]
        if not declared or not set(declared).issubset(refs.get(s,[])):raise ValueError('Script refs: '+ident)
        if any(q in refs for q in range(p,p+n)):raise ValueError('Interior pointer: '+ident)
        if any(occupied[p:p+n]):raise ValueError('V27 collision: '+ident)
        for q in declared:
            if any(base[q:q+4]!=rom[q:q+4] for _,_,base in bases.values()):
                raise ValueError('V27 modified entry ref: '+ident)
        if e['fr']==e['english']:raise ValueError('Unchanged: '+ident)
        for profile in ('accents','ascii'):
            if len(encode(e['fr'],profile))>n:raise ValueError('Too long: '+ident)
        spans.append((p,p+n))
    spans.sort()
    if any(b>c for (_,b),(c,_) in zip(spans,spans[1:])):raise ValueError('New overlap')
    return bases
def build(rom_path,out):
    rom=Path(rom_path).read_bytes();bases=audit(rom);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    results={}
    for profile,(prior,old,base) in bases.items():
        additions=[];allowed=bytearray(SIZE)
        for e in entries():
            p=int(e['id'],16);n=e['text_length'];payload=encode(e['fr'],profile).ljust(n,b'\x50')
            if payload==base[p:p+n]:raise ValueError('No change')
            additions.append((p,payload));allowed[p:p+n]=b'\x01'*n
        ips=append(prior,additions)
        if sha(ips)!=FINAL_SHA[profile] or records(ips)!=old+additions:raise ValueError('IPS mismatch')
        target=apply(rom,records(ips))
        if target!=apply(base,additions):raise ValueError('ROM roundtrip mismatch')
        if any(a!=b for a,b,m in zip(target,base,allowed) if not m):raise ValueError('Outside spans modified')
        if any(target[p:p+len(b)]!=base[p:p+len(b)] for p,b in old):raise ValueError('V27 regression')
        (out/f'EarthBound_Beginnings_FR_v28_{profile}.ips').write_bytes(ips)
        results[profile]={'sha256':sha(ips),'target_rom_sha256':sha(target),'rom_roundtrip':True}
    return results
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,default=ROOT/'build_v28')
    a=p.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
