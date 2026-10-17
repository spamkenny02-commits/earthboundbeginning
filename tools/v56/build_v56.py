"""Translate dialogue and shared feedback text while preserving original commands."""
import argparse,bisect,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v55'))
from build_v55 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,parse,encode,dictionary_from_rom,decode,spans_fr,pointer,commands,free_reserves

def text_layout(raw):
    # Each run ends immediately before a command; append a temporary terminator.
    spans=spans_fr(raw+b'\x02');cursor=0
    for a,z in spans:
        gap=raw[cursor:a]
        if len(gap)%2 or any(gap[i]!=0x10 for i in range(0,len(gap),2)):raise ValueError('Commande non permise dans le segment')
        cursor=z
    if cursor!=len(raw) or not spans or spans[0][0]!=0:raise ValueError('Segment textuel invalide')
    return spans

def copy_text(e,profile):
    raw=bytes.fromhex(e['profiles'][profile]['baseline_hex']);spans=text_layout(raw)
    if len(spans)!=len(e['fr']):raise ValueError('Nombre de fragments divergent')
    out=bytearray();cursor=0
    for (a,z),fr in zip(spans,e['fr']):out.extend(raw[cursor:a]);out.extend(encode(fr,profile));cursor=z
    out.extend(raw[cursor:]);return bytes(out)

def fixtures_from_baselines(source,bases,priors):
    if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
    targets=sorted(set(pointer_index(source))|set().union(*(set(pointer_index(d)) for d in bases.values())))
    reserves=free_reserves(source,bases,priors,targets);free=[r[:] for r in reserves]
    dictionary=dictionary_from_rom(source);edits=[];contexts={}
    for c in json.loads((ROOT/'tools/v56/candidates_v56.json').read_text())['entries']:
        a,z,r=int(c['offset'],16),int(c['end'],16),int(c['context'],16);e=dict(c);e['profiles']={}
        i=bisect.bisect_right(targets,a)
        if z-a<5 or i<len(targets) and targets[i]<a+5:raise ValueError('Entrée intérieure écrasée')
        e['interior_targets']=[f'{t:06X}' for t in targets[i:bisect.bisect_left(targets,z)]]
        context={}
        for p,data in bases.items():
            parsed=parse(data,r,8192,extra_glyphs=range(0xB0,0xC0));raw=data[a:z]
            if parsed['error'] or not parsed['terminal']:raise ValueError('Contexte non fermé')
            allsp=spans_fr(data[r:parsed['end']]);local=text_layout(raw)
            if any((a-r+lo,a-r+hi) not in allsp for lo,hi in local):raise ValueError('Frontière de texte invalide')
            e['profiles'][p]={'baseline_hex':raw.hex(),'english_or_prior_french':[decode(raw[lo:hi],dictionary) for lo,hi in local]}
            context[p]={'end':f"{parsed['end']:06X}",'baseline_hex':data[r:parsed['end']].hex()}
            copy_text(e,p)
        contexts[c['context']]=context;edits.append(e)
    for e in sorted(edits,key=lambda e:(-max(len(copy_text(e,p)) for p in bases),e['offset'])):
        size=max(len(copy_text(e,p)) for p in bases)+5
        for region in free:
            if region[1]-region[0]>=size:
                e['copy_offset']=f'{region[0]:06X}';e['capacity']=size;region[0]=(region[0]+size+3)&~3;break
        else:raise ValueError('Réserve épuisée')
    return {'version':'v56','base':'v55','edits':edits,'contexts':contexts,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves]}

def additions_from_fixtures(f,profile):
    changes=[]
    for e in f['edits']:
        a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
        if len(bytes.fromhex(e['profiles'][profile]['baseline_hex']))!=z-a or z-a<5:raise ValueError('Capacité source invalide')
        if any(a<int(t,16)<a+5 for t in e['interior_targets']):raise ValueError('Entrée intérieure écrasée')
        text=copy_text(e,profile)
        if len(text)+5>e['capacity']:raise ValueError('Traduction trop longue')
        if not any(int(lo,16)<=d and d+e['capacity']<=int(hi,16) for lo,hi in f['reserves']):raise ValueError('Copie hors réserve')
        changes.extend(((a,b'\x0a'+pointer(d)),(d,text+b'\x0a'+pointer(z))))
    ranges=sorted((a,a+len(v)) for a,v in changes)
    if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Écritures en chevauchement')
    return changes

def logical_context(target,f,root,profile):
    a=int(root,16);z=int(f['contexts'][root][profile]['end'],16);cursor=a;out=bytearray()
    for e in sorted(f['edits'],key=lambda e:int(e['offset'],16)):
        p,q=int(e['offset'],16),int(e['end'],16)
        if not a<=p<z:continue
        d=int(e['copy_offset'],16);text=copy_text(e,profile)
        if target[p:p+5]!=b'\x0a'+pointer(d) or target[d:d+len(text)+5]!=text+b'\x0a'+pointer(q):raise ValueError('Trajet de saut invalide')
        if target[p+5:q]!=bytes.fromhex(e['profiles'][profile]['baseline_hex'])[5:]:raise ValueError('Entrée intérieure modifiée')
        out.extend(target[cursor:p]);out.extend(text);cursor=q
    out.extend(target[cursor:z]);return bytes(out)

def build(rom,out):
    source=Path(rom).read_bytes();oldplan=json.loads((ROOT/'tools/v55/validation_v55.json').read_text())
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v55_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=oldplan['profiles'][p]['sha256'] for p,v in priors.items()):raise ValueError('IPS V55 divergent')
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
        (out/f'EarthBound_Beginnings_FR_v56_{p}.ips').write_bytes(ips)
        profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p]))}
    plan={'version':'v56','source_sha256':sha(source),'text_runs_revised':len(f['edits']),'new_text_fragments':sum(len(e['fr'])-len(e['already_french_spans']) for e in f['edits']),'prior_french_fragments_preserved':sum(len(e['already_french_spans']) for e in f['edits']),'contexts_revised':len(f['contexts']),'literal_reference_operands_rewritten':0,'shared_dictionary_modified':False,'natural_scene_access_verified':False,'profiles':profiles}
    for name,data in (('v56_fixtures',f),('validation_v56',plan)):(ROOT/f'tools/v56/{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return plan
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
