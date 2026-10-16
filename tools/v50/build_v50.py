"""Translate remaining English spans and add scoped French possessive helpers."""
import argparse,bisect,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v48'))
from build_v48 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,parse,length,encode,dictionary_from_rom,expand,render
from build_v19 import ACCENTS
from build_v33 import transform,pointer
from build_v48 import reference_proof
HELPERS={0x07E660:'sa',0x07E66B:'sa',0x35C758:'son',0x35C764:'son'}
CALLS=((0x3479FF,0x07E660),(0x35C6FC,0x35C758))
BASE_SHA={'accents': '5d9e3cf5c8ef06d95a2ae337b76fce2edb69c4c797a0a6e727737e574bfb73b1', 'ascii': '33aaa7ef567cf6c434e89af5a464171c60bebc8333f417f5db05d94ba33f18f1'}

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

def helper_fixtures(original,bases):
    mask=bytearray(SIZE);refs=set(pointer_index(original))
    for p,data in bases.items():
        refs.update(pointer_index(data))
        for a,raw in records((ROOT/f'patches/EarthBound_Beginnings_FR_v49_{p}.ips').read_bytes()):mask[a:a+len(raw)]=b'\1'*len(raw)
    for a in refs:mask[a]=1
    reserve=None
    for lo,hi in ((0x250000,0x260000),(0x320000,0x330000)):
        safe=bytes(not mask[i] and original[i]==0 and all(d[i]==0 for d in bases.values()) for i in range(lo,hi))
        for match in re.finditer(b'\1{96,}',safe):
            a,z=lo+match.start(),lo+match.end();a=(a+31)&~15;z=(z-16)&~15
            if z-a>=64:reserve=(a,z);break
        if reserve:break
    if not reserve:raise ValueError('Réserve grammaticale épuisée')
    helpers=[]
    for a,fr in HELPERS.items():
        parsed=parse(original,a,256);end=parsed['end'];raw=original[a:end]
        if parsed['error'] or not parsed['terminal'] or any(d[a:end]!=raw for d in bases.values()):raise ValueError('Source grammaticale divergente')
        helpers.append({'id':f'{a:06X}','end':f'{end:06X}','raw_hex':raw.hex(),'spans':spans_fr(raw),'fr':[fr]})
    calls=[]
    for root,target in CALLS:
        parsed=parse(bases['accents'],root,8192,extra_glyphs=range(0xB0,0xC0));matches=[q for q,t in parsed['refs'] if t==target]
        if parsed['error'] or len(matches)!=1:raise ValueError('Appel grammatical divergent')
        q=matches[0]
        if bases['ascii'][q:q+4]!=pointer(target):raise ValueError("Profils d'appel divergents")
        calls.append({'root':f'{root:06X}','offset':f'{q:06X}','old_target':f'{target:06X}','command_candidate':reference_proof(bases['accents'],q,target)})
    return {'reserve':[f'{a:06X}' for a in reserve],'scripts':helpers,'calls':calls}

def helper_additions(f,profile):
    cursor=int(f['reserve'][0],16);built=[];mapping={};changes=[];moved=[]
    for e in f['scripts']:
        raw=bytes.fromhex(e['raw_hex']);out,local=transform(raw,e['spans'],e['fr'],cursor,profile)
        a=int(e['id'],16)
        for q,v in local.items():
            if q<len(raw):mapping[a+q]=cursor+v
        built.append((e,cursor,out,local));cursor=(cursor+len(out)+3)&~3
    if cursor>int(f['reserve'][1],16):raise ValueError('Réserve grammaticale épuisée')
    for e,a,out,local in built:
        parsed=parse(bytes.fromhex(e['raw_hex']),0,256);refs=[]
        for q,t in parsed['refs']:
            if t in mapping:
                out[local[q]:local[q]+4]=pointer(mapping[t]);refs.append({'offset':f'{a+local[q]:06X}','old_target':f'{t:06X}','new_target':f'{mapping[t]:06X}'})
        check=parse(bytes(out),0,len(out)+1,extra_glyphs=range(0xB0,0xC0))
        if check['error'] or not check['terminal'] or check['end']!=len(out):raise ValueError('Copie grammaticale non fermée')
        changes.append((a,bytes(out)));moved.append({'id':e['id'],'offset':f'{a:06X}','length':len(out),'internal_refs':refs})
    for e in f['calls']:changes.append((int(e['offset'],16),pointer(mapping[int(e['old_target'],16)])))
    return changes,moved

def fixtures_from_baselines(original,bases):
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
    tr=json.loads((ROOT/'tools/v50/translations_v50.json').read_text())
    config=json.loads((ROOT/'tools/v50/contexts_v50.json').read_text())
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
    return {'version':'v50','base':'v49','edits':[edits[k] for k in ranges],'contexts':contexts,'deferred':deferred,'excluded':config['excluded'],'grammar':helper_fixtures(original,bases)}

def additions_from_fixtures(f,profile):
    changes=[]
    for e in f['edits']:
        a,z=int(e['offset'],16),int(e['end'],16);raw=encode(e['fr'],profile)
        if len(raw)>z-a:raise ValueError('Traduction trop longue')
        if z-a!=len(bytes.fromhex(e['source_hex'])):raise ValueError('Capacité divergente')
        changes.append((a,raw.ljust(z-a,b'\x50')))
    helper_changes,_=helper_additions(f['grammar'],profile);changes.extend(helper_changes)
    ranges=sorted((a,a+len(v)) for a,v in changes)
    if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Écritures en chevauchement')
    return changes

def build(rom,out):
    original=Path(rom).read_bytes()
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v49_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=BASE_SHA[p] for p,v in priors.items()):raise ValueError('IPS V49 divergent')
    bases={p:apply(original,records(v)) for p,v in priors.items()}
    f=fixtures_from_baselines(original,bases);out=Path(out);out.mkdir(parents=True,exist_ok=True);profiles={}
    for p,base in bases.items():
        changes=additions_from_fixtures(f,p);ips=append(priors[p],changes);target=apply(original,records(ips))
        if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
        mask=bytearray(SIZE)
        for a,v in changes:mask[a:a+len(v)]=b'\1'*len(v)
        if any(a!=b and not m for a,b,m in zip(base,target,mask)):raise ValueError('Écriture hors texte')
        _,helper_layout=helper_additions(f['grammar'],p)
        for e in f['contexts']:
            a=int(e['id'],16);z=int(e['profiles'][p]['end'],16);parsed=parse(target,a,8192,extra_glyphs=range(0xB0,0xC0))
            if parsed['error'] or not parsed['terminal'] or parsed['end']!=z:raise ValueError('Contexte après modification invalide')
        (out/f'EarthBound_Beginnings_FR_v50_{p}.ips').write_bytes(ips)
        profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p])),'rom_roundtrip':True,'outside_declared_ranges_unchanged':True,'grammar_copies':helper_layout}
    plan={'version':'v50','base':'v49','source_sha256':sha(original),'text_spans_translated':len(f['edits']),'lexical_spans_translated':sum(any(c.isalpha() for c in e['fr']) for e in f['edits']),'distinct_english_fragments':len({e['english'] for e in f['edits']}),'contexts_revised':len(f['contexts']),'main_script_addresses_changed':False,'private_grammar_copies':4,'grammar_call_operands_changed':2,'shared_dictionary_modified':False,'profiles':profiles,'natural_scene_access_verified':False}
    (ROOT/'tools/v50/v50_fixtures.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n');(ROOT/'tools/v50/validation_v50.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    return plan
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
