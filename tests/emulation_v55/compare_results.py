"""Verify visible outcomes against V54; only the translated question may differ."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops
ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);args=ap.parse_args();result={}
for profile in ('accents','ascii'):
 checks={}
 for old in sorted((args.directory/'v54'/profile).glob('*/result.png')):
  name=old.parent.name;new=args.directory/'v55'/profile/name/'result.png'
  a=Image.open(old).convert('RGB');b=Image.open(new).convert('RGB');assert a.size==b.size==(256,224)
  equal=ImageChops.difference(a,b).getbbox() is None
  crops=[(0,0,256,16),(0,29,256,224),(0,16,106,29),(243,16,256,29)] if name in ['snowman_'+str(i) for i in range(4)] else [(0,0,256,224)]
  outside=all(ImageChops.difference(a.crop(c),b.crop(c)).getbbox() is None for c in crops)
  checks[name]={'identical':equal,'outside_translated_question_identical':outside};assert outside,name
 assert len(checks)==20;result[profile]=checks
(args.directory/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print('40 outcome comparisons passed')
