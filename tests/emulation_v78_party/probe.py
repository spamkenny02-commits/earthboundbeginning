"""Native temporary party preparation; controlled storage and party-count branches."""
import argparse,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('party_base78',ROOT/'tests/emulation_v78/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CASES={
 'minnie_two':{'entry':0x36B788,'operations':[('join',2),('give',0x70)],'steps':[['A'],['A'],['A'],['A'],['Right','A'],['A'],['Right','A'],['Right','A'],['A'],['A'],['Right','A'],['A'],['Right','A'],['B'],['A'],['A'],['Right','A'],['Right'],['A']],'scope':'Minnie NPC204 entry forced; native join02 and give70; deposit from Ninten, retrieval to Ana, both inventories inspected; no natural recruitment or initial encounter'},
 'mother_two':{'entry':0x33FC0E,'operations':[('join',2)],'steps':[['A']]*3,'scope':'name branch forced; native join02; native party-count pronoun selection with Ninten and Ana; no natural encounter'},
 'mother_three':{'entry':0x33FC0E,'operations':[('join',2),('join',3)],'steps':[['A']]*3,'scope':'name branch forced; native join02 and join03; native party-count pronoun selection with Ninten, Ana and Lloyd; no natural encounter'},
}
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78)
 m.CASES=CASES;m.run(ap.parse_args())
