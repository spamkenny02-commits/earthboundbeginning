"""Controlled copied water help and medical continuation; preserved alias checks."""
import argparse,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('base_scoped78',ROOT/'tests/emulation_v78/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CASES={
 'water_scoped':{'entry':0x054733,'scoped_copy':True,'steps':[['A']]*3,'scope':'copied item-help entry from qualified ID6E record; inventory Help navigation not certified'},
 'water_original':{'entry':0x054733,'steps':[['A']]*3,'scope':'preserved original help entry forced; raw interior alias not certified as an executable text path'},
 'medical_scoped':{'entry':0x0911E2,'steps':[['A']]*4,'scope':'medical preceding text bridge forced; copied continuation reached through its native jump, no diagnosis certified'},
 'medical_original':{'entry':0x0911EB,'steps':[['A']]*4,'scope':'preserved original medical entry forced; raw interior alias not certified as an executable text path'},
}
m.CASES=CASES
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);m.run(ap.parse_args())
