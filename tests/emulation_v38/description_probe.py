"""Reach the first lamp battle normally, then select Voir in the battle menu."""
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
summary = {"method": "normal_gameplay_to_first_lamp_then_battle_menu_Voir",
           "temporary_entry_point": False,
           "core_sha256": hashlib.sha256(args.core.read_bytes()).hexdigest(),
           "profiles": {}}
for profile in ("accents", "ascii"):
    out = (args.out / profile).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = apply(source, records((ROOT / f"patches/EarthBound_Beginnings_FR_v38_{profile}.ips").read_bytes()))
    rom = out / "test.sfc"
    rom.write_bytes(target)
    history = json.loads((ROOT / f"tests/emulation_v18_work/{profile}_history.json").read_text())
    stop = next(i for i, item in enumerate(history)
                if item["command"].get("screenshot") == "battle_menu")
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

        def send(command):
            proc.stdin.write(json.dumps(command) + "\n")
            proc.stdin.flush()
            return response()

        for item in history[:stop + 1]:
            command = dict(item["command"])
            if "save" in command:
                command["save"] = str(out / (Path(command["save"]).name + ".state"))
            if "load" in command:
                command["load"] = str(out / Path(command["load"]).name)
            send(command)
        for command in (
            {"frames": 2, "buttons": ["Right"]},
            {"frames": 10, "screenshot": "lamp_menu_right"},
            {"frames": 2, "buttons": ["Down"]},
            {"frames": 10, "screenshot": "lamp_menu_parer"},
            {"frames": 2, "buttons": ["Right"]},
            {"frames": 10, "screenshot": "lamp_menu_voir"},
            {"frames": 2, "buttons": ["A"]},
            {"frames": 120, "screenshot": "lamp_description_1"},
            {"frames": 2, "buttons": ["A"]},
            {"frames": 120, "screenshot": "lamp_description_2"},
        ):
            last = send(command)
        send({"quit": True})
        proc.wait(timeout=10)
    rom.unlink()
    summary["profiles"][profile] = {
        "ready": ready, "commands_from_normal_history": stop + 1,
        "last_frame": last["frame"], "returncode": proc.returncode,
        "captures": ["lamp_menu_right.png", "lamp_menu_parer.png",
                     "lamp_menu_voir.png", "lamp_description_1.png",
                     "lamp_description_2.png"],
    }
    print(profile, summary["profiles"][profile], flush=True)
(args.out / "description_results.json").write_text(json.dumps(summary, indent=2) + "\n")
if not all(p["returncode"] == 0 for p in summary["profiles"].values()):
    raise SystemExit("Échec du coeur")
