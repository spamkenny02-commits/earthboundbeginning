"""Temporary native display probes for five V34 parent scripts.

The hook is not part of the release IPS and does not claim to exercise the
normal narrative or transaction trigger.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/v19'))
from build_v19 import apply, records, sha

def pointer(offset):
    return (offset + 0xC00000).to_bytes(4, 'little')

ap = argparse.ArgumentParser()
ap.add_argument('--rom', type=Path, required=True)
ap.add_argument('--core', type=Path, required=True)
ap.add_argument('--replay-out', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()

source = args.rom.read_bytes()
history = json.loads((ROOT/'tests/emulation_v18_work/accents_history.json').read_text())
scripts = ('33F009', '34EC37', '364E88', '36A6E3', '37B70A')
results = []
for profile in ('accents', 'ascii'):
    base = apply(source, records((ROOT/f'patches/EarthBound_Beginnings_FR_v34_{profile}.ips').read_bytes()))
    state = args.replay_out/profile/'after_combat.state'
    for ident in scripts:
        dest = int(ident, 16)
        out = (args.out/(profile+'_'+ident)).resolve()
        out.mkdir(parents=True, exist_ok=True)
        test = bytearray(base)
        test[0x07C588:0x07C58D] = b'\x0A' + pointer(dest)
        rom = out/'probe.sfc'
        rom.write_bytes(test)
        proc = subprocess.Popen([
            sys.executable, str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),
            '--core', str(args.core), '--rom', str(rom), '--out', str(out)
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
           stderr=open(out/'stderr.log', 'w'), text=True)

        def response():
            while True:
                line = proc.stdout.readline()
                if not line:
                    raise RuntimeError('Core ended before response')
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    pass

        ready = response()
        def send(command):
            proc.stdin.write(json.dumps(command)+'\n')
            proc.stdin.flush()
            return response()

        send({'load': str(state.resolve()), 'frame': history[254]['response']['frame']})
        for item in history[255:290]:
            command = dict(item['command'])
            command.pop('screenshot', None)
            command.pop('save', None)
            if 'load' in command:
                command['load'] = str((args.replay_out/profile/Path(command['load']).name).resolve())
            send(command)
        shots = [send({'frames': 240, 'screenshot': 'page_0'})]
        for index in range(1, 4):
            send({'frames': 2, 'buttons': ['A']})
            shots.append(send({'frames': 160, 'screenshot': 'page_'+str(index)}))
        send({'quit': True})
        proc.wait(timeout=10)
        rom.unlink()
        results.append({
            'profile': profile, 'script': ident, 'destination': ident,
            'base_sha256': sha(base), 'probe_sha256': sha(test),
            'hook': '07C588', 'hook_hex': bytes(test[0x07C588:0x07C58D]).hex(),
            'screens': [{'file': profile+'_'+ident+'/page_'+str(i)+'.png',
                         'sha256_rgb': shot['image']['sha256_rgb']}
                        for i, shot in enumerate(shots)],
            'returncode': proc.returncode,
            'temporary_entry_point': True,
            'native_story_trigger_tested': False,
        })
        print(profile, ident, proc.returncode, flush=True)

args.out.mkdir(parents=True, exist_ok=True)
(args.out/'results.json').write_text(json.dumps({
    'core_sha256': hashlib.sha256(args.core.read_bytes()).hexdigest(),
    'results': results,
}, indent=2)+'\n')
if any(row['returncode'] != 0 for row in results):
    raise SystemExit('Probe failed')
