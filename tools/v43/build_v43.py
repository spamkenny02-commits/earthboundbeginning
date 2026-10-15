"""Relocate remaining battle and service text, with optional dictionary expansion, from V42."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/v19'),str(ROOT/'tools/v33'),str(ROOT/'atelier/outils'),str(ROOT/'traduction')]
from build_v19 import ROM_SHA, SIZE, sha, records, apply, append, pointer_index
from build_v33 import pointer, transform
from extraire import parse, render, length
from compression import text_spans, expand

BASE_SHA = {'accents': '9d9a0b12736f6cf835194d9ca0c96a04c01e7d4a8eeac171a7fb693bc127cb39', 'ascii': 'b85b81a5c352bfc437577b601b40f95dc29a25d09e573b66338137decc467c1a'}
ACTION_START, ACTION_END, ACTION_STRIDE = 0x368211, 0x369549, 12
RESERVES = ((2699168, 2700144), (3334752, 3335152), (3321888, 3322272), (3322512, 3322896), (3329856, 3330240), (3318480, 3318848), (3335296, 3335664), (3340832, 3341200), (3329504, 3329808), (3329168, 3329456), (3337376, 3337664), (3328480, 3328752), (3334432, 3334704), (3336528, 3336800), (3323136, 3323392), (3279776, 3280000), (3338272, 3338496), (3340560, 3340784), (3341856, 3342064), (3319680, 3319872), (3325904, 3326096), (3338016, 3338208), (3338544, 3338736), (3341248, 3341440), (2488224, 2488400), (3328800, 3328976), (3338800, 3338976), (3341632, 3341808), (2487440, 2487600), (3278896, 3279056), (3337040, 3337200), (2488752, 2488896), (3322320, 3322464), (3336848, 3336992), (3337808, 3337952))
LEGACY_ACTION_START = 0x157B68
LEGACY_ACTION_END = LEGACY_ACTION_START + 410 * 12


def reference_proof_remake(data,q,target):
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


def reference_proof(data,q,target):
    if data[q:q+4] != pointer(target):raise ValueError('Pointeur source divergent')
    if LEGACY_ACTION_START+4 <= q < LEGACY_ACTION_END and (q-LEGACY_ACTION_START-4)%12 == 0:
        record=q-4;asm=int.from_bytes(data[record+8:record+12],'little')
        if not (asm==0 or 0xC00000<=asm<0x1000000):raise ValueError('Ancienne action incorrecte')
        return {'kind':'legacy_battle_action_description','record':f'{record:06X}',
                'record_hex':data[record:record+12].hex()}
    return reference_proof_remake(data,q,target)


def dictionary_from_rom(original):
    dictionary={}
    for i in range(768):
        q=0x8CDED+4*i;p=int.from_bytes(original[q:q+4],'little')-0xC00000
        if not 0<=p<len(original):raise ValueError('Pointeur dictionnaire invalide')
        end=original.find(b'\0',p,min(p+512,len(original)))
        if end<0 or not all(0x50<=x<=0xAE for x in original[p:end]):
            raise ValueError('Entrée de dictionnaire invalide')
        dictionary[f'{0x15+i//256:02X} {i%256:02X}']={
            'offset':f'{p:06X}','pointer_offset':f'{q:06X}',
            'raw_hex':original[p:end].hex(),'text_en':render(original[p:end])}
    return dictionary


def fixtures_from_baselines(original,baselines):
    translations=json.loads((ROOT/'tools/v43/translations_v43.json').read_text())
    if len(translations)!=56:raise ValueError('Inventaire V43 incorrect')
    dictionary=dictionary_from_rom(original);used=set()
    indexes={p:pointer_index(b) for p,b in baselines.items()};scripts=[]
    for ident,french in sorted(translations.items()):
        start=int(ident,16);parsed=parse(original,start,8192)
        if parsed['error'] or not parsed['terminal']:raise ValueError('Source non close: '+ident)
        end=parsed['end'];raw=original[start:end];spans=[list(span) for span in text_spans(raw)]
        if len(spans)!=len(french):raise ValueError('Fragments divergents: '+ident)
        for b in baselines.values():
            if b[start:end]!=raw:raise ValueError('Source déjà modifiée: '+ident)
        english=[expand(raw[a:b],dictionary) for a,b in spans]
        local_used=set()
        for a,b in spans:
            p=a
            while p<b:
                if raw[p] in (0x15,0x16,0x17):local_used.add(raw[p:p+2].hex(' ').upper());p+=2
                else:p+=1
        used.update(local_used);refs=[];held=[]
        if not indexes['accents'].get(start):raise ValueError('Aucun appel: '+ident)
        for target in sorted(t for t in indexes['accents'] if start<=t<end):
            if indexes['accents'][target]!=indexes['ascii'].get(target):raise ValueError('Références de profils divergentes')
            for q in indexes['accents'][target]:
                try:proof=reference_proof(baselines['accents'],q,target)
                except ValueError:
                    held.append({'offset':f'{q:06X}','target':f'{target:06X}',
                                 'raw_hex':baselines['accents'][q:q+4].hex()})
                    continue
                if proof!=reference_proof(baselines['ascii'],q,target):raise ValueError('Preuves divergentes')
                refs.append({'offset':f'{q:06X}','target':f'{target:06X}','proof':proof})
        if not any(r['target']==ident for r in refs):
            raise ValueError('Aucun appel prouvé: '+ident)
        scripts.append({'id':ident,'end':f'{end:06X}','english':english,'fr':french,
                        'spans':spans,'original_hex':raw.hex(),'dictionary_codes':sorted(local_used),
                        'references':refs,'preserved_unproven_refs':held})
    ranges=sorted((int(e['id'],16),int(e['end'],16)) for e in scripts)
    if any(b>c for (_,b),(c,_) in zip(ranges,ranges[1:])):raise ValueError('Sources en chevauchement')
    subset={code:dictionary[code] for code in sorted(used)}
    for word in subset.values():
        p,q=int(word['offset'],16),int(word['pointer_offset'],16);raw=bytes.fromhex(word['raw_hex'])
        for b in baselines.values():
            if b[p:p+len(raw)+1]!=original[p:p+len(raw)+1] or b[q:q+4]!=original[q:q+4]:
                raise ValueError('Dictionnaire antérieur modifié')
    return {'version':'v43','base':'v42','dictionary':subset,'scripts':scripts}


def additions_from_fixtures(fixtures,profile):
    built=[];mapping={};region=0;cursor=RESERVES[0][0]
    # Allocate the longest copy first so short scripts cannot exhaust its only hole.
    ordered=sorted(fixtures['scripts'],key=lambda e:len(transform(bytes.fromhex(e['original_hex']),e['spans'],e['fr'],0,profile)[0]),reverse=True)
    for e in ordered:
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
        raise ValueError('Écritures V43 en chevauchement')
    return changes,moved,rewritten


def build(rom_path,out):
    original=Path(rom_path).read_bytes()
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('ROM USA 1.2 originale requise')
    original_refs=pointer_index(original);priors={};baselines={}
    for profile in ('accents','ascii'):
        prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v42_{profile}.ips').read_bytes()
        if sha(prior)!=BASE_SHA[profile]:raise ValueError('IPS V42 divergent')
        rec=records(prior);baseline=apply(original,rec);refs=pointer_index(baseline)
        for a,b in RESERVES:
            if original[a:b]!=bytes(b-a) or baseline[a:b]!=bytes(b-a):raise ValueError('Réserve non nulle')
            if any(a<=t<b for t in original_refs) or any(a<=t<b for t in refs):raise ValueError('Réserve ciblée')
            if any(p<b and p+len(raw)>a for p,raw in rec):raise ValueError('Collision avec V42')
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
                raise ValueError('Régression hors opérandes prouvés V42')
        mask=bytearray(SIZE)
        for p,raw in changes:mask[p:p+len(raw)]=b'\1'*len(raw)
        if any(a!=b for a,b,m in zip(baseline,target,mask) if not m):raise ValueError('Écriture hors plages')
        for e in fixtures['scripts']:
            a,b=int(e['id'],16),int(e['end'],16)
            if target[a:b]!=baseline[a:b]:raise ValueError('Script source altéré')
        (out/f'EarthBound_Beginnings_FR_v43_{profile}.ips').write_bytes(ips)
        layouts.append([(e['id'],e['offset'],e['new_length']) for e in moved])
        results[profile]={'sha256':sha(ips),'target_rom_sha256':sha(target),
                         'prior_records_preserved':len(old),'records_added':len(changes),
                         'relocated':moved,'external_refs_rewritten':rewritten,
                         'rom_roundtrip':True,'source_scripts_preserved':True,
                         'outside_declared_ranges_unchanged':True,
                         'prior_record_pointer_updates':[r for r in rewritten if any(p<=int(r['offset'],16) and int(r['offset'],16)+4<=p+len(raw) for p,raw in old)]}
    if layouts[0]!=layouts[1]:raise ValueError('Implantations divergentes')
    for profile,baseline in baselines.items():
        target=apply(original,records((out/f'EarthBound_Beginnings_FR_v43_{profile}.ips').read_bytes()))
        for e in fixtures['scripts']:
            for ref in e['preserved_unproven_refs']:
                q=int(ref['offset'],16)
                if target[q:q+4]!=baseline[q:q+4]:raise ValueError('Référence non prouvée altérée')
    (ROOT/'tools/v43/v43_dialogues_fr.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    changed=[(en,fr) for e in fixtures['scripts'] for en,fr in zip(e['english'],e['fr']) if en!=fr]
    report={'base':'V42','source_sha256':sha(original),'scripts_revised':len(fixtures['scripts']),
            'text_spans_in_copies':sum(len(e['fr']) for e in fixtures['scripts']),
            'newly_translated_fragments':sum(any(c.isalpha() for c in fr) for _,fr in changed),
            'nonlexical_fragments_adjusted':sum(not any(c.isalpha() for c in fr) for _,fr in changed),
            'already_french_fragments':0,
            'dictionary_entries_expanded':len(fixtures['dictionary']),
            'shared_dictionary_modified':False,
            'unproven_references_preserved':sum(len(e['preserved_unproven_refs']) for e in fixtures['scripts']),
            'distinct_new_english_fragments':len({en for en,fr in changed if any(c.isalpha() for c in fr)}),
            'dialogue_yes_no_choices_deferred_to_menu_pass':sum(fr in ('Yes','No') for e in fixtures['scripts'] for fr in e['fr']),'reservations':[[f'{a:06X}',f'{b:06X}'] for a,b in RESERVES],
            'profiles':results,'new_scenes_naturally_emulator_tested':False}
    (ROOT/'tools/v43/validation_v43.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');args=ap.parse_args()
    result=build(args.rom,args.out);print(json.dumps({k:v for k,v in result.items() if k!='profiles'},ensure_ascii=False,indent=2))
