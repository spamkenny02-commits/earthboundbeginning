"""Recompute all V65 RGB hashes and V64/V65 storage image comparisons."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[2]
def verify():
 count=pairs=0
 for p in ('accents','ascii'):
  report=json.loads((ROOT/f'tests/emulation_v65/results_{p}.json').read_text())
  for case in report['cases'].values():
   for cap in case['captures']:
    im=Image.open(ROOT/cap['path']).convert('RGB');assert im.size==(256,224);assert hashlib.sha256(im.tobytes()).hexdigest()==cap['sha256_rgb'];count+=1
 comparisons=json.loads((ROOT/'tests/emulation_v65/comparison_v64.json').read_text())
 for profile in comparisons.values():
  for c in profile['comparisons']:
   a=Image.open(ROOT/c['before_path']).convert('RGB');z=Image.open(ROOT/c['after_path']).convert('RGB');assert hashlib.sha256(a.tobytes()).hexdigest()==c['before_rgb_sha256'];assert hashlib.sha256(z.tobytes()).hexdigest()==c['after_rgb_sha256']
   diff=ImageChops.difference(a,z);bbox=diff.getbbox();pixels=diff.tobytes();assert (list(bbox) if bbox else None)==c['bbox'];assert sum(any(pixels[i:i+3]) for i in range(0,len(pixels),3))==c['changed_pixels'];diff.paste((0,0,0),tuple(profile['allowed_text_window']));assert diff.getbbox() is None;pairs+=1
 assert count==84 and pairs==40
 return {'primary_captures':count,'reference_pairs':pairs,'only_text_window_changed':True}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
