"""Finish English spans in mixed French/English scripts without moving commands."""
import argparse,bisect,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v48'))
from build_v48 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,parse,length,encode,dictionary_from_rom,expand,render
from build_v19 import ACCENTS
BASE_SHA={'accents': '3cab19b8e176a82dd6e6818724e4ea0eb1d4d287da10dc757b556b13525bb3f7', 'ascii': '7e857bb7852e5b074cd3311d5eee05d8146cd0883953917488ae8f3f74ee1ffd'}

def spans_fr(raw):
    parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
    if parsed['error'] or not parsed['terminal'] or parsed['end']!=len(raw):raise ValueError('Contexte non fermé')
    spans=[];start=None;pos=0
    while pos<len(raw):
        c=raw[pos]
        if 0x50<=c<0xC0 or c in (0xC8,0xC9,0xCA,0xCB,0x15,0x16,0x17):
            if start is None:start=pos
            pos+=2 if c in (0x15,0x16,0x17) else 1
        else:
            if start is not None:spans.append((start,pos));start=None
            pos+=length(raw,pos)
    if start is not None:spans.append((start,pos))
    return spans

def decode(raw,dictionary):
    out=[];p=0
    while p<len(raw):
        c=raw[p]
        if c in (0x15,0x16,0x17):out.append(dictionary[raw[p:p+2].hex(' ').upper()]['text_en']);p+=2
        else:out.append(ACCENTS[c-0xB0] if 0xB0<=c<0xC0 else render(raw[p:p+1]));p+=1
    return ''.join(out)

def fixtures_from_baselines(original,bases):
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
    tr=json.loads((ROOT/'tools/v49/translations_v49.json').read_text())
    config=json.loads((ROOT/'tools/v49/contexts_v49.json').read_text())
    dictionary=dictionary_from_rom(original)
    targets=sorted(set(pointer_index(original))|set(pointer_index(bases['accents']))|set(pointer_index(bases['ascii'])))
    edits={};contexts=[];deferred=[]
    for ident in sorted(config['roots']):
        start=int(ident,16);profiles={};found=[]
        for profile,data in bases.items():
            parsed=parse(data,start,8192,extra_glyphs=range(0xB0,0xC0))
            if parsed['error'] or not parsed['terminal']:raise ValueError('Contexte invalide: '+ident)
            raw=data[start:parsed['end']];spans=spans_fr(raw)
            profiles[profile]={'end':f"{parsed['end']:06X}",'baseline_hex':raw.hex(),'spans':spans}
        if profiles['accents']['spans']!=profiles['ascii']['spans'] or profiles['accents']['end']!=profiles['ascii']['end']:raise ValueError('Profils de contexte divergents')
        raw=bytes.fromhex(profiles['accents']['baseline_hex'])
        for lo,hi in profiles['accents']['spans']:
            a,z=start+lo,start+hi
            if original[a:z]!=raw[lo:hi]:continue
            en=decode(raw[lo:hi],dictionary)
            if en not in tr:continue
            fr=tr[en]
            if en==fr:continue
            if bases['ascii'][a:z]!=original[a:z]:raise ValueError('Texte anglais divergent')
            index=bisect.bisect_right(targets,a)
            if index<len(targets) and targets[index]<z:
                deferred.append({'offset':f'{a:06X}','end':f'{z:06X}','context':ident,'reason':'interior_literal_target','target':f'{targets[index]:06X}'});continue
            for profile in bases:
                if len(encode(fr,profile))>z-a:raise ValueError('Traduction trop longue: '+en)
            key=(a,z)
            e=edits.setdefault(key,{'offset':f'{a:06X}','end':f'{z:06X}','source_hex':original[a:z].hex(),'english':en,'fr':fr,'contexts':[]})
            if e['fr']!=fr:raise ValueError('Traductions concurrentes')
            e['contexts'].append(ident);found.append(f'{a:06X}')
        if found:contexts.append({'id':ident,'profiles':profiles,'edits':found})
    ranges=sorted(edits)
    if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Textes en chevauchement')
    if not edits:raise ValueError('Aucune traduction nouvelle')
    return {'version':'v49','base':'v48','edits':[edits[k] for k in ranges],'contexts':contexts,'deferred':deferred,'excluded':config['excluded']}

def additions_from_fixtures(f,profile):
    changes=[]
    for e in f['edits']:
        a,z=int(e['offset'],16),int(e['end'],16);raw=encode(e['fr'],profile)
        if len(raw)>z-a:raise ValueError('Traduction trop longue')
        if z-a!=len(bytes.fromhex(e['source_hex'])):raise ValueError('Capacité divergente')
        changes.append((a,raw.ljust(z-a,b'\x50')))
    ranges=sorted((a,a+len(v)) for a,v in changes)
    if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Écritures en chevauchement')
    return changes

def build(rom,out):
    original=Path(rom).read_bytes()
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v48_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=BASE_SHA[p] for p,v in priors.items()):raise ValueError('IPS V48 divergent')
    bases={p:apply(original,records(v)) for p,v in priors.items()}
    f=fixtures_from_baselines(original,bases);out=Path(out);out.mkdir(parents=True,exist_ok=True);profiles={}
    for p,base in bases.items():
        changes=additions_from_fixtures(f,p);ips=append(priors[p],changes);target=apply(original,records(ips))
        if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
        mask=bytearray(SIZE)
        for a,v in changes:mask[a:a+len(v)]=b'\1'*len(v)
        if any(a!=b and not m for a,b,m in zip(base,target,mask)):raise ValueError('Écriture hors texte')
        for e in f['contexts']:
            a=int(e['id'],16);z=int(e['profiles'][p]['end'],16);parsed=parse(target,a,8192,extra_glyphs=range(0xB0,0xC0))
            if parsed['error'] or not parsed['terminal'] or parsed['end']!=z:raise ValueError('Contexte après modification invalide')
        (out/f'EarthBound_Beginnings_FR_v49_{p}.ips').write_bytes(ips)
        profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p])),'rom_roundtrip':True,'outside_text_unchanged':True}
    plan={'version':'v49','base':'v48','source_sha256':sha(original),'text_spans_translated':len(f['edits']),'lexical_spans_translated':sum(any(c.isalpha() for c in e['fr']) for e in f['edits']),'distinct_english_fragments':len({e['english'] for e in f['edits']}),'contexts_revised':len(f['contexts']),'script_addresses_changed':False,'shared_dictionary_modified':False,'profiles':profiles,'natural_scene_access_verified':False}
    (ROOT/'tools/v49/v49_fixtures.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n');(ROOT/'tools/v49/validation_v49.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    return plan
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
