"""Controlled service calls, declared native item grants/removals; no direct WRAM writes."""
import collections,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v64'))
from session import Session as BaseSession
import runtime as b
from live_text import prove

def operations_payload(operations):
 assert len(operations)<=13
 result=bytearray()
 for op,item in operations:
  assert op in ('give','take') and type(item) is int and 1<=item<=255
  result.extend((0x1D,0 if op=='give' else 1,1,item))
 return bytes(result)

class ServiceSession(BaseSession):
 def __init__(self,source,core,out,profile,entries,version=67,operations=()):
  preparation=operations_payload(operations)
  self.out=out.resolve();self.out.mkdir(parents=True,exist_ok=True);self.rom=self.out/'fixture.sfc'
  assert b.sha(source)==b.ROM_SHA
  plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes()
  assert b.sha(ips)==plan['profiles'][profile]['sha256']
  self.data=b.apply(source,b.records(ips));assert b.sha(self.data)==plan['profiles'][profile]['target_rom_sha256']
  wrapper=0x330FC0;payload=preparation+b''.join(b'\x08'+b.pointer(a) for a in entries)+b'\x02'
  assert len(payload)<=64 and self.data[wrapper:wrapper+len(payload)]==bytes(len(payload))
  self.fixture=bytearray(self.data);self.fixture[0x368B51:0x368B55]=b.pointer(wrapper);self.fixture[wrapper:wrapper+len(payload)]=payload
  self.routing=[{'offset':'368B51','hex':b.pointer(wrapper).hex()},{'offset':f'{wrapper:06X}','hex':payload.hex()}]
  mask=bytearray(len(self.data))
  for r in self.routing:
   a=int(r['offset'],16);raw=bytes.fromhex(r['hex']);mask[a:a+len(raw)]=b'\1'*len(raw)
  assert all(x==y or m for x,y,m in zip(self.data,self.fixture,mask));prove(self.fixture)
  self.rom.write_bytes(self.fixture);self.err=(self.out/'stderr.log').open('w')
  self.proc=subprocess.Popen([sys.executable,str(ROOT/'tests/emulation_v18_work/libretro_runner.py'),'--rom',str(self.rom),'--core',str(core.resolve()),'--out',str(self.out),'--history-every','120'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True)
  self.events=[];self.counts=collections.Counter();self.frame=0;self.last=None;self.commands=[];assert self.read()['source_sha256']==b.sha(self.fixture)
