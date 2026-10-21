"""Strict two-window comparison: native action labels and dialogue/help text."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'tests/emulation_v78_actions'
WINDOWS=[[104,8,248,98],[8,8,56,110]]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def collect(current,reference):
 comparison={}
 for p in ('accents','ascii'):
  r=json.loads((current/f'results_{p}.json').read_text());old=json.loads((reference/f'results_{p}.json').read_text());assert r['initial_state_sha256']==old['initial_state_sha256'];pairs=[]
  for name,c in r['cases'].items():
   before=old['cases'][name]
   for key in ('entries','logical_entry','scope','operations','trigger','steps','settle_frames','wait_after_preparation_frames','sampled_frames'):assert c[key]==before[key],(name,key)
   assert len(c['captures'])==len(before['captures'])
   for cap,prior in zip(c['captures'],before['captures']):
    paths=[]
    for entry,base,prefix in ((cap,current,Path()),(prior,reference,Path('reference_v77'))):
     src=Path(entry['path']);src=src if src.is_absolute() else base/p/name/src.name;dst=DEST/prefix/p/name/src.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);paths.append(dst);entry['path']=str(dst.relative_to(ROOT));entry['artifact_png_sha256']=sha(dst.read_bytes())
    z,a=(Image.open(path).convert('RGB') for path in paths);diff=ImageChops.difference(a,z);box=diff.getbbox()
    for window in WINDOWS:diff.paste((0,0,0),tuple(window))
    assert diff.getbbox() is None,(p,name,cap['path'],box)
    pairs.append({'case':name,'windows':WINDOWS,'before_path':prior['path'],'after_path':cap['path'],'before_png_sha256':prior['artifact_png_sha256'],'before_rgb_sha256':sha(a.tobytes()),'after_rgb_sha256':sha(z.tobytes()),'bbox':list(box) if box else None})
  (DEST/f'results_{p}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');comparison[p]={'same_controller_inputs':True,'comparisons':pairs}
 (DEST/'comparison_v77.json').write_text(json.dumps(comparison,indent=2)+'\n')
 return verify()
def verify():
 comparison=json.loads((DEST/'comparison_v77.json').read_text());count=changed=frames=0;declared=set()
 for p in ('accents','ascii'):
  r=json.loads((DEST/f'results_{p}.json').read_text());caps=[cap for c in r['cases'].values() for cap in c['captures']];pairs=comparison[p]['comparisons'];assert len(caps)==len(pairs);frames+=sum(c['sampled_frames'] for c in r['cases'].values())
  for cap,pair in zip(caps,pairs):
   assert pair['windows']==WINDOWS and pair['after_path']==cap['path'];a_path=ROOT/pair['before_path'];z_path=ROOT/cap['path'];declared.update((a_path,z_path));assert sha(a_path.read_bytes())==pair['before_png_sha256'];assert sha(z_path.read_bytes())==cap['artifact_png_sha256'];a=Image.open(a_path).convert('RGB');z=Image.open(z_path).convert('RGB');assert a.size==z.size==(256,224);assert sha(a.tobytes())==pair['before_rgb_sha256'];assert sha(z.tobytes())==pair['after_rgb_sha256']==cap['sha256_rgb'];diff=ImageChops.difference(a,z);box=diff.getbbox();assert (list(box) if box else None)==pair['bbox']
   for window in WINDOWS:diff.paste((0,0,0),tuple(window))
   assert diff.getbbox() is None;count+=1;changed+=bool(box)
 assert declared==set(DEST.rglob('*.png'))
 return {'pairs':count,'changed_text_only':changed,'sampled_frames':frames}
