"""Compare reference replay and normal Telepathy images against V55."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops
ap=argparse.ArgumentParser();ap.add_argument('--prior-replay',type=Path,required=True);ap.add_argument('--replay',type=Path,required=True);ap.add_argument('--natural',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();summary={}
for profile in ('accents','ascii'):
 old={p.name:p for p in (args.prior_replay/profile).glob('*.png')};new={p.name:p for p in (args.replay/profile).glob('*.png')};assert old and old.keys()==new.keys()
 changed=[n for n in old if Image.open(old[n]).tobytes()!=Image.open(new[n]).tobytes()];assert not changed
 a=Image.open(args.natural/'v55'/profile/'step_4.png').convert('RGB');b=Image.open(args.natural/'v56'/profile/'step_4.png').convert('RGB');assert a.size==b.size==(256,224)
 crops=[(0,0,256,16),(0,65,256,224),(0,16,104,65),(244,16,256,65)]
 outside=all(ImageChops.difference(a.crop(c),b.crop(c)).getbbox() is None for c in crops);assert outside
 summary[profile]={'reference_screens_compared':len(old),'changed_reference_screens':changed,'natural_telepathy_only_text_rectangle_changed':outside,'text_rectangle':[104,16,244,65]}
args.out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
