"""Relocate closed dialogue scripts while keeping original aliases intact."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
sys.path.insert(0,str(ROOT/'traduction'))
sys.path.insert(0,str(ROOT/'atelier/outils'))
from build_v19 import ROM_SHA,SIZE,sha,encode,records,append,apply,pointer_index
from extraire import parse
from layout_v33 import decode_layout
from audit_v33 import commands_preserved,BASE_SHA
RESERVES=((0x258DC0,0x259400),(0x25C210,0x25C820),(0x32B620,0x32BC20),(0x228820,0x228D60),(0x32D530,0x32DA20))

def pointer(p):return (p+0xC00000).to_bytes(4,'little')

def transform(raw,spans,french,destination,profile):
    """Only text changes size; every original command byte gets a mapped offset."""
    if len(spans)!=len(french):raise ValueError('Translation span count differs')
    out=bytearray();mapping={};previous=0
    for (a,b),fr in zip(spans,french):
        if not previous<=a<b<=len(raw):raise ValueError('Invalid source spans')
        for q in range(previous,a):mapping[q]=len(out)+q-previous
        out.extend(raw[previous:a]);mapping[a]=len(out)
        out.extend(encode(fr,profile));mapping[b]=len(out);previous=b
    for q in range(previous,len(raw)):mapping[q]=len(out)+q-previous
    out.extend(raw[previous:]);mapping[len(raw)]=len(out)
    return out,mapping

def build_from_fixtures(fixtures,profile):
    scripts=fixtures['scripts'];region=0;cursor=RESERVES[0][0];built=[];global_map={}
    for e in scripts:
        raw=bytes.fromhex(e['baseline_hex'][profile]);out,mapping=transform(raw,e['spans'],e['fr'],cursor,profile)
        if cursor+len(out)>RESERVES[region][1]:
            region+=1
            if region>=len(RESERVES):raise ValueError('Reservation exhausted')
            cursor=RESERVES[region][0]
            out,mapping=transform(raw,e['spans'],e['fr'],cursor,profile)
            if cursor+len(out)>RESERVES[region][1]:raise ValueError('Reservation exhausted')
        start=int(e['id'],16)
        for old,new in mapping.items():global_map[start+old]=cursor+new
        built.append((e,cursor,out,mapping));cursor=(cursor+len(out)+15)&~15
    changes=[];relocated=[];rewritten=[]
    ranges=[(int(e['id'],16),int(e['end'],16)) for e in scripts]
    for e,dest,out,mapping in built:
        start=int(e['id'],16);old=bytes.fromhex(e['baseline_hex'][profile])
        parsed=parse(old,0,len(old)+1,extra_glyphs=range(0xB0,0xC0))
        if parsed['error'] or not parsed['terminal'] or parsed['end']!=len(old):raise ValueError('Source script not closed')
        adjusted=[]
        for ref,target in parsed['refs']:
            if any(a<=target<b for a,b in ranges):
                if target not in global_map:raise ValueError('Branch into translated text interior')
                pos=mapping[ref];new=global_map[target];out[pos:pos+4]=pointer(new)
                adjusted.append({'offset':f'{dest+pos:06X}','old_target':f'{target:06X}','new_target':f'{new:06X}'})
        check=parse(bytes(out),0,len(out)+1,extra_glyphs=range(0xB0,0xC0))
        if check['error'] or not check['terminal'] or check['end']!=len(out):raise ValueError('Relocated script not closed')
        # Command sequences must match, except declared relocated pointer operands.
        allowed={q for r in adjusted for q in range(int(r['offset'],16)-dest,int(r['offset'],16)-dest+4)}
        textual={q for a,b in e['spans'] for q in range(a,b)}
        for q,byte in enumerate(old):
            if q not in textual and mapping[q] not in allowed and out[mapping[q]]!=byte:
                raise ValueError('Command changed')
        changes.append((dest,bytes(out)))
        relocated.append({'id':e['id'],'offset':f'{dest:06X}','old_length':len(old),'new_length':len(out),'internal_refs':adjusted})
        for ref in e['entry_refs']:
            ref=int(ref,16)
            if any(a<=ref<b for a,b in ranges+fixtures['protected_original_ranges']):continue # Original aliases remain intact.
            changes.append((ref,pointer(dest)));rewritten.append({'offset':f'{ref:06X}','old_target':e['id'],'new_target':f'{dest:06X}'})
    spans=sorted((p,p+len(raw)) for p,raw in changes)
    if any(b>c for (a,b),(c,d) in zip(spans,spans[1:])):raise ValueError('New writes overlap')
    return changes,relocated,rewritten,cursor

def fixtures_from_rom(original,baselines):
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('Original USA 1.2 required')
    french=json.loads((ROOT/'tools/v33/dialogues_fr.json').read_text())
    catalog={e['id']:e for e in json.loads((ROOT/'catalogue/catalogue.json').read_text())['entries'] if e['category']=='script'}
    original_refs=pointer_index(original);refs={p:pointer_index(b) for p,b in baselines.items()};scripts=[]
    protected=[];prior_refs={p:{} for p in baselines}
    for version in ('31','32'):
        old=json.loads((ROOT/f'tools/v{version}/v{version}_dialogues_fr.json').read_text())
        protected.extend([int(e['id'],16),int(e['end'],16)] for e in old['scripts'])
        plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text())
        for profile,baseline in baselines.items():
            for e in plan['profiles'][profile]['relocated']:
                start=int(e['offset'],16);raw=baseline[start:start+e['new_length']]
                parsed=parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
                if parsed['error'] or not parsed['terminal'] or parsed['end']!=len(raw):raise ValueError('Prior copy not closed')
                for q,target in parsed['refs']:prior_refs[profile].setdefault(target,[]).append(start+q)
    for ident,fr in french.items():
        start=int(ident,16);layout=decode_layout(original,start,catalog[ident]['english'])
        if not layout:raise ValueError('Source layout differs: '+ident)
        end,_,spans=layout
        if not original_refs.get(start):raise ValueError('Unreferenced entry')
        if len(fr)!=len(spans):raise ValueError('French span count: '+ident)
        expected={p:sorted(set(original_refs[start]+prior_refs[p].get(start,[]))) for p in baselines}
        if expected['accents']!=expected['ascii']:raise ValueError('Profile reference sets differ')
        for profile,b in baselines.items():
            if refs[profile].get(start)!=expected[profile]:raise ValueError('Entry reference set changed')
            if not commands_preserved(original,b,start,end,spans):raise ValueError('Baseline commands changed')
            for ref in original_refs[start]:
                if b[ref:ref+4]!=original[ref:ref+4]:raise ValueError('Entry already relocated')
        scripts.append({'id':ident,'end':f'{end:06X}','english_script':catalog[ident]['english'],
            'original_hex':original[start:end].hex(),'baseline_hex':{p:b[start:end].hex() for p,b in baselines.items()},
            'spans':[[a-start,b-start] for a,b in spans], 'fr':fr,
            'entry_refs':[f'{q:06X}' for q in expected['accents']],
            'verified_prior_copy_refs':[f'{q:06X}' for q in prior_refs['accents'].get(start,[])],
            'preserved_aliases':[{ 'offset':f'{q:06X}','target':f'{t:06X}'} for t,positions in refs['accents'].items()
                if start<t<end for q in positions]})
    ranges=sorted((int(e['id'],16),int(e['end'],16)) for e in scripts)
    if any(b>c for (a,b),(c,d) in zip(ranges,ranges[1:])):raise ValueError('Selected scripts overlap')
    return {'version':'v33','base':'v32','protected_original_ranges':protected,'scripts':scripts}

def build(rom_path,out):
    original=Path(rom_path).read_bytes()
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('Original USA 1.2 required')
    baselines={};priors={}
    for profile in ('accents','ascii'):
        ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v32_{profile}.ips').read_bytes()
        if sha(ips)!=BASE_SHA[profile]:raise ValueError('V32 IPS differs')
        baseline=apply(original,records(ips));refs=pointer_index(baseline)
        for a,b in RESERVES:
            if original[a:b]!=bytes(b-a) or baseline[a:b]!=bytes(b-a):raise ValueError('Reservation not empty')
            if any(a<=t<b for t in refs) or any(a<=t<b for t in pointer_index(original)):raise ValueError('Reservation already referenced')
            if any(p<b and p+len(raw)>a for p,raw in records(ips)):raise ValueError('Reservation occupied by IPS')
        baselines[profile]=baseline;priors[profile]=ips
    fixtures=fixtures_from_rom(original,baselines);out=Path(out);out.mkdir(parents=True,exist_ok=True);results={}
    for profile,baseline in baselines.items():
        extra,relocated,rewritten,cursor=build_from_fixtures(fixtures,profile)
        ips=append(priors[profile],extra);target=apply(original,records(ips));mask=bytearray(SIZE)
        for p,raw in extra:mask[p:p+len(raw)]=b'\1'*len(raw)
        if target!=apply(baseline,extra):raise ValueError('IPS roundtrip differs')
        if any(x!=y for x,y,m in zip(baseline,target,mask) if not m):raise ValueError('Write outside declared ranges')
        for e in fixtures['scripts']:
            s=int(e['id'],16);end=int(e['end'],16)
            if target[s:end]!=baseline[s:end]:raise ValueError('Original script aliases damaged')
        (out/f'EarthBound_Beginnings_FR_v33_{profile}.ips').write_bytes(ips)
        results[profile]={'sha256':sha(ips),'target_rom_sha256':sha(target),'additions':len(extra),
            'used_end':f'{cursor:06X}','rom_roundtrip':True,'original_scripts_preserved':True,
            'outside_declared_ranges_unchanged':True,'relocated':relocated,'entry_refs_rewritten':rewritten}
    (ROOT/'tools/v33/v33_dialogues_fr.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    report={'base':'V32','source_sha256':sha(original),'scripts':len(fixtures['scripts']),
        'text_spans':sum(len(e['fr']) for e in fixtures['scripts']), 'reservations':[[f'{p:06X}' for p in r] for r in RESERVES],
        'profiles':results,'new_scene_emulator_tested':False}
    (ROOT/'tools/v33/validation_v33.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--out',type=Path,default=ROOT/'patches');args=ap.parse_args()
    result=build(args.rom,args.out);print(json.dumps({k:v for k,v in result.items() if k!='profiles'},indent=2))
