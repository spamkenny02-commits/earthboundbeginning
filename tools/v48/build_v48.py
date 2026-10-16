"""Relocate 40 messages and four private grammar helpers from V47."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/v19'),str(ROOT/'tools/v33'),str(ROOT/'atelier/outils'),str(ROOT/'traduction')]
from build_v19 import ROM_SHA, SIZE, sha, records, apply, append, pointer_index
from build_v33 import pointer, transform
from build_v19 import encode
from extraire import parse, render, length
from compression import text_spans, expand

BASE_SHA = {'accents': '4ca8fb5d031ff1a54da81bdb7e01a6cfe01982b36df7ebb7363cce850b95ec73', 'ascii': '7aee36235ebd8e6fae420bee4bc97ba0a335bf265e11be605d238bcea68f7cf0'}
ACTION_START, ACTION_END, ACTION_STRIDE = 0x368211, 0x369549, 12
RESERVES = ((2488224, 2488400), (3337040, 3337200), (2488752, 2488896), (3322320, 3322464), (3336848, 3336992), (3337808, 3337952), (3338352, 3338496), (3325728, 3325856), (2434016, 2434128), (2476448, 2476560), (3278944, 3279056), (3279360, 3279472), (3326208, 3326320), (3336368, 3336480), (2431872, 2431968), (2432016, 2432112), (2453392, 2453488), (2459760, 2459856), (2462832, 2462928), (2465424, 2465520), (2467984, 2468080), (2482128, 2482224), (3279120, 3279216), (3279632, 3279728), (3334256, 3334352), (3341488, 3341584), (3342192, 3342288), (2432512, 2432592), (2432704, 2432784), (2432864, 2432944), (2473408, 2473488), (3278240, 3278320), (3280160, 3280240), (3314448, 3314528), (3317696, 3317776), (3319440, 3319520), (2458224, 2458288), (2462640, 2462704), (2465680, 2465744), (3277744, 3277808), (3280544, 3280608), (3319568, 3319632), (3323024, 3323088), (3326032, 3326096), (3327056, 3327120), (3329056, 3329120), (3335600, 3335664), (2435232, 2435280), (2435904, 2435952), (2436000, 2436048), (2470880, 2470928), (2487552, 2487600), (2489760, 2489808), (3279520, 3279568), (3313184, 3313232), (3325632, 3325680), (3327168, 3327216), (3328192, 3328240), (3335200, 3335248), (3337712, 3337760), (3339088, 3339136), (2430384, 2430416), (2430512, 2430544), (2430896, 2430928), (2435760, 2435792), (2436624, 2436656), (2441296, 2441328), (2445776, 2445808), (2446000, 2446032), (2447024, 2447056), (2447248, 2447280), (2451920, 2451952), (2452144, 2452176), (2452400, 2452432), (2452656, 2452688), (2452912, 2452944), (2453168, 2453200), (2454960, 2454992), (2455760, 2455792), (2455920, 2455952), (2458512, 2458544), (2459600, 2459632), (2460048, 2460080), (2463120, 2463152), (2465968, 2466000), (2466224, 2466256), (2466480, 2466512), (2468528, 2468560), (2468784, 2468816), (2469040, 2469072), (2476240, 2476272), (2479888, 2479920), (2480080, 2480112), (2480272, 2480304), (2485552, 2485584), (2487088, 2487120), (2487856, 2487888), (2489680, 2489712), (2490192, 2490224), (3279280, 3279312), (3280416, 3280448), (3280800, 3280832), (3320000, 3320032), (3322944, 3322976), (3328336, 3328368), (3329424, 3329456), (3329776, 3329808), (3338704, 3338736), (3339184, 3339216))
PRIVATE_HELPERS = {'07E5F3','07E5FE','07E6C5','07E6D1'}
EXISTING_HELPERS = {0x07E602:0x320BB8,0x07E74E:0x32C02C}
TOUCHUPS=((0x356262,0x3561C5),(0x3562B3,0x356270))
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
    translations=json.loads((ROOT/'tools/v48/translations_v48.json').read_text())
    if len(translations)!=44:raise ValueError('Inventaire V48 incorrect')
    dictionary=dictionary_from_rom(original);used=set()
    indexes={p:pointer_index(b) for p,b in baselines.items()};scripts=[]
    for ident,french in sorted(translations.items()):
        start=int(ident,16);parsed=parse(original,start,8192)
        if parsed['error'] or not parsed['terminal']:raise ValueError('Source non close: '+ident)
        end=parsed['end'];raw=original[start:end];spans=[list(span) for span in text_spans(raw)]
        if len(spans)!=len(french):raise ValueError('Fragments divergents: '+ident)
        baseline_raw=baselines['accents'][start:end]
        if baseline_raw!=baselines['ascii'][start:end]:raise ValueError('Source de profils divergente')
        # A mixed source may already contain proven V47 pointer updates.
        # Keep those operands in the new copy and reject any other difference.
        allowed=bytearray(len(raw));source_updates=[]
        for q,t in parsed['refs']:
            if baseline_raw[q-start:q-start+4]==pointer(t):continue
            new=int.from_bytes(baseline_raw[q-start:q-start+4],'little')-0xC00000
            if not 0<=new<SIZE:raise ValueError('Pointeur antérieur invalide')
            proof=reference_proof(baselines['accents'],q,new)
            allowed[q-start:q-start+4]=b'\1'*4
            source_updates.append({'offset':f'{q:06X}','old_target':f'{t:06X}','new_target':f'{new:06X}','proof':proof})
        if any(a!=b and not m for a,b,m in zip(raw,baseline_raw,allowed)):
            raise ValueError('Source déjà traduite ou commande altérée: '+ident)
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
        helper_refs=[]
        if ident in PRIVATE_HELPERS:
            # Keep the global English entry points unchanged. Only relocated
            # scripts in this lot call these private French copies.
            helper_refs=[{'offset':r['offset'],'target':r['target'],'raw_hex':baselines['accents'][int(r['offset'],16):int(r['offset'],16)+4].hex()} for r in refs]+held
            refs=[];held=[]
        if ident not in PRIVATE_HELPERS and not any(r['target']==ident for r in refs):
            raise ValueError('Aucun appel prouvé: '+ident)
        scripts.append({'id':ident,'end':f'{end:06X}','english':english,'fr':french,
                        'spans':spans,'original_hex':raw.hex(),'baseline_hex':baseline_raw.hex(),
                        'source_pointer_updates_preserved':source_updates,'dictionary_codes':sorted(local_used),
                        'references':refs,'preserved_unproven_refs':held,
                        'private_helper':ident in PRIVATE_HELPERS,'preserved_original_helper_refs':helper_refs})
    ranges=sorted((int(e['id'],16),int(e['end'],16)) for e in scripts)
    if any(b>c for (_,b),(c,_) in zip(ranges,ranges[1:])):raise ValueError('Sources en chevauchement')
    subset={code:dictionary[code] for code in sorted(used)}
    for word in subset.values():
        p,q=int(word['offset'],16),int(word['pointer_offset'],16);raw=bytes.fromhex(word['raw_hex'])
        for b in baselines.values():
            if b[p:p+len(raw)+1]!=original[p:p+len(raw)+1] or b[q:q+4]!=original[q:q+4]:
                raise ValueError('Dictionnaire antérieur modifié')
    touchups=[]
    for q,root in TOUCHUPS:
        for data in baselines.values():
            parsed=parse(data,root,8192,extra_glyphs=range(0xB0,0xC0))
            if parsed['error'] or not parsed['terminal'] or (q,q+7) not in parsed['spans'] or data[q:q+7]!=b'\x70\x71\x9e\xa9\x9f\x9e\x95':raise ValueError('Contexte Anyone divergent')
        touchups.append({'offset':f'{q:06X}','root':f'{root:06X}','old':'@Anyone','fr':'@Chacun'})
    return {'version':'v48','base':'v47','dictionary':subset,'scripts':scripts,'touchups':touchups,
            'prior_pointer_repairs':{p:[] for p in baselines}}


def additions_from_fixtures(fixtures,profile):
    built=[];mapping=dict(EXISTING_HELPERS);cursors=[a for a,_ in RESERVES]
    # Allocate the longest copy first so short scripts cannot exhaust its only hole.
    ordered=sorted(fixtures['scripts'],key=lambda e:len(transform(bytes.fromhex(e.get('baseline_hex',e['original_hex'])),e['spans'],e['fr'],0,profile)[0]),reverse=True)
    for e in ordered:
        raw=bytes.fromhex(e.get('baseline_hex',e['original_hex']))
        out,local=transform(raw,e['spans'],e['fr'],0,profile)
        region=next((i for i,(_,end) in enumerate(RESERVES) if cursors[i]+len(out)<=end),None)
        if region is None:raise ValueError('Réserves épuisées')
        cursor=cursors[region]
        cursors[region]=(cursor+len(out)+3)&~3
        for a,b in local.items():
            # A script's exclusive end may be the next script's entry point.
            # It must never overwrite that entry when allocation reorders copies.
            if a<len(raw):mapping[int(e['id'],16)+a]=cursor+b
        built.append((e,cursor,out,local))
    ranges=[(int(e['id'],16),int(e['end'],16)) for e in fixtures['scripts']]
    changes=[];moved=[];rewritten=[]
    for e,dest,out,local in built:
        source=bytes.fromhex(e.get('baseline_hex',e['original_hex']));parsed=parse(source,0,len(source)+1)
        adjusted=[]
        for q,target in parsed['refs']:
            if target in EXISTING_HELPERS or any(a<=target<b for a,b in ranges):
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
            if target not in mapping:raise ValueError(f'Alias au milieu du texte: {e["id"]} {q:06X} -> {target:06X}')
            changes.append((q,pointer(mapping[target])))
            rewritten.append({'offset':ref['offset'],'old_target':ref['target'],
                              'new_target':f'{mapping[target]:06X}','proof':ref['proof']})
    for repair in fixtures.get('prior_pointer_repairs',{}).get(profile,[]):
        changes.append((int(repair['offset'],16),pointer(int(repair['new_target'],16))))
    changes.extend((int(e['offset'],16),encode(e['fr'],profile)) for e in fixtures.get('touchups',[]))
    writes=sorted((p,p+len(b)) for p,b in changes)
    if any(b>c for (_,b),(c,_) in zip(writes,writes[1:])):
        raise ValueError('Écritures V48 en chevauchement')
    return changes,moved,rewritten


def build(rom_path,out):
    original=Path(rom_path).read_bytes()
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('ROM USA 1.2 originale requise')
    original_refs=pointer_index(original);priors={};baselines={}
    for profile in ('accents','ascii'):
        prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v47_{profile}.ips').read_bytes()
        if sha(prior)!=BASE_SHA[profile]:raise ValueError('IPS V47 divergent')
        rec=records(prior);baseline=apply(original,rec);refs=pointer_index(baseline)
        for a,b in RESERVES:
            if original[a:b]!=bytes(b-a) or baseline[a:b]!=bytes(b-a):raise ValueError('Réserve non nulle')
            if any(a<=t<b for t in original_refs) or any(a<=t<b for t in refs):raise ValueError('Réserve ciblée')
            if any(p<b and p+len(raw)>a for p,raw in rec):raise ValueError('Collision avec V47')
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
        repairs=fixtures['prior_pointer_repairs'][profile]
        for ref in rewritten+repairs:
            q=int(ref['offset'],16);pointer_mask[q:q+4]=b'\1'*4
        for e in fixtures.get('touchups',[]):
            q=int(e['offset'],16);pointer_mask[q:q+len(encode(e['fr'],profile))]=b'\1'*len(encode(e['fr'],profile))
        for p,raw in old:
            if any(target[q]!=baseline[q] and not pointer_mask[q] for q in range(p,p+len(raw))):
                raise ValueError('Régression hors opérandes prouvés V47')
        mask=bytearray(SIZE)
        for p,raw in changes:mask[p:p+len(raw)]=b'\1'*len(raw)
        if any(a!=b for a,b,m in zip(baseline,target,mask) if not m):raise ValueError('Écriture hors plages')
        for e in fixtures['scripts']:
            a,b=int(e['id'],16),int(e['end'],16)
            if target[a:b]!=baseline[a:b]:raise ValueError('Script source altéré')
        (out/f'EarthBound_Beginnings_FR_v48_{profile}.ips').write_bytes(ips)
        layouts.append([(e['id'],e['offset'],e['new_length']) for e in moved])
        results[profile]={'sha256':sha(ips),'target_rom_sha256':sha(target),
                         'prior_records_preserved':len(old),'records_added':len(changes),
                         'relocated':moved,'external_refs_rewritten':rewritten,
                         'prior_pointer_repairs':repairs,
                         'rom_roundtrip':True,'source_scripts_preserved':True,
                         'outside_declared_ranges_unchanged':True,
                         'prior_record_pointer_updates':[r for r in rewritten+repairs if any(p<=int(r['offset'],16) and int(r['offset'],16)+4<=p+len(raw) for p,raw in old)]}
    if layouts[0]!=layouts[1]:raise ValueError('Implantations divergentes')
    for profile,baseline in baselines.items():
        target=apply(original,records((out/f'EarthBound_Beginnings_FR_v48_{profile}.ips').read_bytes()))
        for e in fixtures['scripts']:
            for ref in e['preserved_unproven_refs']+e['preserved_original_helper_refs']:
                q=int(ref['offset'],16)
                if target[q:q+4]!=baseline[q:q+4]:raise ValueError('Référence non prouvée altérée')
    (ROOT/'tools/v48/v48_dialogues_fr.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    changed=[(en,fr) for e in fixtures['scripts'] for en,fr in zip(e['english'],e['fr']) if en!=fr]
    report={'base':'V47','source_sha256':sha(original),'scripts_revised':len(fixtures['scripts']),
            'main_message_scripts':len(fixtures['scripts'])-len(PRIVATE_HELPERS),
            'context_touchups':len(fixtures['touchups']),
            'private_helper_scripts':len(PRIVATE_HELPERS),
            'text_spans_in_copies':sum(len(e['fr']) for e in fixtures['scripts']),
            'newly_translated_fragments':sum(sum(c.isalpha() for c in fr)>1 for _,fr in changed),
            'onomatopoeia_characters_adjusted':sum(sum(c.isalpha() for c in fr)==1 for _,fr in changed),
            'nonlexical_fragments_adjusted':sum(not any(c.isalpha() for c in fr) for _,fr in changed),
            'already_french_fragments':0,
            'dictionary_entries_expanded':len(fixtures['dictionary']),
            'shared_dictionary_modified':False,
            'unproven_references_preserved':sum(len(e['preserved_unproven_refs']) for e in fixtures['scripts']),
            'distinct_new_english_fragments':len({en for en,fr in changed if sum(c.isalpha() for c in fr)>1}),
            'dialogue_yes_no_choices_deferred_to_menu_pass':sum(fr in ('Yes','No') for e in fixtures['scripts'] for fr in e['fr']),'reservations':[[f'{a:06X}',f'{b:06X}'] for a,b in RESERVES],
            'profiles':results,'new_scenes_naturally_emulator_tested':False}
    (ROOT/'tools/v48/validation_v48.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,default=ROOT/'patches');args=ap.parse_args()
    result=build(args.rom,args.out);print(json.dumps({k:v for k,v in result.items() if k!='profiles'},ensure_ascii=False,indent=2))
