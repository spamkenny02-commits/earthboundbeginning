"""Import screenshots and cursor reports only; never import private handoff states."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def collect(source,sheets=None):
 dest=ROOT/'tests/emulation_v69';caps=[]
 for p in ('accents','ascii'):
  r=json.loads((source/f'results_{p}.json').read_text())
  for name,phase in r['phases'].items():
   for cap in phase['captures']:
    src=Path(cap['path']);src=src if src.is_absolute() else source/p/name/src.name;target=dest/p/name/src.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target);cap['path']=str(target.relative_to(ROOT));cap['artifact_png_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();caps.append((p,name,target))
  (dest/f'results_{p}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 if sheets:
  sheets.mkdir(parents=True,exist_ok=True)
  for start in range(0,len(caps),25):
   batch=caps[start:start+25];sheet=Image.new('RGB',(1280,250*((len(batch)+4)//5)),(35,35,35));draw=ImageDraw.Draw(sheet)
   for i,(p,name,path) in enumerate(batch):
    x=i%5*256;y=i//5*250;sheet.paste(Image.open(path),(x,y+25));draw.text((x+2,y+3),f'{p} {name} {path.stem}',fill='white')
   sheet.save(sheets/f'sheet_{start//25}.png')
 return {'captures':len(caps),'private_files_imported':0}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--sheets',type=Path);a=ap.parse_args();print(collect(a.source,a.sheets))
