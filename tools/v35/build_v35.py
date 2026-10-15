"""Build V35 by relocating complete V34 scripts with verified live references."""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/v19'), str(ROOT/'tools/v33'), str(ROOT/'tools/v34'), str(ROOT/'traduction'), str(ROOT/'atelier/outils')]
from build_v19 import ROM_SHA, SIZE, ACCENTS, sha, encode, records, append, apply, pointer_index
import build_v33
from build_v33 import build_from_fixtures
from layout_v33 import decode_layout
from audit_v34 import commands_preserved
from extraire import parse

BASE_SHA = {
    'accents': '699ac56104579b09a32652eb760402e7eaf84d70de2fa6dde26eba5dc208e9c4',
    'ascii': 'c8faf4467b35735b81ffdf209075d7f1a43bf89d11381be2e0bcbc28ad8f4e7f',
}
RESERVES = ((0x167800,0x168000),(0x16F800,0x170000),(0x177800,0x177FD0),(0x257BA0,0x258000))
build_v33.RESERVES = RESERVES

SCRIPTS = (
    '33C125','33C5A2','33C628','33D2AC','34A897','351BC6','351C42','351FFE',
    '352382','3528E1','353CC9','3540E9','3544C9','3545AC','3608E7','360A5B',
    '3618F0','3639EE','363AF4','36443B','36448A','3645E8','364FBE','36F4F6',
    '371E94','373D51','3770CF','37728F','380C03','3838F8','38535C',
)

# Only these source-verified residual English fragments are replaced. All other
# spans keep their V34 French text (or deliberate names/onomatopoeia) verbatim.
OVERRIDES = {
    '33C24B':'(Et toi?)',
    '33C5D7':"(Quelqu'un a-t-il trouvé le trésor enterré dans le parterre...)",
    '33C63E':" C'est un très bon os. Ouaf!)",
    '33D3C9':'Non', '34A8C6':'Non', '351C20':'Non,', '351C98':'Non,',
    '35203A':'Je suis sérieux.', '3523BA':'Non', '35292B':' mon pote.',
    '353D56':'Non', '3540FE':'Hé', '354568':'Non', '354653':'Non',
    '3608E8':'Bonjour,', '360A9F':'Non', '36194A':'Non', '363A11':'Non',
    '363B32':'Non', '364463':'Non', '3644AE':'Non', '3645E9':'Salut',
    '36501E':'Maison', '365025':' hantée!', '36F4F7':"D'accord.",
    '371ED1':'Non', '373D55':'Non,',
    '3770DF':"(Combien de temps pour arriver jusqu'ici?)",
    '377315':' gauche,', '380C04':"Oh! C'est", '3838F9':'Tu veux un',
    '38537C':' ton sang!',
}

def decode_text(data):
    out=[]
    for byte in data:
        if 0x50 <= byte <= 0xAA:
            out.append(chr(byte-48))
        elif 0xB0 <= byte < 0xB0+len(ACCENTS):
            out.append(ACCENTS[byte-0xB0])
        else:
            raise ValueError(f'Octet de texte inattendu: {byte:02X}')
    return ''.join(out).rstrip(' ')

def prior_copy_refs(baseline, profile):
    refs={}; protected=[]
    for version in ('31','32','33'):
        fixture=json.loads((ROOT/f'tools/v{version}/v{version}_dialogues_fr.json').read_text())
        protected.extend([int(e['id'],16),int(e['end'],16)] for e in fixture['scripts'])
        plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text())
        for e in plan['profiles'][profile]['relocated']:
            start=int(e['offset'],16); raw=baseline[start:start+e['new_length']]
            parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
            if parsed['error'] or not parsed['terminal'] or parsed['end']!=len(raw):
                raise ValueError(f'Copie V{version} non close: {start:06X}')
            for q,target in parsed['refs']:
                refs.setdefault(target,[]).append(start+q)
    return refs, protected

def make_fixtures(original, baselines):
    catalog={e['id']:e for e in json.loads((ROOT/'catalogue/catalogue.json').read_text())['entries'] if e['category']=='script'}
    original_refs=pointer_index(original); active_refs={p:pointer_index(b) for p,b in baselines.items()}
    prior={}; protected=[]
    for profile,baseline in baselines.items():
        prior[profile], ranges=prior_copy_refs(baseline,profile)
        if not protected: protected=ranges
        elif protected!=ranges: raise ValueError('Plages protégées divergentes')
    scripts=[]; seen_overrides=set()
    for ident in SCRIPTS:
        start=int(ident,16); layout=decode_layout(original,start,catalog[ident]['english'])
        if not layout: raise ValueError('Layout source invalide: '+ident)
        end,_,spans=layout
        if not original_refs.get(start): raise ValueError('Script sans appel: '+ident)
        expected={p:sorted(set(original_refs[start]+prior[p].get(start,[]))) for p in baselines}
        if expected['accents']!=expected['ascii']: raise ValueError('Références de profils divergentes: '+ident)
        for profile,baseline in baselines.items():
            if active_refs[profile].get(start)!=expected[profile]: raise ValueError('Références actives inattendues: '+ident)
            if not commands_preserved(original,baseline,start,end,spans): raise ValueError('Commandes modifiées: '+ident)
            for ref in original_refs[start]:
                if baseline[ref:ref+4]!=original[ref:ref+4]: raise ValueError('Entrée déjà relocalisée: '+ident)
        french=[]
        for a,b in spans:
            key=f'{a:06X}'
            current=decode_text(baselines['accents'][a:b])
            if encode(current,'ascii') != baselines['ascii'][a:b].rstrip(b'\x50'):
                raise ValueError('Texte V34 divergent entre profils: '+key)
            if key in OVERRIDES:
                if current.strip()!=decode_text(original[a:b]).strip(): raise ValueError('Résidu non anglais: '+key)
                current=OVERRIDES[key]; seen_overrides.add(key)
            french.append(current)
        scripts.append({'id':ident,'end':f'{end:06X}','english_script':catalog[ident]['english'],
            'original_hex':original[start:end].hex(),'baseline_hex':{p:b[start:end].hex() for p,b in baselines.items()},
            'spans':[[a-start,b-start] for a,b in spans],'fr':french,
            'entry_refs':[f'{q:06X}' for q in expected['accents']],
            'verified_prior_copy_refs':[f'{q:06X}' for q in prior['accents'].get(start,[])],
            'preserved_aliases':[]})
    if seen_overrides != set(OVERRIDES):
        raise ValueError('Remplacements non atteints: '+','.join(sorted(set(OVERRIDES)-seen_overrides)))
    ranges=sorted((int(e['id'],16),int(e['end'],16)) for e in scripts)
    if any(b>c for (_,b),(c,_) in zip(ranges,ranges[1:])): raise ValueError('Scripts sélectionnés en chevauchement')
    return {'version':'v35','base':'v34','protected_original_ranges':protected,'scripts':scripts}

def build(rom_path,out):
    original=Path(rom_path).read_bytes()
    if len(original)!=SIZE or sha(original)!=ROM_SHA: raise ValueError('ROM originale USA 1.2 requise')
    baselines={}; priors={}
    for profile in ('accents','ascii'):
        ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v34_{profile}.ips').read_bytes()
        if sha(ips)!=BASE_SHA[profile]: raise ValueError('IPS V34 non conforme: '+profile)
        baseline=apply(original,records(ips)); refs=pointer_index(baseline)
        for a,b in RESERVES:
            if original[a:b]!=bytes(b-a) or baseline[a:b]!=bytes(b-a): raise ValueError('Réserve non nulle')
            if any(a<=t<b for t in refs) or any(a<=t<b for t in pointer_index(original)): raise ValueError('Réserve référencée')
            if any(p<b and p+len(raw)>a for p,raw in records(ips)): raise ValueError('Réserve occupée par V34')
        baselines[profile]=baseline; priors[profile]=ips
    fixtures=make_fixtures(original,baselines); out=Path(out); out.mkdir(parents=True,exist_ok=True); results={}
    for profile,baseline in baselines.items():
        extra,relocated,rewritten,cursor=build_from_fixtures(fixtures,profile)
        ips=append(priors[profile],extra); target=apply(original,records(ips)); changed=bytearray(SIZE)
        for p,raw in extra: changed[p:p+len(raw)]=b'\1'*len(raw)
        if target!=apply(baseline,extra): raise ValueError('Application IPS divergente')
        if any(x!=y for x,y,m in zip(baseline,target,changed) if not m): raise ValueError('Écriture hors zones déclarées')
        for e in fixtures['scripts']:
            s=int(e['id'],16); z=int(e['end'],16)
            if target[s:z]!=baseline[s:z]: raise ValueError('Alias source endommagé')
        path=out/f'EarthBound_Beginnings_FR_v35_{profile}.ips'; path.write_bytes(ips)
        results[profile]={'sha256':sha(ips),'target_rom_sha256':sha(target),'additions':len(extra),
            'used_end':f'{cursor:06X}','rom_roundtrip':True,'original_scripts_preserved':True,
            'outside_declared_ranges_unchanged':True,'relocated':relocated,'entry_refs_rewritten':rewritten}
    (ROOT/'tools/v35/v35_dialogues_fr.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    already=sum(1 for e in fixtures['scripts'] for (a,b),fr in zip(e['spans'],e['fr'])
        if f'{int(e["id"],16)+a:06X}' not in OVERRIDES and
        decode_text(bytes.fromhex(e['baseline_hex']['accents'])[a:b]).strip()!=decode_text(bytes.fromhex(e['original_hex'])[a:b]).strip())
    report={'base':'V34','source_sha256':sha(original),'scripts_revised':len(fixtures['scripts']),
        'text_spans_in_copies':sum(len(e['fr']) for e in fixtures['scripts']),
        'newly_translated_fragments':len(OVERRIDES),'already_french_fragments':already,
        'unchanged_names_cries_or_punctuation':sum(len(e['fr']) for e in fixtures['scripts'])-len(OVERRIDES)-already,
        'reservations':[[f'{x:06X}' for x in r] for r in RESERVES],
        'profiles':results,'new_scene_emulator_tested':False}
    (ROOT/'tools/v35/validation_v35.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--rom',type=Path,required=True); ap.add_argument('--out',type=Path,default=ROOT/'patches')
    args=ap.parse_args(); print(json.dumps(build(args.rom,args.out),ensure_ascii=False,indent=2))
