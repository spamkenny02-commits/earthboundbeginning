"""Verify the later V78 checkpoint images separately from the 81-text checkpoint."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[2]
def verify(dest=None):
 count=changed=frames=0;declared=set();dest=dest or ROOT/'tests/emulation_v78_remaining';comparison=json.loads((dest/'comparison_v77.json').read_text())
 for p in ('accents','ascii'):
  report=json.loads((dest/f'results_{p}.json').read_text());pairs=comparison[p]['comparisons'];captures=[cap for c in report['cases'].values() for cap in c['captures']];assert len(pairs)==len(captures);frames+=sum(c['sampled_frames'] for c in report['cases'].values())
  for pair,cap in zip(pairs,captures):
   assert cap['path']==pair['after_path'];a_path=ROOT/pair['before_path'];z_path=ROOT/cap['path'];declared.update((a_path,z_path));a=Image.open(a_path).convert('RGB');z=Image.open(z_path).convert('RGB');assert a.size==z.size==(256,224);assert hashlib.sha256(z_path.read_bytes()).hexdigest()==cap['artifact_png_sha256'];assert hashlib.sha256(a_path.read_bytes()).hexdigest()==pair['before_png_sha256'];assert hashlib.sha256(a.tobytes()).hexdigest()==pair['before_rgb_sha256'];assert hashlib.sha256(z.tobytes()).hexdigest()==pair['after_rgb_sha256']==cap['sha256_rgb'];diff=ImageChops.difference(a,z);box=diff.getbbox();assert (list(box) if box else None)==pair['bbox'];window=[104,8,248,126] if pair['case'].startswith('train_') else [104,8,248,98];assert pair['allowed_text_window']==window;diff.paste((0,0,0),tuple(window));assert diff.getbbox() is None;count+=1;changed+=bool(box)
 assert set(dest.rglob('*.png'))==declared
 return {'pairs':count,'changed_text_only':changed,'sampled_frames':frames}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
