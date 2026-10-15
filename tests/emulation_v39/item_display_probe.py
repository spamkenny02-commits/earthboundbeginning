import argparse,json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--rom',type=Path,required=True)
parser.add_argument('--core',type=Path,required=True)
parser.add_argument('--states-dir',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
parser.add_argument('--ids',nargs='*',help='Optional script IDs for a smaller verification pass')
args=parser.parse_args()
OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tools/v19'));from build_v19 import apply,records,sha
source=args.rom.read_bytes()
assert sha(source)=='e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
fixture=json.loads((ROOT/'tools/v39/v39_descriptions_fr.json').read_text())
summary={'method':'controlled_first_inventory_slot_then_normal_Objects_Help_menu','rom_modified_for_probe':False,'inventory_wram_offset':'99F1','profiles':{}}
for profile in ('accents','ascii'):
 out=OUT/profile;out.mkdir(exist_ok=True)
 rom=out/'test.sfc';rom.write_bytes(apply(source,records((ROOT/f'patches/EarthBound_Beginnings_FR_v39_{profile}.ips').read_bytes())))
 err=(out/'probe_stderr.log').open('w')
 p=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v39/inventory_fixture_runner.py'),'--core',str(args.core.resolve()),'--rom',str(rom),'--out',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
 def read():
  while True:
   line=p.stdout.readline()
   if not line:raise RuntimeError('Emulator exited')
   try:return json.loads(line)
   except json.JSONDecodeError:pass
 def send(x):
  p.stdin.write(json.dumps(x)+'\n');p.stdin.flush();return read()
 def tap(key):send({'frames':2,'buttons':[key]});send({'frames':12})
 ready=read();summary['profiles'][profile]={'ready':ready,'items':[]}
 for e in fixture['scripts']:
  if args.ids and e['id'] not in args.ids:continue
  item=(int(e['table_refs'][0],16)-0x155023)//39;ident=e['id']
  send({'load':str((args.states_dir/profile/'after_combat.state').resolve()),'frames':1})
  before=send({'ram':{'offset':'0x99f1','length':1}})
  assert before['ram_hex']=='b1',before
  send({'write_ram':{'offset':'0x99f1','hex':f'{item:02x}'}})
  send({'frames':60});tap('A');tap('Right');tap('A');tap('A')
  for _ in range(4):tap('Down')
  send({'frames':1,'screenshot':ident+'_selected'})
  tap('A');captures=[]
  for page in range(1,5):
   r=send({'frames':600,'screenshot':f'{ident}_page{page}'});captures.append(r['image'])
   tap('A')
  summary['profiles'][profile]['items'].append({'id':ident,'item_id':item,'captures':captures})
  print(profile,ident,item,flush=True)
 send({'quit':True});p.wait(timeout=10);err.close()
 summary['profiles'][profile]['returncode']=p.returncode
(OUT/'probe_results.json').write_text(json.dumps(summary,indent=2)+'\n')
