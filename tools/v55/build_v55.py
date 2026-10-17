"""Translate inline menu definitions with a five-byte entry jump.

Private definitions retain option order and return to the original selector.
The labels' original tails and interior entry addresses remain intact.
"""
import argparse,bisect,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v53'))
from build_v53 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,parse,encode,dictionary_from_rom,decode,spans_fr,pointer,commands,free_reserves

def width(raw,profile,f):
    widths=bytes.fromhex(f['font']['profiles'][profile]['widths_hex'])
    if any(not 0x50<=c<0xD0 for c in raw):raise ValueError('Glyphe invalide')
    return sum(widths[c-0x50]+f['font']['advance_extra'] for c in raw)

def padding(pixels,profile,f):
    if pixels<6:raise ValueError('Ligne trop longue')
    choices=[bytes.fromhex(v) for v in f['font']['padding_codes']];dp={0:b''}
    for n in range(1,pixels+1):
        candidates=[dp[n-width(c,profile,f)]+c for c in choices if n-width(c,profile,f) in dp]
        if candidates:dp[n]=min(candidates,key=lambda v:(len(v),v))
    if pixels not in dp:raise ValueError('Espacement impossible')
    return dp[pixels]

def row_bytes(row,profile,f):
    raw=bytes.fromhex(row['source_hex']);d=raw.index(0x54)
    city=''.join(chr(c-48) for c in raw[:next(i for i,c in enumerate(raw) if c>=0xC8)])
    fare=int(''.join(chr(c-48) for c in raw[d+1:-1]))
    if city!=row['city'] or fare!=row['fare'] or raw[-1]!=0x56:raise ValueError('Ville ou tarif divergent')
    left=encode('Vers '+city,profile);right=encode(str(fare)+' $',profile)
    return left+padding(f['font']['row_width']-width(left+right,profile,f),profile,f)+right

def body(e,profile,f):
    return encode(e['fr'],profile) if e['kind']=='text' else b''.join(b'\x19\x02'+row_bytes(r,profile,f)+b'\x02' for r in e['rows'])

def copy_bytes(e,profile,f):return body(e,profile,f)+b'\x0a'+pointer(int(e['end'],16))

def fixtures_from_baselines(source,bases,priors):
    if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
    targets=sorted(set(pointer_index(source))|set().union(*(set(pointer_index(d)) for d in bases.values())))
    reserves=free_reserves(source,bases,priors,targets);free=[r[:] for r in reserves];edits=[];contexts={}
    config=json.loads((ROOT/'tools/v55/candidates_v55.json').read_text());font={k:v for k,v in config.items() if k!='entries'};font['profiles']={}
    for p,data in bases.items():
        q=int.from_bytes(data[0x3F054:0x3F058],'little')-0xC00000
        font['profiles'][p]={'offset':f'{q:06X}','widths_hex':data[q:q+128].hex()}
    f={'font':font}
    for c in json.loads((ROOT/'tools/v55/candidates_v55.json').read_text())['entries']:
        a,z=int(c['offset'],16),int(c['end'],16);e=dict(c);e['profiles']={}
        i=bisect.bisect_right(targets,a)
        if z-a<5 or i<len(targets) and targets[i]<a+5:raise ValueError('Entrée intérieure écrasée')
        e['interior_targets']=[f'{t:06X}' for t in targets[i:bisect.bisect_left(targets,z)]]
        for p,data in bases.items():
            expected=data[a:z]
            if c['kind']=='fares' and expected!=b''.join(b'\x19\x02'+bytes.fromhex(r['source_hex'])+b'\x02' for r in c['rows']):raise ValueError('Définitions source divergentes')
            e['profiles'][p]={'baseline_hex':expected.hex()}
            for root in c['contexts']:
                r=int(root,16);parsed=parse(data,r,8192,extra_glyphs=range(0xB0,0xC0))
                if parsed['error'] or not parsed['terminal'] or not r<=a<z<=parsed['end']:raise ValueError('Contexte de menu non fermé')
                spans=spans_fr(data[r:parsed['end']])
                if c['kind']=='text':
                    if (a-r,z-r) not in spans:raise ValueError('Frontière texte invalide')
                else:
                    if (a+2-r,z-1-r) not in spans:raise ValueError('Frontière choix invalide')
                record={'end':f"{parsed['end']:06X}",'baseline_hex':data[r:parsed['end']].hex()}
                if root in contexts and p in contexts[root] and contexts[root][p]!=record:raise ValueError('Contextes concurrents')
                contexts.setdefault(root,{})[p]=record
        edits.append(e)
    for e in sorted(edits,key=lambda e:(-max(len(copy_bytes(e,p,f)) for p in bases),e['offset'])):
        size=max(len(copy_bytes(e,p,f)) for p in bases)
        for region in free:
            if region[1]-region[0]>=size:
                e['copy_offset']=f'{region[0]:06X}';e['capacity']=size;region[0]=(region[0]+size+3)&~3;break
        else:raise ValueError('Réserve épuisée')
    return {'font':font,'version':'v55','base':'v54','edits':edits,'contexts':contexts,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves]}

def additions_from_fixtures(f,profile):
    changes=[]
    for e in f['edits']:
        a,z,d=int(e['offset'],16),int(e['end'],16),int(e['copy_offset'],16)
        baseline=bytes.fromhex(e['profiles'][profile]['baseline_hex'])
        if len(baseline)!=z-a:raise ValueError('Capacité source divergente')
        if e['kind']=='fares' and baseline!=b''.join(b'\x19\x02'+bytes.fromhex(r['source_hex'])+b'\x02' for r in e['rows']):raise ValueError('Capacité source divergente')
        if z-a<5 or any(a<int(t,16)<a+5 for t in e['interior_targets']):raise ValueError('Entrée intérieure écrasée')
        raw=copy_bytes(e,profile,f)
        if len(raw)>e['capacity']:raise ValueError('Traduction trop longue')
        if not any(int(lo,16)<=d and d+e['capacity']<=int(hi,16) for lo,hi in f['reserves']):raise ValueError('Copie hors réserve')
        changes.extend(((a,b'\x0a'+pointer(d)),(d,raw)))
    ranges=sorted((a,a+len(v)) for a,v in changes)
    if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Écritures en chevauchement')
    return changes

def logical_context(target,f,root,profile):
    a=int(root,16);z=int(f['contexts'][root][profile]['end'],16);cursor=a;out=bytearray()
    for e in sorted(f['edits'],key=lambda e:int(e['offset'],16)):
        lo,hi=int(e['offset'],16),int(e['end'],16)
        if not a<=lo<hi<=z:continue
        d=int(e['copy_offset'],16);raw=copy_bytes(e,profile,f)
        if target[lo:lo+5]!=b'\x0a'+pointer(d) or target[d:d+len(raw)]!=raw:raise ValueError('Trajet de menu invalide')
        if target[lo+5:hi]!=bytes.fromhex(e['profiles'][profile]['baseline_hex'])[5:]:raise ValueError('Entrée intérieure modifiée')
        out.extend(target[cursor:lo]);out.extend(body(e,profile,f));cursor=hi
    out.extend(target[cursor:z]);return bytes(out)

def build(rom,out):
    source=Path(rom).read_bytes();oldplan=json.loads((ROOT/'tools/v54/validation_v54.json').read_text())
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v54_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=oldplan['profiles'][p]['sha256'] for p,v in priors.items()):raise ValueError('IPS V54 divergent')
    bases={p:apply(source,records(v)) for p,v in priors.items()};f=fixtures_from_baselines(source,bases,priors);out=Path(out);out.mkdir(parents=True,exist_ok=True);profiles={}
    for p,base in bases.items():
        changes=additions_from_fixtures(f,p);ips=append(priors[p],changes);target=apply(source,records(ips))
        if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
        for e in f['edits']:
            d=int(e['copy_offset'],16)
            if base[d:d+e['capacity']]!=bytes(e['capacity']):raise ValueError('Réserve occupée')
            raw=copy_bytes(e,p,f);parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
            if parsed['error'] or not parsed['terminal'] or parsed['end']!=len(raw) or parsed['targets']!=[int(e['end'],16)]:raise ValueError('Copie de menu invalide')
        for root,c in f['contexts'].items():
            if commands(logical_context(target,f,root,p))!=commands(bytes.fromhex(c[p]['baseline_hex'])):raise ValueError('Commandes du contexte modifiées')
        (out/f'EarthBound_Beginnings_FR_v55_{p}.ips').write_bytes(ips)
        profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p]))}
    plan={'version':'v55','source_sha256':sha(source),'fare_rows_localized':16,'fare_definition_blocks':16,'ticket_offices':4,'optional_youngtown_rows':3,'new_dialogue_fragments':2,'city_names_and_fares_preserved':True,'row_advance_pixels':128,'shared_font_modified':False,'natural_scene_access_verified':False,'profiles':profiles}
    for name,data in (('v55_fixtures',f),('validation_v55',plan)):(ROOT/f'tools/v55/{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return plan
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
