"""V29: coordinate all three boy/girl calls, preserving original aliases."""
import argparse
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
sys.path.insert(0,str(ROOT/'tools/boy_girl'))
from build_v19 import ROM_SHA,SIZE,encode,sha,records,apply,append,pointer_index
from audit_boy_girl import START,GIRL,END,RAW,CALLERS
BASE_SHA={'accents':'3db0607030f931d5acb020fa7b9f9d6af8d157099bb958a887192edef005fbd9',
          'ascii':'60a70dc688b491c5574d01e86856c3e06646545d46e1838183791ea6c50df7f5'}
RESERVE=(0x3FF990,0x3FF9E0) # Inside the established legacy reservation.
ROUTINES={0x3FF990:('garçon','fille'),0x3FF9B0:('un écolier','une écolière')}
DESTINATIONS={0x33FAA8:0x3FF990,0x33FC1F:0x3FF990,0x352FE6:0x3FF9B0}
# Offset, fixed source length, observed V28 text (padded), coordinated French.
TEXTS=[(0x33FA8C,27,'Oh, quel charmant','Oh, tu es adorable, brave '),
       (0x33FC11,13,'Quel brave','Bravo, brave '),
       (0x33FC23,9,' tu fais!','!'),
       (0x352FD5,16,'You are a school','Tu es donc bien '),
       (0x352FED,12," aren't you?",' pas vrai?')]

def pointer(offset):return (offset+0xC00000).to_bytes(4,'little')

def routine(offset,boy,girl,profile):
    male=encode(boy,profile)+b'\x02'
    return RAW[:7]+pointer(offset+11+len(male))+male+encode(girl,profile)+b'\x02'

def additions(profile):
    out=[(p,routine(p,*words,profile)) for p,words in ROUTINES.items()]
    out += [(p,pointer(target)) for p,target in DESTINATIONS.items()]
    for p,n,old,new in TEXTS:
        raw=encode(new,profile)
        if len(raw)>n:raise ValueError('French exceeds fixed text span')
        out.append((p,raw.ljust(n,b'\x50')))
    return out

def audit(original,baseline,prior,profile):
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('Original USA 1.2 required')
    if sha(prior)!=BASE_SHA[profile]:raise ValueError('V28 IPS hash differs')
    if original[START:END]!=RAW or baseline[START:END]!=RAW:raise ValueError('Source routine changed')
    refs=pointer_index(baseline)
    if refs.get(START)!=list(CALLERS) or refs.get(GIRL)!=[START+7]:raise ValueError('Caller set changed')
    if any(refs.get(p) for p in range(START+1,END) if p!=GIRL):raise ValueError('Unknown interior alias')
    a,b=RESERVE
    if original[a:b]!=bytes(b-a) or baseline[a:b]!=bytes(b-a):raise ValueError('Reservation is not free')
    if any(a<=p<b for p in refs):raise ValueError('Reservation already referenced')
    if any(p<b and p+len(raw)>a for p,raw in records(prior)):raise ValueError('Reservation occupied by IPS')
    for p in CALLERS:
        if baseline[p-1:p+4]!=b'\x08'+pointer(START):raise ValueError('Call altered')
    for p,n,old,new in TEXTS:
        if baseline[p:p+n]!=encode(old,profile).ljust(n,b'\x50'):raise ValueError(f'Context altered: {p:06X}')
    spans=sorted((p,p+len(raw)) for p,raw in additions(profile))
    if any(b>c for (a,b),(c,d) in zip(spans,spans[1:])):raise ValueError('Additions overlap')
    for p,words in ROUTINES.items():
        if not a<=p<p+len(routine(p,*words,profile))<=b:raise ValueError('Routine outside reservation')

def build(rom_path,out):
    original=Path(rom_path).read_bytes();out=Path(out);out.mkdir(parents=True,exist_ok=True)
    results={}
    for profile in ('accents','ascii'):
        prior=(ROOT/f'patches/EarthBound_Beginnings_FR_v28_{profile}.ips').read_bytes()
        baseline=apply(original,records(prior));audit(original,baseline,prior,profile)
        extra=additions(profile);ips=append(prior,extra);target=apply(original,records(ips))
        if target!=apply(baseline,extra) or records(ips)!=records(prior)+extra:raise ValueError('IPS roundtrip differs')
        mask=bytearray(SIZE)
        for p,raw in extra:mask[p:p+len(raw)]=b'\1'*len(raw)
        if any(x!=y for x,y,m in zip(baseline,target,mask) if not m):raise ValueError('Change outside approved ranges')
        if target[START:END]!=RAW:raise ValueError('Original aliases damaged')
        (out/f'EarthBound_Beginnings_FR_v29_{profile}.ips').write_bytes(ips)
        results[profile]={'sha256':sha(ips),'target_rom_sha256':sha(target),'additions':len(extra),
            'rom_roundtrip':True,'outside_approved_ranges_unchanged':True,'original_routine_preserved':True}
    report={'base':'V28','source_sha256':sha(original),'profiles':results,
        'reservation':[f'{p:06X}' for p in RESERVE],
        'routines':[{'offset':f'{p:06X}','boy':w[0],'girl':w[1]} for p,w in ROUTINES.items()],
        'calls':[{'pointer':f'{p:06X}','target':f'{t:06X}'} for p,t in DESTINATIONS.items()],
        'text_spans':[{'offset':f'{p:06X}','length':n,'fr':new} for p,n,old,new in TEXTS],
        'native_boy_girl_emulator_tested':False}
    (ROOT/'tools/v29/validation_v29.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--out',type=Path,default=ROOT/'patches');args=ap.parse_args()
    print(json.dumps(build(args.rom,args.out),ensure_ascii=False,indent=2))
