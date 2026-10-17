"""Replay normal V18 gameplay against both V56 profiles."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/v19"))
from build_v19 import apply, records

parser = argparse.ArgumentParser()
parser.add_argument("--rom", type=Path, required=True)
parser.add_argument("--core", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
source = args.rom.read_bytes()
summary = {"core_sha256": hashlib.sha256(args.core.read_bytes()).hexdigest(), "profiles": {}}
for profile in ("accents", "ascii"):
    out = (args.out / profile).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = apply(source, records((ROOT / f"patches/EarthBound_Beginnings_FR_v56_{profile}.ips").read_bytes()))
    rom = out / "test.sfc"
    rom.write_bytes(target)
    history = json.loads((ROOT / f"tests/emulation_v18_work/{profile}_history.json").read_text())
    with (out / "stderr.log").open("w") as errors:
        proc = subprocess.Popen([
            sys.executable, str(ROOT / "tests/emulation_v18_work/libretro_runner.py"),
            "--core", str(args.core), "--rom", str(rom), "--out", str(out),
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors, text=True)

        def response():
            while True:
                line = proc.stdout.readline()
                if not line:
                    raise RuntimeError("Arrêt prématuré du coeur")
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    pass

        ready = response()
        replay = []
        for item in history:
            command = dict(item["command"])
            if "load" in command:
                command["load"] = str(out / Path(command["load"]).name)
            proc.stdin.write(json.dumps(command) + "\n")
            proc.stdin.flush()
            replay.append({"command": command, "response": response()})
        proc.stdin.write('{"quit":true}\n')
        proc.stdin.flush()
        response()
        proc.wait(timeout=10)
    rom.unlink()
    old = {x["command"]["screenshot"]: x["response"]["image"]["sha256_rgb"]
           for x in history if "screenshot" in x["command"]}
    new = {x["command"]["screenshot"]: x["response"]["image"]["sha256_rgb"]
           for x in replay if "screenshot" in x["command"]}
    changed = [name for name, value in new.items() if old.get(name) != value]
    stable = {k: old[k] == new[k] for k in
              ("title_final", "intro", "after_combat", "state_restored", "game_menu")}
    summary["profiles"][profile] = {
        "ready": ready, "commands_replayed": len(replay),
        "last_frame": replay[-1]["response"]["frame"],
        "screens_changed_from_v18": changed, "stable_screens": stable,
        "returncode": proc.returncode,
    }
    print(profile, summary["profiles"][profile], flush=True)
(args.out / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
if not all(p["returncode"] == 0 and all(p["stable_screens"].values()) and
           p["screens_changed_from_v18"] == ["battle_step_30", "battle_step_31", "battle_step_32"]
           for p in summary["profiles"].values()):
    raise SystemExit("Régression visuelle")
