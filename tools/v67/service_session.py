"""Controlled service calls, optional native item grants; no direct WRAM writes."""
import collections,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v64'))
from session import Session as BaseSession
import runtime as b
from live_text import prove

class ServiceSession(BaseSession):
 def __init__(self,source,core,out,profile,entries,version=66,seed_items=()):
  assert all(type(item) is int and 1<=item<=255 for item in seed_items)
  assert len(seed_items)<=13
  self.out=out.resolve();self.out.mkdir(parents=True,exist_ok=True);self.rom=self.out/'fixture.sfc'
  assert b.sha(source)==b.ROM_SHA
  plan=json.loads((ROOT/f'tools/v{version}/validation_v{version}.json').read_text());ips=(ROOT/f'patches/EarthBound_Beginnings_FR_v{version}_{profile}.ips').read_bytes()
  assert b.sha(ips)==plan['profiles'][profile]['sha256']
  self.data=b.apply(source,b.records(ips));assert b.sha(self.data)==plan['profiles'][profile]['target_rom_sha256']
  wrapper=0x330FC0;payload=b''.join(bytes((0x1D,0x00,0x01,item)) for item in seed_items)+b''.join(b'\x08'+b.pointer(a) for a in entries)+b'\x02'
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
