"""Build V46: validate the preparation, localize food and finish seven group calls."""
import argparse,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/v45')]
from build_v45 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,pointer,transform,parse,length,text_spans,expand,dictionary_from_rom,reference_proof
from build_v19 import encode
# Pinned after checking the published V45 artifacts.
BASE_SHA={'accents':'9eaf5f1c58b9e9f80c4b0a7ae8d43cf898d472d4f6b31b7e3d8742457bf42e75','ascii':'8f9c9b3a1c4ee12d789843ade2c8095370ba5f33d7a0ec2d8495f8fd88de2434'}
HELPER=0x32A780
FOOD_SOURCE=0x35ECD5
FOOD_FR=['@Objet consommé par ',' :','  ']
SOLO_SOURCE=0x097BAB
SOLO_FR=['@Objet consommé par ',' :','  ','.']


def audit_preparation(original,baseline):
    selection=json.loads((ROOT/'tools/v46/v46_selection.json').read_text())
    entries=[]
    for e in selection['entries']:
        a=int(e['id'],16);raw=bytes.fromhex(e['raw_hex'])
        if original[a:a+len(raw)]!=raw:raise ValueError('Source de préparation divergente')
        changed=baseline[a:a+len(raw)]!=raw
        identical=all(s['original']==s['french'] for s in e['text_fr_segments'])
        if changed:status='already_modified_by_prior_versions'
        elif identical:status='identical_french_draft'
        else:status='requires_further_audit'
        entries.append({'id':e['id'],'status':status})
    return {'selected':len(entries),'already_modified':sum(e['status']=='already_modified_by_prior_versions' for e in entries),
            'identical_drafts':sum(e['status']=='identical_french_draft' for e in entries),
            'new_integrations_from_preparation':0,'entries':entries}


def choose_reserve(original,baselines):
    mask=bytearray(SIZE)
    refs=set(pointer_index(original))
    for p,data in baselines.items():
        refs.update(pointer_index(data))
        for a,raw in records((ROOT/f'patches/EarthBound_Beginnings_FR_v45_{p}.ips').read_bytes()):mask[a:a+len(raw)]=b'\1'*len(raw)
    for a in refs:mask[a]=1
    safe=bytearray(a==0 and all(d[i]==0 for d in baselines.values()) and not mask[i] for i,a in enumerate(original))
    for match in re.finditer(b'\1{160,}',safe):
        a,z=match.span()
        if not (0x250000<=a<0x260000 or 0x320000<=a<0x330000):continue
        a=(a+31)&~15;z=(z-16)&~15
        if z-a>=128:return a,z
    raise ValueError('Aucune réserve suffisante')


def make_fixtures(original,baselines):
    contexts=json.loads((ROOT/'tools/v46/contexts_v46.json').read_text());profiles={}
    reserve=choose_reserve(original,baselines)
    dictionary=dictionary_from_rom(original)
    parsed=parse(original,FOOD_SOURCE,8192);end=parsed['end'];raw=original[FOOD_SOURCE:end]
    spans=[list(x) for x in text_spans(raw)]
    if parsed['error'] or not parsed['terminal'] or len(spans)!=3:raise ValueError('Source alimentaire incorrecte')
    for profile,data in baselines.items():
        prior_plan=json.loads((ROOT/'tools/v45/validation_v45.json').read_text())
        helper=next(e for e in prior_plan['profiles'][profile]['relocated'] if e['id']=='07E6D7')
        if int(helper['offset'],16)!=HELPER:raise ValueError('Routine française V45 divergente')
        ctx=[]
        for item in contexts:
            a,q=int(item['start'],16),int(item['pointer'],16);p=parse(data,a,8192,extra_glyphs=range(0xB0,0xC0))
            if p['error'] or not p['terminal'] or (q,0x7E6D7) not in p['refs']:raise ValueError('Contexte français divergent')
            entry={**item,'end':f"{p['end']:06X}",'baseline_hex':data[a:p['end']].hex(),'proof':reference_proof(data,q,0x7E6D7)}
            if item['replacement'] is not None:
                lo=int(item['text_offset'],16);hi=lo+item['text_capacity']
                if (lo,hi) not in p['spans']:raise ValueError('Plage française divergente')
                if len(encode(item['replacement'],profile))>hi-lo:raise ValueError('Texte trop long')
                entry['old_text_hex']=data[lo:hi].hex()
            ctx.append(entry)
        foods=[]
        for ident,french in ((FOOD_SOURCE,FOOD_FR),(SOLO_SOURCE,SOLO_FR)):
            parsed_food=parse(original,ident,8192);stop=parsed_food['end'];body=original[ident:stop]
            food_spans=[list(x) for x in text_spans(body)]
            if parsed_food['error'] or not parsed_food['terminal'] or len(food_spans)!=len(french):raise ValueError('Source alimentaire incorrecte')
            if data[ident:stop]!=body:raise ValueError('Source alimentaire déjà modifiée')
            refs=[]
            for q in pointer_index(data).get(ident,[]):
                refs.append({'offset':f'{q:06X}','old_target':f'{ident:06X}','proof':reference_proof(data,q,ident)})
            if len(refs)!=(1 if ident==FOOD_SOURCE else 2):raise ValueError('Inventaire alimentaire divergent')
            foods.append({'id':f'{ident:06X}','end':f'{stop:06X}','original_hex':body.hex(),
                'spans':food_spans,'english':[expand(body[a:b],dictionary) for a,b in food_spans],
                'fr':french,'references':refs})
        profiles[profile]={'contexts':ctx,'foods':foods,
            'food_group_callback_preserved_hex':data[0x35ECFA:0x35ED61].hex()}
    audits={p:audit_preparation(original,d) for p,d in baselines.items()}
    if audits['accents']!=audits['ascii']:raise ValueError('Audit de préparation divergent')
    if (audits['accents']['already_modified'],audits['accents']['identical_drafts'])!=(98,2):raise ValueError('Audit de préparation inattendu')
    return {'version':'v46','base':'v45','reserve':[f'{x:06X}' for x in reserve],
            'helper':f'{HELPER:06X}','audit_preparation':audits['accents'],'profiles':profiles}


def additions_from_fixtures(fixtures,profile):
    f=fixtures['profiles'][profile];changes=[];references=[]
    helper=int(fixtures['helper'],16)
    for e in f['contexts']:
        q=int(e['pointer'],16);changes.append((q,pointer(helper)))
        references.append({'offset':e['pointer'],'old_target':'07E6D7','new_target':f'{helper:06X}','proof':e['proof']})
        if e['replacement'] is not None:
            changes.append((int(e['text_offset'],16),encode(e['replacement'],profile).ljust(e['text_capacity'],b'\x50')))
    moved=[];cursor=int(fixtures['reserve'][0],16)
    for food in f['foods']:
        raw=bytes.fromhex(food['original_hex']);dest=cursor
        out,local=transform(raw,food['spans'],food['fr'],dest,profile);parsed=parse(raw,0,len(raw)+1)
        rewired=[]
        for q,target in parsed['refs']:
            if target==0x7E6D7:
                out[local[q]:local[q]+4]=pointer(helper)
                rewired.append({'offset':f'{dest+local[q]:06X}','old_target':'07E6D7','new_target':f'{helper:06X}'})
        if len(rewired)!=(1 if food['id']==f'{FOOD_SOURCE:06X}' else 0) or dest+len(out)>int(fixtures['reserve'][1],16):raise ValueError('Copie alimentaire incorrecte')
        check=parse(bytes(out),0,len(out)+1,extra_glyphs=range(0xB0,0xC0))
        if check['error'] or not check['terminal'] or check['end']!=len(out):raise ValueError('Copie alimentaire non close')
        changes.append((dest,bytes(out)))
        moved.append({'id':food['id'],'offset':f'{dest:06X}','new_length':len(out),'internal_refs':rewired})
        for r in food['references']:
            changes.append((int(r['offset'],16),pointer(dest)))
            references.append({**r,'new_target':f'{dest:06X}'})
        cursor=(dest+len(out)+3)&~3
    ranges=sorted((a,a+len(raw)) for a,raw in changes)
    if any(b>c for (_,b),(c,_) in zip(ranges,ranges[1:])):raise ValueError('Écritures en chevauchement')
    return changes,moved,references


def build(rom_path,out):
    source=Path(rom_path).read_bytes()
    if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM USA 1.2 originale requise')
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v45_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=BASE_SHA[p] for p,v in priors.items()):raise ValueError('IPS V45 divergent')
    bases={p:apply(source,records(v)) for p,v in priors.items()}
    fixtures=make_fixtures(source,bases);out=Path(out);out.mkdir(parents=True,exist_ok=True);results={}
    for profile,baseline in bases.items():
        changes,food,refs=additions_from_fixtures(fixtures,profile);patch=append(priors[profile],changes)
        target=apply(source,records(patch));mask=bytearray(SIZE)
        for a,raw in changes:mask[a:a+len(raw)]=b'\1'*len(raw)
        if any(a!=b and not m for a,b,m in zip(baseline,target,mask)):raise ValueError('Écriture hors plages')
        if target!=apply(baseline,changes):raise ValueError('IPS non autonome')
        (out/f'EarthBound_Beginnings_FR_v46_{profile}.ips').write_bytes(patch)
        results[profile]={'sha256':sha(patch),'target_rom_sha256':sha(target),'records_added':len(changes),
                         'foods':food,'references_rewritten':refs,'outside_declared_ranges_unchanged':True}
    plan={'base':'V45','source_sha256':sha(source),'newly_translated_food_messages':2,
          'existing_french_contexts_corrected':7,'existing_phrasings_revised':5,
          'preparation_entries_newly_integrated':0,'shared_dictionary_modified':False,'profiles':results}
    (ROOT/'tools/v46/v46_fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'tools/v46/validation_v46.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    return plan

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args()
    print(json.dumps(build(a.rom,a.out),ensure_ascii=False,indent=2))
