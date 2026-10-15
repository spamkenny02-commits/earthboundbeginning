"""Relocate untouched dialogue and narrative scripts from the V40 baseline."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/v19'),str(ROOT/'tools/v33'),str(ROOT/'atelier/outils')]
from build_v19 import ROM_SHA, SIZE, sha, records, apply, append, pointer_index
from build_v33 import pointer, transform
from extraire import parse, render, length

BASE_SHA = {'accents': '62fd07a316cdb00ac7116d5e24e8ea13367baab966602bc00e1b0df351d52744', 'ascii': 'b5e4ecf92ca8b858c19aff03a4981fc638ac22e9518d32a43b7a9dda0b7dcaeb'}
ACTION_START, ACTION_END, ACTION_STRIDE = 0x368211, 0x369549, 12
RESERVES = ((0x257BA0,0x258000),(0x2599C0,0x259D10),(0x25A3A0,0x25A630),
            (0x25ADA0,0x25B1F0),(0x25B220,0x25B420),(0x25D1C0,0x25D3E0),
            (0x32F3F0,0x32F700),(0x32F710,0x32F8F0),(0x32D820,0x32DA10),
            (0x252C10,0x252E40),(0x251A50,0x251BF0),(0x252470,0x252610),
            (0x32E250,0x32E400),(0x32CF30,0x32D0C0),(0x32B020,0x32B1A0))


def reference_proof(data,q,target):
    if data[q:q+4] != pointer(target):
        raise ValueError('Pointeur source divergent')
    if ACTION_START+4 <= q < ACTION_END and (q-ACTION_START-4)%ACTION_STRIDE == 0:
        record=q-4
        asm=int.from_bytes(data[record+8:record+12],'little')
        if not (asm==0 or 0xC00000<=asm<0x1000000):
            raise ValueError('Enregistrement de combat incorrect')
        return {'kind':'battle_action_description','record':f'{record:06X}',
                'record_hex':data[record:record+12].hex()}
    # Recognize the actual command holding the operand, not an arbitrary
    # earlier parse which might encounter the same reference later.
    for start in range(max(0,q-40),q):
        if data[start] not in (6,8,9,10,0x1A,0x1B,0x1F):
            continue
        try:
            n=length(data,start)
        except (ValueError,IndexError):
            continue
        if not start<q or q+4>start+n:
            continue
        parsed=parse(data,start,8192,extra_glyphs=range(0xB0,0xC0))
        if not parsed['error'] and parsed['terminal'] and (q,target) in parsed['refs']:
            return {'kind':'parsed_command_operand','command':f'{start:06X}',
                    'command_hex':data[start:start+n].hex()}
    raise ValueError(f'Référence non prouvée: {q:06X} -> {target:06X}')


def fixtures_from_baselines(original,baselines):
    translations=json.loads((ROOT/'tools/v41/translations_v41.json').read_text())
    if len(translations)!=108:
        raise ValueError('Inventaire V41 incorrect')
    indexes={p:pointer_index(b) for p,b in baselines.items()}
    scripts=[]
    for ident,french in sorted(translations.items()):
        start=int(ident,16);parsed=parse(original,start,8192)
        if parsed['error'] or not parsed['terminal'] or not parsed['spans']:
            raise ValueError('Script source non clos: '+ident)
        end=parsed['end'];spans=[[a-start,b-start] for a,b in parsed['spans']]
        if len(spans)!=len(french):
            raise ValueError('Nombre de fragments divergent: '+ident)
        for b in baselines.values():
            if b[start:end]!=original[start:end]:
                raise ValueError('Script déjà modifié: '+ident)
        if not indexes['accents'].get(start):
            raise ValueError('Entrée sans référence: '+ident)
        refs=[]
        for target in sorted(t for t in indexes['accents'] if start<=t<end):
            if indexes['accents'][target]!=indexes['ascii'].get(target):
                raise ValueError('Références divergentes entre profils')
            for q in indexes['accents'][target]:
                proofs=[reference_proof(b,q,target) for b in baselines.values()]
                if proofs[0]!=proofs[1]:raise ValueError('Preuves divergentes')
                refs.append({'offset':f'{q:06X}','target':f'{target:06X}','proof':proofs[0]})
        scripts.append({'id':ident,'end':f'{end:06X}',
                        'english':[render(original[a:b]) for a,b in parsed['spans']],
                        'fr':french,'spans':spans,'original_hex':original[start:end].hex(),
                        'references':refs})
    ranges=sorted((int(e['id'],16),int(e['end'],16)) for e in scripts)
    if any(b>c for (_,b),(c,_) in zip(ranges,ranges[1:])):
        raise ValueError('Chevauchement de sources')
    return {'version':'v41','base':'v40','scripts':scripts}


def additions_from_fixtures(fixtures,profile):
    built=[];mapping={};region=0;cursor=RESERVES[0][0]
    for e in fixtures['scripts']:
        raw=bytes.fromhex(e['original_hex'])
        out,local=transform(raw,e['spans'],e['fr'],cursor,profile)
        while cursor+len(out)>RESERVES[region][1]:
            region+=1
            if region>=len(RESERVES):raise ValueError('Réserves épuisées')
            cursor=RESERVES[region][0]
        for a,b in local.items():mapping[int(e['id'],16)+a]=cursor+b
        built.append((e,cursor,out,local));cursor=(cursor+len(out)+3)&~3
    ranges=[(int(e['id'],16),int(e['end'],16)) for e in fixtures['scripts']]
    changes=[];moved=[];rewritten=[]
    for e,dest,out,local in built:
        source=bytes.fromhex(e['original_hex']);parsed=parse(source,0,len(source)+1)
        adjusted=[]
        for q,target in parsed['refs']:
            if any(a<=target<b for a,b in ranges):
                if target not in mapping:raise ValueError('Saut dans du texte redimensionné')
                at=local[q];out[at:at+4]=pointer(mapping[target])
                adjusted.append({'offset':f'{dest+at:06X}','old_target':f'{target:06X}',
                                 'new_target':f'{mapping[target]:06X}'})
        check=parse(bytes(out),0,len(out)+1,extra_glyphs=range(0xB0,0xC0))
        if check['error'] or not check['terminal'] or check['end']!=len(out):
            raise ValueError('Copie française non close: '+e['id'])
        allowed={q for r in adjusted for q in range(int(r['offset'],16)-dest,int(r['offset'],16)-dest+4)}
        textual={q for a,b in e['spans'] for q in range(a,b)}
        for q,byte in enumerate(source):
            if q not in textual and local[q] not in allowed and out[local[q]]!=byte:
                raise ValueError('Commande altérée')
        changes.append((dest,bytes(out)))
        moved.append({'id':e['id'],'offset':f'{dest:06X}','old_length':len(source),
                      'new_length':len(out),'internal_refs':adjusted})
        for ref in e['references']:
            q,target=int(ref['offset'],16),int(ref['target'],16)
            if any(a<=q<b for a,b in ranges):continue
            if target not in mapping:raise ValueError('Alias au milieu du texte')
            changes.append((q,pointer(mapping[target])))
            rewritten.append({'offset':ref['offset'],'old_target':ref['target'],
                              'new_target':f'{mapping[target]:06X}','proof':ref['proof']})
    writes=sorted((p,p+len(b)) for p,b in changes)
    if any(b>c for (_,b),(c,_) in zip(writes,writes[1:])):
        raise ValueError('Écritures V41 en chevauchement')
    return changes,moved,rewritten


def build(rom_path,out):
    original=Path(rom_path).read_bytes()
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('ROM USA 1.2 originale requise')
    original_refs=pointer_index(original);priors={};baselines={}
    for profile in ('accents','ascii'):
        prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v40_{profile}.ips').read_bytes()
        if sha(prior)!=BASE_SHA[profile]:raise ValueError('IPS V40 divergent')
        rec=records(prior);baseline=apply(original,rec);refs=pointer_index(baseline)
        for a,b in RESERVES:
            if original[a:b]!=bytes(b-a) or baseline[a:b]!=bytes(b-a):raise ValueError('Réserve non nulle')
            if any(a<=t<b for t in original_refs) or any(a<=t<b for t in refs):raise ValueError('Réserve ciblée')
            if any(p<b and p+len(raw)>a for p,raw in rec):raise ValueError('Collision avec V40')
        priors[profile]=prior;baselines[profile]=baseline
    fixtures=fixtures_from_baselines(original,baselines);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    results={};layouts=[]
    for profile,baseline in baselines.items():
        changes,moved,rewritten=additions_from_fixtures(fixtures,profile)
        old=records(priors[profile]);ips=append(priors[profile],changes);target=apply(original,records(ips))
        if records(ips)!=old+changes or target!=apply(baseline,changes):raise ValueError('IPS non autonome')
        # Calls from older relocated scripts may legitimately need a new
        # destination. Only proven four-byte reference operands may supersede
        # prior records; all other prior bytes remain unchanged.
        pointer_mask=bytearray(SIZE)
        for ref in rewritten:
            q=int(ref['offset'],16);pointer_mask[q:q+4]=b'\1'*4
        for p,raw in old:
            if any(target[q]!=baseline[q] and not pointer_mask[q] for q in range(p,p+len(raw))):
                raise ValueError('Régression hors opérandes prouvés V40')
        mask=bytearray(SIZE)
        for p,raw in changes:mask[p:p+len(raw)]=b'\1'*len(raw)
        if any(a!=b for a,b,m in zip(baseline,target,mask) if not m):raise ValueError('Écriture hors plages')
        for e in fixtures['scripts']:
            a,b=int(e['id'],16),int(e['end'],16)
            if target[a:b]!=baseline[a:b]:raise ValueError('Script source altéré')
        (out/f'EarthBound_Beginnings_FR_v41_{profile}.ips').write_bytes(ips)
        layouts.append([(e['id'],e['offset'],e['new_length']) for e in moved])
        results[profile]={'sha256':sha(ips),'target_rom_sha256':sha(target),
                         'prior_records_preserved':len(old),'records_added':len(changes),
                         'relocated':moved,'external_refs_rewritten':rewritten,
                         'rom_roundtrip':True,'source_scripts_preserved':True,
                         'outside_declared_ranges_unchanged':True,
                         'prior_record_pointer_updates':[r for r in rewritten if any(p<=int(r['offset'],16) and int(r['offset'],16)+4<=p+len(raw) for p,raw in old)]}
    if layouts[0]!=layouts[1]:raise ValueError('Implantations divergentes')
    (ROOT/'tools/v41/v41_dialogues_fr.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    changed=[(en,fr) for e in fixtures['scripts'] for en,fr in zip(e['english'],e['fr']) if en!=fr]
    report={'base':'V40','source_sha256':sha(original),'scripts_revised':len(fixtures['scripts']),
            'text_spans_in_copies':sum(len(e['fr']) for e in fixtures['scripts']),
            'newly_translated_fragments':sum(any(c.isalpha() for c in fr) for _,fr in changed),
            'grammatical_fragments_removed':sum(not any(c.isalpha() for c in fr) for _,fr in changed),
            'already_french_fragments':0,
            'distinct_new_english_fragments':len({en for en,fr in changed if any(c.isalpha() for c in fr)}),
            'dialogue_yes_no_choices_deferred_to_menu_pass':sum(fr in ('Yes','No') for e in fixtures['scripts'] for fr in e['fr']),'reservations':[[f'{a:06X}',f'{b:06X}'] for a,b in RESERVES],
            'profiles':results,'new_scenes_naturally_emulator_tested':False}
    (ROOT/'tools/v41/validation_v41.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');args=ap.parse_args()
    result=build(args.rom,args.out);print(json.dumps({k:v for k,v in result.items() if k!='profiles'},ensure_ascii=False,indent=2))
