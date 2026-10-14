"""Read-only verification of the shared boy/girl dialogue subroutine.

The branch probe models documented control-code semantics, not native CPU
execution. This module never modifies a ROM or generates a patch.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v19'))
from build_v19 import ROM_SHA,SIZE,ACCENTS,sha,records,apply,pointer_index,encode

START=0x387B05
GIRL=0x387B14
END=0x387B19
RAW=bytes.fromhex('19 10 01 0B 02 1B 03 14 7B F8 00 92 9F A9 02 97 99 A2 9C 02')
CALLERS={0x33FAA8:'charming',0x33FC1F:'brave',0x352FE6:'school'}
BASE_SHA={
    'accents':'ea0338dd99f8d85e7a8b91a8318bedb579d3acc9fac2b2d7cf3551f395fd31f4',
    'ascii':'274d6ea182e6b5426b06455d574cb75c4e332ce3817ee4812f548ecf33c1fbfd',
}
V27_SHA={
    'accents':'b48cbe0373f36408d545f8b0ad82e664725d0cf7877fb11c72668135593a27c6',
    'ascii':'298d3bb4c54b6f1db62e835e952a095b99f69aec80296d92b022092dbbe9011a',
}
CONTEXTS={
    'charming':[(0x33FA8C,27)],
    'brave':[(0x33FC11,13),(0x33FC23,9)],
    'school':[(0x352FD5,16),(0x352FED,12)],
}

def decode(raw):
    return ''.join(ACCENTS[x-0xb0] if 0xb0<=x<0xb0+len(ACCENTS) else chr(x-48) for x in raw).rstrip(' ')

def probe(data,character_id):
    """Model 19 10 selection result, 0B equality and 1B 03 true branch.

    The caller supplies the result of party selection. Party availability,
    unconscious characters and native runtime selection are not simulated.
    """
    if data[START:START+7]!=RAW[:7]:raise ValueError('Header differs')
    target=int.from_bytes(data[START+7:START+11],'little')-0xc00000
    p=target if character_id==data[START+4] else START+11
    out=bytearray()
    while p<END:
        if data[p]==2:return decode(out)
        if not 0x50<=data[p]<=0xaa:raise ValueError('Unexpected command in output')
        out.append(data[p]);p+=1
    raise ValueError('Output has no return')

def audit(rom_path):
    original=Path(rom_path).read_bytes()
    if len(original)!=SIZE or sha(original)!=ROM_SHA:raise ValueError('Original USA 1.2 required')
    if original[START:END]!=RAW:raise ValueError('Original routine differs')
    refs=pointer_index(original)
    if refs.get(START)!=list(CALLERS):raise ValueError('Unexpected incoming callers')
    if refs.get(GIRL)!=[START+7]:raise ValueError('Unexpected girl entry aliases')
    for p in range(START+1,END):
        if p!=GIRL and refs.get(p):raise ValueError('Unexpected interior pointer')
    profiles={}
    for version,profile in ((v,p) for v in ('v26','v27') for p in ('accents','ascii')):
        expected=BASE_SHA if version=='v26' else V27_SHA
        ips=(ROOT/f'patches/EarthBound_Beginnings_FR_{version}_{profile}.ips').read_bytes()
        if sha(ips)!=expected[profile]:raise ValueError('Published IPS differs')
        data=apply(original,records(ips))
        if data[START:END]!=RAW:raise ValueError('Published routine changed')
        calls=[]
        for p,scene in CALLERS.items():
            if original[p-1]!=8 or data[p-1:p+4]!=original[p-1:p+4]:
                raise ValueError('Call opcode or destination altered')
            texts=[{'offset':f'{a:06X}','text':decode(data[a:a+n]),'length':n} for a,n in CONTEXTS[scene]]
            calls.append({'pointer_offset':f'{p:06X}','scene':scene,'texts':texts})
        profiles[version+'_'+profile]={'routine_unchanged':True,'callers':calls,
            'modeled_outputs':{str(i):probe(data,i) for i in (1,2,3,4)}}
    return {'source_sha256':sha(original),'base':['V26','V27'],'routine_offset':f'{START:06X}',
        'routine_snes_address':'F87B05','length':END-START,'raw_hex':RAW.hex(' '),
        'girl_target':f'{GIRL:06X}','incoming_calls':len(CALLERS),'profiles':profiles,
        'french_lengths':{'garçon':len(encode('garçon','accents')),'fille':len(encode('fille','accents'))},
        'native_boy_girl_emulator_tested':False,'rom_modified':False,
        'semantics_reference':'https://github.com/jeffman/Mother2GbaTranslation/blob/master/tools/ScriptToolGui/m12-codelist.json'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--out',type=Path,default=ROOT/'tools/boy_girl/validation_boy_girl.json')
    a=ap.parse_args();result=audit(a.rom)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'incoming_calls':result['incoming_calls'],'profiles':list(result['profiles']),
        'native_boy_girl_emulator_tested':False},indent=2))
