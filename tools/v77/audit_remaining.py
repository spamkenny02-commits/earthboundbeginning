"""Refresh the scoped V73 direct-NPC inventory after the desert translations."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v73'))
from audit_custom_npc_roots import audit,b
def run(rom):
 source=rom.read_bytes();assert b.sha(source)==b.ROM_SHA;ips=(ROOT/'patches/EarthBound_Beginnings_FR_v77_accents.ips').read_bytes();plan=json.loads((ROOT/'tools/v77/validation_v77.json').read_text());assert b.sha(ips)==plan['profiles']['accents']['sha256'];data=b.apply(source,b.records(ips));assert b.sha(data)==plan['profiles']['accents']['target_rom_sha256'];result=audit(source,data);result['version']='v77';return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);a=ap.parse_args();r=run(a.rom);(ROOT/'tools/v77/custom_npc_roots_v77.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print({'roots':r['custom_roots_examined'],'remaining_candidates':[e['root'] for e in r['candidates']],'unparsed':len(r['unparsed_roots'])})
