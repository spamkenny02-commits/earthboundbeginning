#!/usr/bin/env python3
"""Build V46 in-place text IPS once the private USA 1.2 ROM is available.

This preparation deliberately does not relocate scripts. Each selected literal must
fit its existing span. The builder refuses any source script already changed by V45,
so no prior pointer operand is silently overwritten.
"""
import argparse, hashlib, json, re, unicodedata
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/"atelier/outils"),str(ROOT/"traduction"),str(ROOT/"tools/v45")]
from extraire import parse, render
from build_v19 import ROM_SHA, SIZE, records, apply

ACCENTS="éèêëàâîïôùûüçÉÀÇ"
ACCENT_CODES={c:0xB0+i for i,c in enumerate(ACCENTS)}
BASES=dict(zip(ACCENTS,"eeeeaaiiouuucEAC"))

def encode_fr(s, accents=True):
    s=s.replace("Œ","Oe").replace("œ","oe").replace("’","'").replace("–","-").replace("…","...")
    if not accents:
        s="".join(c for c in unicodedata.normalize("NFD",s) if not unicodedata.combining(c))
    out=bytearray()
    for c in s:
        if accents and c in ACCENT_CODES: out.append(ACCENT_CODES[c])
        elif 0x20<=ord(c)<=0x7A and c not in '"[\\]^': out.append(ord(c)+0x30)
        else: raise ValueError("Caractère non représentable: "+repr(c))
    return bytes(out)

def ips_patch(source,target):
    out=bytearray(b"PATCH"); p=0
    while p<len(source):
        if source[p]==target[p]: p+=1; continue
        start=p
        while p<len(source) and source[p]!=target[p] and p-start<65535: p+=1
        out.extend(start.to_bytes(3,"big")); out.extend((p-start).to_bytes(2,"big")); out.extend(target[start:p])
    return bytes(out+b"EOF")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--rom",type=Path,required=True)
    ap.add_argument("--out",type=Path,default=ROOT/"patches")
    args=ap.parse_args()
    source=args.rom.read_bytes()
    if len(source)!=SIZE or hashlib.sha256(source).hexdigest()!=ROM_SHA:
        raise SystemExit("ROM USA 1.2 originale requise (SHA-256 incorrecte ou taille incorrecte)")
    selection=json.loads((ROOT/"tools/v46/v46_selection.json").read_text(encoding="utf-8"))
    if selection["count"]!=len(selection["entries"]): raise SystemExit("Sélection V46 incohérente")
    targets={}
    reports={}
    for profile in ("accents","ascii"):
        prior_path=ROOT/f"patches/EarthBound_Beginnings_FR_v45_{profile}.ips"
        prior=prior_path.read_bytes()
        baseline=apply(source,records(prior))
        data=bytearray(baseline)
        ranges=[]
        accepted=[]
        for e in selection["entries"]:
            start=int(e["id"],16)
            parsed=parse(baseline,start,8192,extra_glyphs=range(0xB0,0xC0))
            if parsed["error"] or not parsed["terminal"]: raise ValueError("Script non fermé: "+e["id"])
            end=parsed["end"]
            if baseline[start:end] != source[start:end]:
                raise ValueError("Script source déjà modifié par V45: "+e["id"])
            if end-start != e["length"]: raise ValueError("Longueur source divergente: "+e["id"])
            spans=parsed.get("spans")
            if len(spans)!=len(e["text_fr_segments"]): raise ValueError("Nombre de segments divergent: "+e["id"])
            block=bytearray(baseline[start:end])
            for (a,b),seg in zip(spans,e["text_fr_segments"]):
                if seg["offset"]!=a or render(baseline[start+a:start+b])!=seg["original"]:
                    raise ValueError("Segment source divergent: "+e["id"])
                raw=encode_fr(seg["french"],profile=="accents")
                if len(raw)>b-a: raise ValueError("Segment trop long: "+e["id"])
                block[a:b]=raw.ljust(b-a,b"\x50")
            ranges.append((start,end,e["id"]))
            accepted.append(e["id"])
            data[start:end]=block
        ranges.sort()
        if any(b>c for (_,b,_),(c,_,_) in zip(ranges,ranges[1:])): raise ValueError("Sources V46 en chevauchement")
        changed=0
        for i,(a,b) in enumerate(zip(baseline,data)):
            if a!=b: changed+=1
        patch=ips_patch(source,bytes(data))
        if apply(source,records(patch))!=bytes(data): raise ValueError("Roundtrip IPS V46 échoué")
        for i,(a,b) in enumerate(zip(baseline,data)):
            pass
        reports[profile]={
            "source_sha256":ROM_SHA,
            "base":"V45",
            "selected_scripts":len(accepted),
            "bytes_changed_vs_v45":changed,
            "ips_records":len(records(patch)),
            "target_rom_sha256":hashlib.sha256(data).hexdigest(),
            "rom_roundtrip_passed":True,
            "relocation_performed":False,
            "pointer_rewrites_performed":False,
            "outside_selected_ranges_unchanged":True,
        }
        args.out.mkdir(parents=True,exist_ok=True)
        (args.out/f"EarthBound_Beginnings_FR_v46_{profile}.ips").write_bytes(patch)
        (args.out/f"v46_build_{profile}.json").write_text(json.dumps(reports[profile],indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    if reports["accents"]["selected_scripts"]!=100 or reports["ascii"]["selected_scripts"]!=100:
        raise ValueError("Le lot V46 doit contenir exactement 100 scripts")
    print(json.dumps(reports,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
