"""Relocate three guarded NPC dialogues using engine-validated table fields.

No interior reference is rewritten. The original NPC scripts remain intact.
An unrelated short item-confirmation prefix uses the existing two-jump method.
"""
import argparse,bisect,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v52'))
from build_v52 import ROM_SHA,SIZE,sha,records,apply,append,pointer_index,parse,encode,dictionary_from_rom,decode,spans_fr,pointer,commands

def engine_table_proof(data,config):
    expected=int(config['npc_table_offset'],16)+0xC00000;proof=[]
    for e in config['engine_references']:
        a=int(e['offset'],16)
        if e['kind']=='asm':
            raw=data[a:a+10]
            if not (len(raw)==10 and raw[0] in (0xA9,0xA2,0xA0) and raw[3] in (0x85,0x86,0x84) and raw[5] in (0xA9,0xA2,0xA0) and raw[8] in (0x85,0x86,0x84) and raw[4]+2==raw[9]):raise ValueError('Structure ASM divergente')
            dest=int.from_bytes(raw[1:3]+raw[6:8],'little')
        elif e['kind']=='xl':
            raw=data[a:a+4]
            if len(raw)!=4 or raw[0]&15!=15:raise ValueError('Structure XL divergente')
            dest=int.from_bytes(raw[1:4],'little')
        else:raise ValueError('Type de référence inconnu')
        if dest!=expected:raise ValueError('Table NPC divergente')
        proof.append({**e,'raw_hex':raw.hex(),'table_snes':f'{dest:06X}'})
    if len(proof)!=10:raise ValueError('Dix références moteur requises')
    return proof

def npc_field_proof(data,slot,target,config):
    base=int(config['npc_table_offset'],16);stride=config['record_size']
    if stride!=17 or config['text_fields']!=[9,13]:raise ValueError('Schéma NPC divergent')
    for field in config['text_fields']:
        row,rem=divmod(slot-base-field,stride)
        if row>=0 and rem==0:break
    else:raise ValueError('Hors champ texte NPC')
    a=base+row*stride;raw=data[a:a+stride]
    if len(raw)!=17 or raw[0]>3 or raw[3]>7 or raw[8]>2:raise ValueError('Enregistrement NPC invalide')
    if data[slot:slot+4]!=pointer(target):raise ValueError('Destination NPC divergente')
    return {'row_index':row,'record_offset':f'{a:06X}','field_offset':field,'record_hex':raw.hex()}

def free_reserves(source,bases,priors,targets):
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
    return sorted(reserves,key=lambda r:r[1]-r[0],reverse=True)

def copy_bytes(e,profile):
    raw=bytes.fromhex(e['profiles'][profile]['baseline_hex']);lo,hi=e['span'];text=encode(e['fr'],profile)
    out=raw[:lo]+text+raw[hi:]
    if e['mode']=='text_jump':out+=b'\x0a'+pointer(int(e['end'],16))
    else:
        p=parse(out,0,len(out)+1,extra_glyphs=range(0xB0,0xC0))
        if p['error'] or not p['terminal'] or p['end']!=len(out):raise ValueError('Copie NPC non fermée')
    return out

def fixtures_from_baselines(source,bases,priors):
    if len(source)!=SIZE or sha(source)!=ROM_SHA:raise ValueError('ROM originale USA 1.2 requise')
    config=json.loads((ROOT/'tools/v53/candidates_v53.json').read_text());engine=engine_table_proof(source,config)
    if any(engine_table_proof(d,config)!=engine for d in bases.values()):raise ValueError('Moteur antérieur modifié')
    indexes={p:pointer_index(d) for p,d in bases.items()};original_index=pointer_index(source)
    targets=sorted(set(original_index)|set().union(*(set(x) for x in indexes.values())))
    reserves=free_reserves(source,bases,priors,targets);free=[r[:] for r in reserves];edits=[];dictionary=dictionary_from_rom(source)
    for c in config['entries']:
        a=int(c['id'],16);e=dict(c);e['profiles']={}
        for p,data in bases.items():
            if c['mode']=='npc_copy':
                parsed=parse(data,a,8192,extra_glyphs=range(0xB0,0xC0));z=parsed['end']
                if parsed['error'] or not parsed['terminal']:raise ValueError('Source NPC non fermée')
                # This lot needs no internal pointer remapping. Exclusive-end
                # targets deliberately stay at the original continuation.
                if any(a<=t<z for q,t in parsed['refs']):raise ValueError('Branche intérieure non prise en charge')
                proof=npc_field_proof(data,int(c['slot'],16),a,config)
                if p=='accents':e['npc_field_proof']=proof
                elif proof!=e['npc_field_proof']:raise ValueError('Profils NPC divergents')
                raw=data[a:z];span=spans_fr(raw)[0]
            elif c['mode']=='text_jump':
                z=int(c['end'],16);root=int(c['context'],16);parsed=parse(data,root,8192,extra_glyphs=range(0xB0,0xC0))
                if parsed['error'] or (a-root,z-root) not in spans_fr(data[root:parsed['end']]):raise ValueError('Frontière textuelle invalide')
                raw=data[a:z];span=(0,z-a);i=bisect.bisect_right(targets,a)
                if z-a<5 or i<len(targets) and targets[i]<a+5:raise ValueError('Entrée intérieure écrasée')
                e['context_end']=f"{parsed['end']:06X}"
            else:raise ValueError('Mode inconnu')
            allowed=bytearray(z-a)
            for update in c['prior_pointer_updates']:
                q,old,new=int(update['offset'],16),int(update['old_target'],16),int(update['new_target'],16)
                historical=json.loads((ROOT/f"tools/v{update['version']}/validation_v{update['version']}.json").read_text())
                refs=historical['profiles'][p]['entry_refs_rewritten']
                if not any(r['offset']==update['offset'] and r['old_target']==update['old_target'] and r['new_target']==update['new_target'] for r in refs):raise ValueError('Mise à jour historique non prouvée')
                original_parse=parse(source,a,8192,extra_glyphs=range(0xB0,0xC0))
                if not a<=q<q+4<=z or (q,old) not in original_parse['refs'] or (q,new) not in parsed['refs'] or data[q:q+4]!=pointer(new):raise ValueError('Opérande historique divergent')
                allowed[q-a:q-a+4]=b'\1'*4
            if any(x!=y and not m for x,y,m in zip(data[a:z],source[a:z],allowed)):raise ValueError('Source déjà modifiée')
            if p=='accents':e['end']=f'{z:06X}';e['span']=list(span)
            elif e['end']!=f'{z:06X}' or e['span']!=list(span):raise ValueError('Implantations sources divergentes')
            e['profiles'][p]={'baseline_hex':raw.hex(),'english':decode(raw[span[0]:span[1]],dictionary)}
        z=int(e['end'],16);e['preserved_interior_refs']=[{'target':f'{t:06X}','sites':[f'{q:06X}' for q in sorted(set(original_index.get(t,[]))|set().union(*(set(x.get(t,[])) for x in indexes.values())))]} for t in targets if a<t<z]
        if c['mode']=='npc_copy':e['other_start_ref_sites']=[f'{q:06X}' for q in sorted(set().union(*(set(x.get(a,[])) for x in indexes.values()))-{int(c['slot'],16)})]
        edits.append(e)
    for e in sorted(edits,key=lambda e:-max(len(copy_bytes(e,p)) for p in bases)):
        size=max(len(copy_bytes(e,p)) for p in bases)
        for region in free:
            if region[1]-region[0]>=size:
                e['copy_offset']=f'{region[0]:06X}';e['capacity']=size;region[0]=(region[0]+size+3)&~3;break
        else:raise ValueError('Réserve épuisée')
    return {'version':'v53','base':'v52','config':config,'engine_proof':engine,'edits':edits,'reserves':[[f'{a:06X}',f'{z:06X}'] for a,z in reserves]}

def additions_from_fixtures(f,profile):
    changes=[]
    for e in f['edits']:
        a,z,d=int(e['id'],16),int(e['end'],16),int(e['copy_offset'],16);raw=copy_bytes(e,profile)
        if len(bytes.fromhex(e['profiles'][profile]['baseline_hex']))!=z-a:raise ValueError('Capacité source divergente')
        if len(raw)>e['capacity']:raise ValueError('Traduction trop longue')
        if not any(int(lo,16)<=d and d+e['capacity']<=int(hi,16) for lo,hi in f['reserves']):raise ValueError('Copie hors réserve')
        if e['mode']=='npc_copy':
            npc_field_proof_from_fixture=e['npc_field_proof'];q=int(e['slot'],16)
            if int(npc_field_proof_from_fixture['record_offset'],16)+npc_field_proof_from_fixture['field_offset']!=q or npc_field_proof_from_fixture['field_offset'] not in (9,13):raise ValueError('Champ NPC divergent')
            changes.append((q,pointer(d)))
        else:
            if z-a<5 or any(a<int(r['target'],16)<a+5 for r in e['preserved_interior_refs']):raise ValueError('Entrée intérieure écrasée')
            changes.append((a,b'\x0a'+pointer(d)))
        changes.append((d,raw))
    ranges=sorted((a,a+len(v)) for a,v in changes)
    if any(z>a for (_,z),(a,_) in zip(ranges,ranges[1:])):raise ValueError('Écritures en chevauchement')
    return changes

def build(rom,out):
    source=Path(rom).read_bytes();oldplan=json.loads((ROOT/'tools/v52/validation_v52.json').read_text())
    priors={p:(ROOT/f'patches/EarthBound_Beginnings_FR_v52_{p}.ips').read_bytes() for p in ('accents','ascii')}
    if any(sha(v)!=oldplan['profiles'][p]['sha256'] for p,v in priors.items()):raise ValueError('IPS V52 divergent')
    bases={p:apply(source,records(v)) for p,v in priors.items()};f=fixtures_from_baselines(source,bases,priors);out=Path(out);out.mkdir(parents=True,exist_ok=True);profiles={}
    for p,base in bases.items():
        changes=additions_from_fixtures(f,p);ips=append(priors[p],changes);target=apply(source,records(ips))
        if target!=apply(base,changes) or records(ips)!=records(priors[p])+changes:raise ValueError('IPS non autonome')
        for e in f['edits']:
            a,z,d=int(e['id'],16),int(e['end'],16),int(e['copy_offset'],16)
            if base[d:d+e['capacity']]!=bytes(e['capacity']):raise ValueError('Réserve occupée')
            if e['mode']=='npc_copy':
                if target[a:z]!=base[a:z]:raise ValueError('Source NPC altérée')
                if commands(copy_bytes(e,p))!=commands(base[a:z]):raise ValueError('Commandes NPC altérées')
        (out/f'EarthBound_Beginnings_FR_v53_{p}.ips').write_bytes(ips)
        profiles[p]={'sha256':sha(ips),'target_rom_sha256':sha(target),'records_added':len(changes),'prior_records_preserved':len(records(priors[p]))}
    plan={'version':'v53','source_sha256':sha(source),'new_text_fragments':len(f['edits']),'npc_copies':3,'npc_table_fields_rewritten':3,'text_entry_jumps':1,'engine_references_verified':len(f['engine_proof']),'shared_dictionary_modified':False,'natural_scene_access_verified':False,'profiles':profiles}
    for name,data in (('v53_fixtures',f),('validation_v53',plan)):(ROOT/f'tools/v53/{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return plan
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');a=ap.parse_args();print(json.dumps(build(a.rom,a.out),indent=2))
