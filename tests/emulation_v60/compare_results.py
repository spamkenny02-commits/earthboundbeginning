"""Compare complete reference captures from V59 and V60, in RGB."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops
ap=argparse.ArgumentParser()
for name in ('prior','current','out'):ap.add_argument('--'+name,type=Path,required=True)
a=ap.parse_args();result={}
for profile,count in (('accents',109),('ascii',103)):
 old={p.name:p for p in (a.prior/profile).glob('*.png')};new={p.name:p for p in (a.current/profile).glob('*.png')}
 assert old.keys()==new.keys() and len(old)==count,'Incomplete capture set'
 for name,p in old.items():
  before=Image.open(p).convert('RGB');after=Image.open(new[name]).convert('RGB')
  assert before.size==after.size and ImageChops.difference(before,after).getbbox() is None,name
 result[profile]={'screens_compared':count,'all_identical':True}
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
