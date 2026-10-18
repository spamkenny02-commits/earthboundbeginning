"""Private Snes9x controller session with read-only live text sampling."""
import collections,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/v63'),str(ROOT/'tools/v62')]
import runtime as b
from live_text import BASE,TOP,prove,current_pointer
class Session:
 def __init__(self,source,core,out,profile,entry=None,version=64):
  self.out=out.resolve();self.out.mkdir(parents=True,exist_ok=True);self.rom=self.out/'fixture.sfc'
  plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());assert b.sha(source)==b.ROM_SHA
  ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes();assert b.sha(ips)==plan['profiles'][profile]['sha256']
  self.data=b.apply(source,b.records(ips));assert b.sha(self.data)==plan['profiles'][profile]['target_rom_sha256'];prove(self.data)
  self.fixture=bytearray(self.data)
  self.routing=[]
  if entry is not None:
   self.routing=[{'offset':'368B51','old':self.data[0x368B51:0x368B55].hex(),'new':b.pointer(entry).hex()}]
   self.fixture[0x368B51:0x368B55]=b.pointer(entry)
   assert self.fixture[:0x368B51]==self.data[:0x368B51] and self.fixture[0x368B55:]==self.data[0x368B55:]
  prove(self.fixture)
  self.rom.write_bytes(self.fixture);self.err=(self.out/'stderr.log').open('w')
  self.proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(self.rom),'--core',str(core.resolve()),'--out',str(self.out),'--history-every','120'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True)
  self.events=[];self.counts=collections.Counter();self.frame=0;self.last=None;self.commands=[];assert self.read()['source_sha256']==b.sha(self.fixture)
 def read(self):
  while True:
   line=self.proc.stdout.readline()
   if not line:raise RuntimeError('Emulator exited')
   try:return json.loads(line)
   except json.JSONDecodeError:pass
 def send(self,c):
  self.commands.append(c);self.proc.stdin.write(json.dumps(c)+'\n');self.proc.stdin.flush();return self.read()
 def step(self,n,buttons=(),sample=True):
  if not sample:return self.send({'frames':n,'buttons':list(buttons)})
  for _ in range(n):
   r=self.send({'frames':1,'buttons':list(buttons),'ram':{'offset':hex(BASE),'length':TOP+2-BASE}});self.frame+=1
   p=current_pointer(bytes.fromhex(r['ram_hex']))
   if p:self.counts[p['rom_offset']]+=1
   if p!=self.last:self.events.append({'sample':self.frame,'pointer':p});self.last=p
 def tap(self,key,sample=True):self.step(2,(key,),sample);self.step(12,sample=sample)
 def capture(self,name):return self.send({'screenshot':name})['image']
 def close(self):
  try:self.send({'quit':True});self.proc.wait(timeout=10);assert self.proc.returncode==0
  finally:
   if self.proc.poll() is None:self.proc.kill();self.proc.wait()
   self.err.close();self.rom.unlink(missing_ok=True)
