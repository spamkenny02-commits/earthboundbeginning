from pathlib import Path
import json,sys
sys.path.insert(0,'/mnt/data/v17_merge')
from fusionner_v17 import records
rom=Path('/mnt/data/EarthBound Beginnings (USA) 1.2(1).sfc').read_bytes()
patch=Path('/mnt/data/v17_release/EarthBound_Beginnings_FR_v17_accents.ips').read_bytes()
occupied=bytearray(len(rom))
for p,b in records(patch):occupied[p:p+len(b)]=b'\1'*len(b)
refs={}
for p in range(len(rom)-3):
 if rom[p+3]==0 and 0xC0<=rom[p+2]<=0xFF:
  v=int.from_bytes(rom[p:p+4],'little')-0xC00000
  if 0<=v<len(rom):refs.setdefault(v,[]).append(p)
out=[]
for start,rs in refs.items():
 if rom[start]!=0x70 or occupied[start]:continue
 pos=start+1
 while pos<min(start+140,len(rom)) and 0x50<=rom[pos]<=0xAA and not occupied[pos]:pos+=1
 if pos-start<13 or pos-start>100:continue
 if rom[pos:pos+2]!=b'\x13\x02':continue
 end=pos+2
 if any(occupied[start:end]):continue
 if any(x in refs for x in range(start+1,end)):continue
 s=''.join(chr(x-48) for x in rom[start+1:pos])
 if not all(32<=ord(c)<127 for c in s):continue
 out.append({'id':f'{start:06X}','english':s,'refs':[f'{x:06X}' for x in rs],'length':end-start})
out.sort(key=lambda e:(e['length'],e['id']))
Path('/mnt/data/v18_candidates.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print('total',len(out));
for e in out[:95]:print(e['id'],e['length'],e['english'])
