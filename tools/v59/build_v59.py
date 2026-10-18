"""Translate dialogue and shared feedback text while preserving original commands."""
import argparse,bisect,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v57'))
from build_v57 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,parse,encode,dictionary_from_rom,decode,spans_fr,pointer,commands

from build_v48 import length
from safe_storage import safe_reserves,sprite_digest,POOL_LO,POOL_HI
GRAMMAR_OLD=0x07E66E
GRAMMAR_NEW=0x251E0C
GRAMMAR_HEX='a39102'
GRAMMAR_HELPERS={'sa':(GRAMMAR_NEW,GRAMMAR_HEX),'son':(0x251E1C,'a39f9e02')}

def free_reserves(source,bases,priors,targets):
    return safe_reserves(source,bases,priors,targets,records)[0]

def text_layout(raw):
    body=raw[:-1] if raw.endswith(b'\x02') else raw
    spans=spans_fr(body+b'\x02');cursor=0
    for a,z in [*spans,(len(body),len(body))]:
        gap=body[cursor:a];pos=0
        while pos<len(gap):
            c=gap[pos]
            if c not in (0x00,0x01,0x03,0x08,0x10,0x19,0x1B,0x1C) or c==0x1B and gap[pos+1] not in (0x01,0x04):raise ValueError('Commande non permise dans le segment')
            if c==0x19 and gap[pos:pos+2]!=b'\x19\x1f':raise ValueError('Commande de nom non permise')
            if c==0x08 and gap[pos+1:pos+5]!=pointer(GRAMMAR_OLD):raise ValueError('Appel non permis dans le segment')
            n=length(gap,pos)
            if n<1 or pos+n>len(gap):raise ValueError('Commande tronquée')
            pos+=n
        cursor=z
    if not spans or spans[0][0]!=0:raise ValueError('Segment textuel invalide')
    return spans

def copy_text(e,profile):
    raw=bytes.fromhex(e['profiles'][profile]['baseline_hex']);spans=text_layout(raw)
    if len(spans)!=len(e['fr']):raise ValueError('Nombre de fragments divergent')
    out=bytearray();cursor=0
    for (a,z),fr in zip(spans,e['fr']):out.extend(raw[cursor:a]);out.extend(encode(fr,profile));cursor=z
    out.extend(raw[cursor:])
    refs=parse(bytes(out)+b'\x02',0,len(out)+2,extra_glyphs=range(0xB0,0xC0))['refs']
    if e.get('possessive_call'):
        if len(refs)!=1 or refs[0][1]!=GRAMMAR_OLD:raise ValueError('Appel possessif divergent')
        q,t=refs[0]
        if out[q-1]!=0x08:raise ValueError('Appel possessif non ancré')
        out[q:q+4]=pointer(GRAMMAR_HELPERS[e.get('grammar_helper','sa')][0])
    elif refs:raise ValueError('Appel non déclaré')
    return bytes(out)

def context_commands(raw):
    normalized=bytearray(raw);parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
    if parsed['error'] or not parsed['terminal']:raise ValueError('Contexte non fermé')
    for q,t in parsed['refs']:
        if t in {a for a,h in GRAMMAR_HELPERS.values()} and raw[q-1]==0x08:normalized[q:q+4]=pointer(GRAMMAR_OLD)
    return commands(bytes(normalized))

def fixtures_from_baselines(source,bases,priors):
    if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
    targets=sorted(set(pointer_index(source))|set().union(*(set(pointer_index(d)) for d in bases.values())))
    reserves,storage=safe_reserves(source,bases,priors,targets,records);free=[r[:] for r in reserves]
    dictionary=dictionary_from_rom(source);edits=[];contexts={}
    for c in json.loads((ROOT/'tools/v59/candidates_v59.json').read_text())['entries']:
        a,z,r=int(c['offset'],16),int(c['end'],16),int(c['context'],16);e=dict(c);e['profiles']={}
        i=bisect.bisect_right(targets,a)
        if z-a<5 or i<len(targets) and targets[i]<a+5:raise ValueError('Entrée intérieure écrasée: '+c['offset'])
        e['interior_targets']=[f'{t:06X}' for t in targets[i:bisect.bisect_left(targets,z)]]
        context={}
        for p,data in bases.items():
            parsed=parse(data,r,8192,extra_glyphs=range(0xB0,0xC0));raw=data[a:z]
            if parsed['error'] or not parsed['terminal']:raise ValueError('Contexte non fermé')
            allsp=spans_fr(data[r:parsed['end']]);local=text_layout(raw)
            if any((a-r+lo,a-r+hi) not in allsp for lo,hi in local):raise ValueError('Frontière de texte invalide')
            if e.get('possessive_call'):
                helper,h=GRAMMAR_HELPERS[e.get('grammar_helper','sa')]
                if data[helper:helper+len(bytes.fromhex(h))]!=bytes.fromhex(h):raise ValueError('Copie grammaticale V50 divergente')
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
    return {'storage':storage,'version':'v59','base':'v58','edits':edits,'contexts':contexts,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves]}

def additions_from_fixtures(f,profile):
    changes=[]
    for e in f['edits']:
        a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
        if len(bytes.fromhex(e['profiles'][profile]['baseline_hex']))!=z-a or z-a<5:raise ValueError('Capacité source invalide')
        if any(a<int(t,16)<a+5 for t in e['interior_targets']):raise ValueError('Entrée intérieure écrasée')
        text=copy_text(e,profile)
        if len(text)+5>e['capacity']:raise ValueError('Traduction trop longue')
        if not POOL_LO<=d<d+e['capacity']<=POOL_HI or not any(int(lo,16)<=d and d+e['capacity']<=int(hi,16) for lo,hi in f['reserves']):raise ValueError('Copie hors réserve')
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
    source=Path(rom).read_bytes();oldplan=json.loads((ROOT/'tools/v58/validation_v58.json').read_text())
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v58_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=oldplan['profiles'][p]['sha256'] for p,v in priors.items()):raise ValueError('IPS V58 divergent')
    bases={p:apply(source,records(v)) for p,v in priors.items()};f=fixtures_from_baselines(source,bases,priors)
    out=Path(out);out.mkdir(parents=True,exist_ok=True);profiles={}
    for p,base in bases.items():
        changes=additions_from_fixtures(f,p);ips=append(priors[p],changes);target=apply(source,records(ips))
        if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
        for e in f['edits']:
            d=int(e['copy_offset'],16)
            if base[d:d+e['capacity']]!=bytes(e['capacity']):raise ValueError('Réserve occupée')
        if sprite_digest(target)!=f['storage']['baseline_sprite_sha256'][p]:raise ValueError('Données de sprites modifiées')
        for root,c in f['contexts'].items():
            if context_commands(logical_context(target,f,root,p))!=context_commands(bytes.fromhex(c[p]['baseline_hex'])):raise ValueError('Commandes du contexte modifiées')
        (out/f'EarthBound_Beginnings_FR_v59_{p}.ips').write_bytes(ips)
        profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p]))}
    plan={'version':'v59','source_sha256':sha(source),'text_runs_revised':len(f['edits']),'new_text_fragments':sum(a!=b for e in f['edits'] for a,b in zip(e['profiles']['accents']['english_or_prior_french'],e['fr'])),'retained_text_fragments':sum(a==b for e in f['edits'] for a,b in zip(e['profiles']['accents']['english_or_prior_french'],e['fr'])),'prior_french_fragments_preserved':sum(len(e['already_french_spans']) for e in f['edits']),'contexts_revised':len(f['contexts']),'literal_reference_operands_rewritten':0,'shared_dictionary_modified':False,'private_possessive_calls_redirected':sum(bool(e.get('possessive_call')) for e in f['edits']),'existing_v50_grammar_helpers_reused':[],'sprite_groups_protected':f['storage']['sprite_groups'],'sprite_frames_protected':f['storage']['sprite_frames'],'new_copies_in_original_padding':True,'natural_scene_access_verified':False,'profiles':profiles}
    for name,data in (('v59_fixtures',f),('validation_v59',plan)):(ROOT/f'tools/v59/{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return plan
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
