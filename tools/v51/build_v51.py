"""Translate guarded spans with two tail jumps, preserving every interior entry.

The five-byte entry jump runs a private French text copy, whose final jump
resumes at the original next command. No return-stack frame is introduced.
Literal pointer occurrences are conservative guards, never rewritten here.
"""
import argparse,bisect,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v50'))
from build_v50 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,parse,encode,dictionary_from_rom,decode,spans_fr,pointer

def fixtures_from_baselines(source,bases,priors):
    if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
    targets=sorted(set(pointer_index(source))|set().union(*(set(pointer_index(d)) for d in bases.values())))
    mask=bytearray(SIZE)
    for ips in priors.values():
        for a,raw in records(ips):mask[a:a+len(raw)]=b'\1'*len(raw)
    for t in targets:mask[t]=1
    reserves=[]
    for lo,hi in ((0x250000,0x260000),(0x320000,0x330000)):
        safe=bytes(not mask[i] and source[i]==0 and all(d[i]==0 for d in bases.values()) for i in range(lo,hi))
        for m in re.finditer(b'\1{32,}',safe):
            a,z=(lo+m.start()+15)&~15,(lo+m.end())&~15
            if z-a>=16:reserves.append([a,z])
    reserves.sort(key=lambda r:r[1]-r[0],reverse=True)
    free=[r[:] for r in reserves];edits=[];deferred=[];contexts={};dictionary=dictionary_from_rom(source)
    candidates=json.loads((ROOT/'tools/v51/candidates_v51.json').read_text())['entries']
    for c in candidates:
        a,z=int(c['offset'],16),int(c['end'],16);root=int(c['context'],16)
        if any(d[a:z]!=source[a:z] for d in bases.values()) or decode(source[a:z],dictionary)!=c['english']:raise ValueError('Source divergente')
        context={}
        for p,data in bases.items():
            parsed=parse(data,root,8192,extra_glyphs=range(0xB0,0xC0))
            raw=data[root:parsed['end']]
            if parsed['error'] or not parsed['terminal'] or (a-root,z-root) not in spans_fr(raw):raise ValueError('Frontière de texte invalide')
            context[p]={'end':f"{parsed['end']:06X}",'baseline_hex':raw.hex()}
        i=bisect.bisect_right(targets,a);inside=targets[i] if i<len(targets) and targets[i]<z else None
        e={k:c[k] for k in ('offset','end','context','english','fr')}
        e['source_hex']=source[a:z].hex();e['interior_targets']=[f'{t:06X}' for t in targets[i:bisect.bisect_left(targets,z)]]
        if z-a<5 or inside is not None and inside<a+5:
            deferred.append(e);continue
        contexts[c['context']]=context;edits.append(e)
    # Largest copies first; both profiles use the same deterministic allocation.
    for e in sorted(edits,key=lambda e:(-max(len(encode(e['fr'],p)) for p in bases),e['offset'])):
        size=max(len(encode(e['fr'],p)) for p in bases)+5
        for r in free:
            if r[1]-r[0]>=size:
                e['copy_offset']=f'{r[0]:06X}';e['capacity']=size;r[0]=(r[0]+size+3)&~3;break
        else:raise ValueError('Réserve épuisée')
    return {'version':'v51','base':'v50','edits':edits,'deferred':deferred,'contexts':contexts,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves]}

def additions_from_fixtures(f,profile):
    changes=[]
    for e in f['edits']:
        a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
        if len(bytes.fromhex(e['source_hex']))!=z-a or z-a<5:raise ValueError('Capacité source invalide')
        if any(a<int(t,16)<a+5 for t in e['interior_targets']):raise ValueError('Entrée intérieure écrasée')
        text=encode(e['fr'],profile)
        if len(text)+5>e['capacity']:raise ValueError('Traduction trop longue')
        if not any(int(lo,16)<=d and d+e['capacity']<=int(hi,16) for lo,hi in f['reserves']):raise ValueError('Copie hors réserve')
        changes.extend(((a,b'\x0a'+pointer(d)),(d,text+b'\x0a'+pointer(z))))
    ranges=sorted((a,a+len(v)) for a,v in changes)
    if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Écritures en chevauchement')
    return changes

def logical_context(target,f,root,profile):
    """Follow only declared entry/copy/return jumps, preserving all other bytes.

    This is a static linear-context check, not simulation of event branches.
    """
    a=int(root,16);z=int(f['contexts'][root][profile]['end'],16);cursor=a;out=bytearray()
    for e in sorted(f['edits'],key=lambda e:int(e['offset'],16)):
        p,q=int(e['offset'],16),int(e['end'],16)
        if not a<=p<z:continue
        d=int(e['copy_offset'],16);text=encode(e['fr'],profile)
        if target[p:p+5]!=b'\x0a'+pointer(d) or target[d:d+len(text)+5]!=text+b'\x0a'+pointer(q):raise ValueError('Trajet de saut invalide')
        if target[p+5:q]!=bytes.fromhex(e['source_hex'])[5:]:raise ValueError('Entrée intérieure modifiée')
        out.extend(target[cursor:p]);out.extend(text);cursor=q
    out.extend(target[cursor:z]);return bytes(out)

def commands(raw):
    spans=spans_fr(raw);out=bytearray();cursor=0
    for a,z in spans:out.extend(raw[cursor:a]);cursor=z
    out.extend(raw[cursor:]);return bytes(out)

def build(rom,out):
    source=Path(rom).read_bytes();oldplan=json.loads((ROOT/'tools/v50/validation_v50.json').read_text())
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v50_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=oldplan['profiles'][p]['sha256'] for p,v in priors.items()):raise ValueError('IPS V50 divergent')
    bases={p:apply(source,records(v)) for p,v in priors.items()};f=fixtures_from_baselines(source,bases,priors)
    out=Path(out);out.mkdir(parents=True,exist_ok=True);profiles={}
    for p,base in bases.items():
        changes=additions_from_fixtures(f,p);ips=append(priors[p],changes);target=apply(source,records(ips))
        if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
        for e in f['edits']:
            d=int(e['copy_offset'],16)
            if base[d:d+e['capacity']]!=bytes(e['capacity']):raise ValueError('Réserve occupée')
        for root,c in f['contexts'].items():
            if commands(logical_context(target,f,root,p))!=commands(bytes.fromhex(c[p]['baseline_hex'])):raise ValueError('Commandes du contexte modifiées')
        (out/f'EarthBound_Beginnings_FR_v51_{p}.ips').write_bytes(ips)
        profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p]))}
    plan={'version':'v51','source_sha256':sha(source),'text_spans_translated':len(f['edits']),'contexts_revised':len(f['contexts']),'deferred':len(f['deferred']),'entry_bytes_changed_per_span':5,'literal_reference_operands_rewritten':0,'shared_dictionary_modified':False,'natural_scene_access_verified':False,'profiles':profiles}
    for name,data in (('v51_fixtures',f),('validation_v51',plan)):(ROOT/f'tools/v51/{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return plan
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
