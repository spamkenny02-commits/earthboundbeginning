"""Collect public screenshots only; keep ROM, states and memory private."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def collect(current,reference,sheets=None):
 dest=ROOT/'tests/emulation_v74';caps=[];comparison={}
 for p in ('accents','ascii'):
  r=json.loads((current/f'results_{p}.json').read_text());ref=json.loads((reference/f'results_{p}.json').read_text());pairs=[]
  assert r['initial_state_sha256']==ref['initial_state_sha256']
  for name,c in r['cases'].items():
   oldcase=ref['cases'][name]
   for field in ('trigger','steps','operations','inventory_trigger','sampled_frames'):assert oldcase[field]==c[field],field
   assert len(oldcase['captures'])==len(c['captures'])
   for old,cap in zip(oldcase['captures'],c['captures']):
    for source,entry,sub in ((current,cap,Path(p)/name),(reference,old,Path('reference_v73')/p/name)):
     src=Path(entry['path']);src=src if src.is_absolute() else source/p/name/src.name;target=dest/sub/src.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target);entry['path']=str(target.relative_to(ROOT));entry['artifact_png_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
    a=Image.open(ROOT/old['path']).convert('RGB');z=Image.open(ROOT/cap['path']).convert('RGB');diff=ImageChops.difference(a,z);box=diff.getbbox();diff.paste((0,0,0),(104,8,248,98));assert diff.getbbox() is None,(p,name,cap['path'],box)
    pairs.append({'case':name,'before_path':old['path'],'after_path':cap['path'],'before_png_sha256':old['artifact_png_sha256'],'before_rgb_sha256':hashlib.sha256(a.tobytes()).hexdigest(),'after_rgb_sha256':hashlib.sha256(z.tobytes()).hexdigest(),'bbox':list(box) if box else None});caps.append((p,name,ROOT/cap['path']))
  (dest/f'results_{p}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');comparison[p]={'same_controller_inputs':True,'allowed_text_window':[104,8,248,98],'comparisons':pairs}
 (dest/'comparison_v73.json').write_text(json.dumps(comparison,indent=2)+'\n')
 if sheets:
  sheets.mkdir(parents=True,exist_ok=True)
  for start in range(0,len(caps),20):
   batch=caps[start:start+20];im=Image.new('RGB',(1024,250*((len(batch)+3)//4)),(35,35,35));d=ImageDraw.Draw(im)
   for i,(p,name,path) in enumerate(batch):
    x=i%4*256;y=i//4*250;im.paste(Image.open(path),(x,y+25));d.text((x,y+2),f'{p} {name} {path.stem}',fill='white')
   im.save(sheets/f'sheet_{start//20}.png')
 return len(caps)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',type=Path,required=True);ap.add_argument('--reference',type=Path,required=True);ap.add_argument('--sheets',type=Path);a=ap.parse_args();print(collect(a.current,a.reference,a.sheets))
