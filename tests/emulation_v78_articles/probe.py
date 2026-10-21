"""Qualified container caption and Minnie deposit contexts, all entries forced."""
import argparse,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('base_articles78',ROOT/'tests/emulation_v78/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CASES={
 'contents_caption':{'entry':0x32B500,'steps':[['A']]*2,'scope':'container text branch forced with current native item variable; no natural container or object acquisition certified'},
 'minnie_deposit':{'entry':0x36B788,'operations':[['give',0x70]],'steps':[['A'],['A'],['A'],['Right','A'],['A'],['Right','A'],['A'],['A'],['B'],['Right','A'],['A'],['A'],['A'],['A'],['Right','A'],['B'],['A'],['A'],['Right','A']],'scope':'complete Minnie NPC204 entry forced with native gift of item70 (58 dollars); deposit, reserve listing, retrieval and final inventory observed through controller input; no natural encounter certified'},
 'minnie_confirmation':{'entry':0x36B82E,'steps':[],'scope':'interior confirmation forced with current native item variable; pause captured, no deposit completion certified'},
}
m.CASES=CASES
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);m.run(ap.parse_args())
