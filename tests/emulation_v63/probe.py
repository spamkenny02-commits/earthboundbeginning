"""Sample the live text stack during normal controller-driven inventory/PSI use.
No routing patch, temporary ASM, cheats or direct WRAM writes.
"""
import argparse, collections, json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/v63'), str(ROOT/'tools/v62')]
import runtime as b
from live_text import BASE, TOP, prove, current_pointer
OPERATIONS = {
    'use_card': ('A','Right','A','A','A'),
    'eat_card': ('A','Right','A','A','Down','A'),
    'give_card_to_self': ('A','Right','A','A','Down','Down','A','A'),
    'drop_card': ('A','Right','A','A','Down','Down','Down','A'),
    'help_card': ('A','Right','A','A','Down','Down','Down','Down','A'),
    'help_card_description': ('A','Right','A','A','Down','Down','Down','Down','A','A'),
    'telepathy': ('A','Down','A','A','A'),
}
def run(args):
    source=args.rom.read_bytes(); assert b.sha(source)==b.ROM_SHA
    plan=json.loads((ROOT/'tools/v61/validation_v61.json').read_text())
    p=args.profile; ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes()
    assert b.sha(ips)==plan['profiles'][p]['sha256']
    data=b.apply(source,b.records(ips)); assert b.sha(data)==plan['profiles'][p]['target_rom_sha256']
    anchors=prove(source); assert anchors==prove(data)
    state=(args.states_dir/p/'after_combat.state').resolve()
    summary={'version':'v63','input_patch':'v61','profile':p,'rom_sha256':b.sha(data),'core_sha256':b.sha(args.core.read_bytes()),'initial_state_sha256':b.sha(state.read_bytes()),'engine_anchors':anchors,'rom_modified_for_probe':False,'wram_written_by_probe':False,'sampling':'top DISPLAY_TEXT state after each emulated frame; not instruction tracing','cases':{}}
    for name, keys in OPERATIONS.items():
        if args.case and name != args.case:continue
        out=(args.out/p/name).resolve(); out.mkdir(parents=True,exist_ok=True)
        rom=out/'fixture.sfc'; rom.write_bytes(data)
        with (out/'stderr.log').open('w') as err:
            proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(rom),'--core',str(args.core.resolve()),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
            def read():
                while True:
                    line=proc.stdout.readline()
                    if not line:raise RuntimeError('Emulator exited')
                    try:return json.loads(line)
                    except json.JSONDecodeError:pass
            def send(c):
                proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();return read()
            events=[];counts=collections.Counter();last=None;frames=0
            def advance(n,buttons=()):
                nonlocal frames,last
                for _ in range(n):
                    result=send({'frames':1,'buttons':list(buttons),'ram':{'offset':hex(BASE),'length':TOP+2-BASE}})
                    frames+=1;pointer=current_pointer(bytes.fromhex(result['ram_hex']))
                    if pointer:counts[pointer['rom_offset']]+=1
                    if pointer!=last:
                        events.append({'frame':result['frame'],'pointer':pointer});last=pointer
            try:
                ready=read();assert ready['source_sha256']==b.sha(data)
                send({'load':str(state),'frames':0});advance(60)
                for key in keys:advance(2,(key,));advance(12);advance(60)
                advance(150)
                capture=send({'screenshot':'response'})['image']
                send({'quit':True});proc.wait(timeout=10);assert proc.returncode==0
            finally:
                if proc.poll() is None:proc.kill();proc.wait()
                rom.unlink(missing_ok=True)
        summary['cases'][name]={'buttons':list(keys),'sampled_frames':frames,'events':events,'pointer_frame_counts':dict(sorted(counts.items())),'capture':capture,'returncode':proc.returncode}
        print(p,name,frames,'frames',len(counts),'pointers',flush=True)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/f'results_{p}.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
    ap.add_argument('--profile',choices=('accents','ascii'),required=True)
    ap.add_argument('--case',choices=OPERATIONS)
    run(ap.parse_args())
