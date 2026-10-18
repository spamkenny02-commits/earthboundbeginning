"""Read actual V59 entry jumps and copies with a temporary return and pause.
No item acquisition, service branch, or effect is claimed by this isolated probe.
"""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/v59'));import build_v59 as b
SLOT,WRAPPER=0x368B51,0x330FC0
ap=argparse.ArgumentParser()
for name in ('rom','core','states-dir','out'):ap.add_argument('--'+name,type=Path,required=True)
ap.add_argument('--profile',choices=('accents','ascii'),required=True);args=ap.parse_args();profile=args.profile
source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA
plan=json.loads((ROOT/'tools/v59/validation_v59.json').read_text());f=json.loads((ROOT/'tools/v59/v59_fixtures.json').read_text())
base=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v59_{profile}.ips').read_bytes()));assert b.sha(base)==plan['profiles'][profile]['target_rom_sha256']
summary={'method':'isolated_entry_copy_with_temporary_return_and_wait','profile':profile,'wram_modified_by_tester':False,'base_rom_sha256':b.sha(base),'core_sha256':b.sha(args.core.read_bytes()),'cases':{}}
for e in f['edits']:
 name=e['offset'];out=(args.out/profile/name).resolve();out.mkdir(parents=True,exist_ok=True);fixture=bytearray(base);a=int(name,16);d=int(e['copy_offset'],16);text=b.copy_text(e,profile);tail=d+len(text)
 assert base[a:a+5]==b'\x0a'+b.pointer(d) and base[d:tail]==text and base[tail:tail+5]==b'\x0a'+b.pointer(int(e['end'],16))
 wrapper=b'\x01\x08'+b.pointer(a)+b'\x13\x02';assert base[WRAPPER:WRAPPER+len(wrapper)]==bytes(len(wrapper))
 changes=[(SLOT,b.pointer(WRAPPER)),(WRAPPER,wrapper),(tail,b'\x02\x00\x00\x00\x00')]
 for q,v in changes:fixture[q:q+len(v)]=v
 mask=bytearray(len(base))
 for q,v in changes:mask[q:q+len(v)]=b'\1'*len(v)
 assert all(x==y or m for x,y,m in zip(base,fixture,mask))
 rom=out/'fixture.sfc';rom.write_bytes(fixture)
 with (out/'stderr.log').open('w') as err:
  proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(rom),'--core',str(args.core.resolve()),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
  def read():
   while True:
    line=proc.stdout.readline()
    if not line:raise RuntimeError('Emulator exited')
    try:return json.loads(line)
    except json.JSONDecodeError:pass
  def send(c):proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();return read()
  def tap(key):send({'frames':2,'buttons':[key]});send({'frames':12})
  read();send({'load':str((args.states_dir/profile/'after_combat.state').resolve()),'frames':60})
  for key in ('A','Right','A','A','A'):tap(key)
  captures=[send({'frames':90,'screenshot':'early'}),send({'frames':300,'screenshot':'response'})]
  send({'quit':True});proc.wait(timeout=10);assert proc.returncode==0
 rom.unlink();summary['cases'][name]={'returncode':0,'entry_and_copy_payload_unchanged':True,'fixture_sha256':b.sha(fixture),'temporary_writes':[{'offset':f'{q:06X}','hex':v.hex()} for q,v in changes],'captures':captures};print(profile,name,'completed',flush=True)
args.out.mkdir(exist_ok=True,parents=True);(args.out/f'results_{profile}.json').write_text(json.dumps(summary,indent=2)+'\n')
