"""Compare the ten controlled V60/V61 responses; outside text must be identical."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops
ap=argparse.ArgumentParser();ap.add_argument('--display',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();result={}
for profile in ('accents','ascii'):
 rows=[]
 for case in ('article','recipient','boo_one','boo_two','boo_three'):
  images=[Image.open(a.display/f'v{v}'/profile/case/'response.png').convert('RGB') for v in (60,61)];diff=ImageChops.difference(*images);box=diff.getbbox();assert box is not None,(profile,case,'unchanged text');diff.paste((0,0,0),(104,8,248,70));assert diff.getbbox() is None,(profile,case,'outside text changed');rows.append({'case':case,'changed_rectangle':box,'outside_text_box_identical':True})
 result[profile]=rows
a.out.write_text(json.dumps(result,indent=2)+'\n');print('10 controlled comparisons passed')
