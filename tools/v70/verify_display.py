import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[2]
def verify():
 count=changed=frames=0;comparison=json.loads((ROOT/'tests/emulation_v70/comparison_v67.json').read_text())
 for p in ('accents','ascii'):
  report=json.loads((ROOT/f'tests/emulation_v70/results_{p}.json').read_text());caps=[cap for c in report['cases'].values() for cap in c['captures']];frames+=sum(c['sampled_frames'] for c in report['cases'].values());pairs=comparison[p]['comparisons'];assert len(pairs)==len(caps)
  for cap,pair in zip(caps,pairs):
   assert cap['path']==pair['after_path'];a=Image.open(ROOT/pair['before_path']).convert('RGB');z=Image.open(ROOT/cap['path']).convert('RGB');assert a.size==z.size==(256,224)
   assert hashlib.sha256((ROOT/cap['path']).read_bytes()).hexdigest()==cap['artifact_png_sha256'];assert hashlib.sha256((ROOT/pair['before_path']).read_bytes()).hexdigest()==pair['before_png_sha256'];assert hashlib.sha256(z.tobytes()).hexdigest()==cap['sha256_rgb']==pair['after_rgb_sha256'];assert hashlib.sha256(a.tobytes()).hexdigest()==pair['before_rgb_sha256']
   diff=ImageChops.difference(a,z);box=diff.getbbox();assert (list(box) if box else None)==pair['bbox'];changed+=bool(box);diff.paste((0,0,0),(104,8,248,98));assert diff.getbbox() is None;count+=1
 assert count==338
 for f in (ROOT/'tests/emulation_v70').rglob('*'):
  if f.is_file():assert f.suffix.lower() not in ('.sfc','.smc','.state','.so','.bin','.wram','.dmp')
 return {'captures_and_pairs':count,'changed_text_only':changed,'sampled_frames':frames}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
