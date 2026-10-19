import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def verify():
 count=frames=0
 for p in ('accents','ascii'):
  r=json.loads((ROOT/f'tests/emulation_v72/results_{p}.json').read_text())
  for c in r['cases'].values():
   for data in c['phases'].values():
    frames+=data['sampled_frames']
    for cap in data['captures']:
     im=Image.open(ROOT/cap['path']).convert('RGB');assert im.size==(256,224);assert hashlib.sha256(im.tobytes()).hexdigest()==cap['sha256_rgb'];count+=1
 assert count==174
 return {'captures':count,'sampled_frames':frames,'patch':'v71 unchanged','new_ips':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
