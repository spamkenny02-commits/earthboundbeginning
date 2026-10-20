"""Contextual dialogue checks; plural helper calls are deliberately artificial."""
import argparse,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('base_grammar78',ROOT/'tests/emulation_v78/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CASES={
 'mother_after_haunting':{'entry':0x33FA7D,'operations':[['flag',0xB8]],'steps':[['A']]*5,'scope':'complete NPC586 entry forced, native flag00B8 preparation; natural haunted-house progression not certified'},
 'mother_name_branch':{'entry':0x33FC0E,'steps':[['A']]*3,'scope':'direct name branch reaches corrected prefix and party-count pronoun selector; one party member'},
 'pronoun_three':{'entry':0x387B2F,'entries':[0x387B2F,0x33FC51],'steps':[['A']],'scope':'plural helper then caller punctuation/pause forced directly; no three-person party or natural selector outcome certified'},
 'pronoun_two':{'entry':0x387B37,'entries':[0x387B37,0x33FC51],'steps':[['A']],'scope':'plural helper then caller punctuation/pause forced directly; no two-person party or natural selector outcome certified'},
 'maria_first':{'entry':0x369D9B,'steps':[['A']]*7,'scope':'first Maria explanation branch forced, including qualified empty possessive call; scene progression not certified'},
 'maria_again':{'entry':0x369E9E,'steps':[['A']]*5,'scope':'repeat Maria explanation branch forced, including qualified empty possessive call; scene progression not certified'},
}
m.CASES=CASES
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);m.run(ap.parse_args())
