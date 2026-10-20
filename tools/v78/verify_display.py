"""Recheck all paired V77/V78 screenshots, including unchanged inventory."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[2]
def verify():
 count=changed=frames=0;comparison=json.loads((ROOT/'tests/emulation_v78/comparison_v77.json').read_text())
 for p in ('accents','ascii'):
  r=json.loads((ROOT/f'tests/emulation_v78/results_{p}.json').read_text());caps=[cap for c in r['cases'].values() for cap in c['captures']];frames+=sum(c['sampled_frames'] for c in r['cases'].values());pairs=comparison[p]['comparisons'];assert len(pairs)==len(caps)
  for cap,pair in zip(caps,pairs):
   assert cap['path']==pair['after_path'];a=Image.open(ROOT/pair['before_path']).convert('RGB');z=Image.open(ROOT/cap['path']).convert('RGB');assert a.size==z.size==(256,224)
   assert hashlib.sha256((ROOT/cap['path']).read_bytes()).hexdigest()==cap['artifact_png_sha256'];assert hashlib.sha256((ROOT/pair['before_path']).read_bytes()).hexdigest()==pair['before_png_sha256'];assert hashlib.sha256(z.tobytes()).hexdigest()==cap['sha256_rgb']==pair['after_rgb_sha256'];assert hashlib.sha256(a.tobytes()).hexdigest()==pair['before_rgb_sha256'];diff=ImageChops.difference(a,z);box=diff.getbbox();assert (list(box) if box else None)==pair['bbox'];changed+=bool(box);window=[104,8,248,126] if pair['case']=='healer_entry' else [104,8,248,98];assert pair['allowed_text_window']==window;diff.paste((0,0,0),tuple(window));assert diff.getbbox() is None;count+=1
 assert count==146 and frames==39412
 return {'captures_and_pairs':count,'changed_text_only':changed,'sampled_frames':frames}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
