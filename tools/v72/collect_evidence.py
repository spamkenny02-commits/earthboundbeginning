"""Export only PNG screenshots and cursor reports from private linked sessions."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def collect(source,sheets=None):
 dest=ROOT/'tests/emulation_v72';caps=[];count=0
 for p in ('accents','ascii'):
  r=json.loads((source/f'results_{p}.json').read_text())
  for name,c in r['cases'].items():
   for phase,data in c['phases'].items():
    for cap in data['captures']:
     src=Path(cap['path']);src=src if src.is_absolute() else source/p/name/phase/src.name;target=dest/p/name/phase/src.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target);cap['path']=str(target.relative_to(ROOT));cap['artifact_png_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();count+=1
     if phase=='inspect' or src.stem in ('arrival',f"courier_{len(data['courier_steps']):02d}"):caps.append((p,name,phase,target))
  (dest/f'results_{p}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 if sheets:
  sheets.mkdir(parents=True,exist_ok=True)
  for start in range(0,len(caps),24):
   batch=caps[start:start+24];im=Image.new('RGB',(1024,250*((len(batch)+3)//4)),(35,35,35));d=ImageDraw.Draw(im)
   for i,(p,name,phase,path) in enumerate(batch):
    x=i%4*256;y=i//4*250;im.paste(Image.open(path),(x,y+25));d.text((x,y+2),f'{p} {name} {phase} {path.stem}',fill='white')
   im.save(sheets/f'sheet_{start//24}.png')
 return {'exported_captures':count,'review_focus':len(caps)}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--sheets',type=Path);a=ap.parse_args();print(collect(a.source,a.sheets))
