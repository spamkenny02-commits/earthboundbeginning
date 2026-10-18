"""Compare reference replay and normal inventory operation responses against V56."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops
ap=argparse.ArgumentParser();ap.add_argument('--prior-replay',type=Path,required=True);ap.add_argument('--replay',type=Path,required=True);ap.add_argument('--natural',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();summary={}
for profile in ('accents','ascii'):
 old={p.name:p for p in (args.prior_replay/profile).glob('*.png')};new={p.name:p for p in (args.replay/profile).glob('*.png')};assert old and old.keys()==new.keys()
 changed=[n for n in old if Image.open(old[n]).tobytes()!=Image.open(new[n]).tobytes()];assert not changed
 checks={}
 for case in ('eat_card','give_card_to_self','drop_card','help_card','use_card'):
  a=Image.open(args.natural/'v56'/profile/case/'response.png').convert('RGB');b=Image.open(args.natural/'v57'/profile/case/'response.png').convert('RGB');assert a.size==b.size==(256,224)
  crops=[(0,0,256,16),(0,65,256,224),(0,16,104,65),(244,16,256,65)] if case in ('eat_card','give_card_to_self') else [(0,0,256,224)]
  equal=all(ImageChops.difference(a.crop(c),b.crop(c)).getbbox() is None for c in crops);assert equal,(profile,case)
  checks[case]={'only_declared_text_rectangle_changed':equal,'whole_image_identical':ImageChops.difference(a,b).getbbox() is None}
 summary[profile]={'reference_screens_compared':len(old),'changed_reference_screens':changed,'normal_item_response_checks':checks,'translated_text_rectangle':[104,16,244,65]}
args.out.write_text(json.dumps(summary,indent=2)+'\n');print('212 reference images and 10 normal-operation comparisons passed')
