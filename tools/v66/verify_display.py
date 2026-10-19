import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[2]
def verify():
 count=pairs=changed=0
 for p in ('accents','ascii'):
  r=json.loads((ROOT/f'tests/emulation_v66/results_{p}.json').read_text())
  for c in r['cases'].values():
   for cap in c['captures']:
    im=Image.open(ROOT/cap['path']).convert('RGB');assert im.size==(256,224);assert hashlib.sha256(im.tobytes()).hexdigest()==cap['sha256_rgb'];count+=1
 for c in json.loads((ROOT/'tests/emulation_v66/comparison_v65.json').read_text()).values():
  for x in c['comparisons']:
   a=Image.open(ROOT/x['before_path']).convert('RGB');z=Image.open(ROOT/x['after_path']).convert('RGB');assert hashlib.sha256(a.tobytes()).hexdigest()==x['before_rgb_sha256'];assert hashlib.sha256(z.tobytes()).hexdigest()==x['after_rgb_sha256'];diff=ImageChops.difference(a,z);box=diff.getbbox();assert (list(box) if box else None)==x['bbox'];changed+=bool(box);diff.paste((0,0,0),tuple(c['allowed_text_window']));assert diff.getbbox() is None;pairs+=1
 assert count==178 and pairs==48 and changed>0
 return {'captures':count,'reference_pairs':pairs,'changed_pairs':changed,'only_text_window_changed':True}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
