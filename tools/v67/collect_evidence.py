"""Import only screenshots and text-cursor reports from private probe outputs."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def collect(current,reference,sheets=None):
 dest=ROOT/'tests/emulation_v67';allcaps=[];comparisons={}
 for p in ('accents','ascii'):
  r=json.loads((current/f'results_{p}.json').read_text());ref=json.loads((reference/f'results_{p}.json').read_text());pairs=[]
  for name,c in r['cases'].items():
   oldcase=ref['cases'][name];assert oldcase['steps']==c['steps'] and oldcase['seed_items']==c['seed_items'];assert len(oldcase['captures'])==len(c['captures'])
   for old,cap in zip(oldcase['captures'],c['captures']):
    for source,entry,subdir in ((current,cap,Path(p)/name),(reference,old,Path('reference_v66')/p/name)):
     src=Path(entry['path']);src=src if src.is_absolute() else source/p/name/src.name;target=dest/subdir/src.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target);entry['path']=str(target.relative_to(ROOT));entry['artifact_png_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
    a=Image.open(ROOT/old['path']).convert('RGB');z=Image.open(ROOT/cap['path']).convert('RGB');diff=ImageChops.difference(a,z);box=diff.getbbox();diff.paste((0,0,0),(104,8,248,98));assert diff.getbbox() is None
    pairs.append({'case':name,'before_path':old['path'],'after_path':cap['path'],'before_png_sha256':old['artifact_png_sha256'],'before_rgb_sha256':hashlib.sha256(a.tobytes()).hexdigest(),'after_rgb_sha256':hashlib.sha256(z.tobytes()).hexdigest(),'bbox':list(box) if box else None,'only_text_window_changed':True});allcaps.append((p,name,ROOT/cap['path']))
  (dest/f'results_{p}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');comparisons[p]={'same_controller_inputs':True,'same_native_preparations':True,'allowed_text_window':[104,8,248,98],'comparisons':pairs}
 (dest/'comparison_v66.json').write_text(json.dumps(comparisons,indent=2)+'\n')
 if sheets:
  sheets.mkdir(parents=True,exist_ok=True)
  for start in range(0,len(allcaps),32):
   batch=allcaps[start:start+32];sheet=Image.new('RGB',(1024,250*((len(batch)+3)//4)),(35,35,35));draw=ImageDraw.Draw(sheet)
   for i,(p,name,path) in enumerate(batch):
    x=i%4*256;y=i//4*250;sheet.paste(Image.open(path),(x,y+25));draw.text((x+2,y+3),f'{p} {name} {path.stem}',fill='white')
   sheet.save(sheets/f'sheet_{start//32}.png')
 return {'captures':len(allcaps),'reference_pairs':sum(len(c['comparisons']) for c in comparisons.values())}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',type=Path,required=True);ap.add_argument('--reference',type=Path,required=True);ap.add_argument('--sheets',type=Path);a=ap.parse_args();print(collect(a.current,a.reference,a.sheets))
