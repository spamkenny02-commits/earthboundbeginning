"""Controlled remaining V78 dialogue; no natural train trip certified."""
import argparse,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('base_probe78',ROOT/'tests/emulation_v78/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CASES={
 'train_spookane_no':{'entry':0x36DCD5,'steps':[['A'],['A'],['A'],['Right','A'],['A']]},
 'train_reindeer_no':{'entry':0x36DCD5,'steps':[['A'],['A'],['Down','A'],['Right','A'],['A']]},
 'train_merrysville_no':{'entry':0x36DCD5,'steps':[['A'],['A'],['Down','Down','A'],['Right','A'],['A']]},
 'train_youngtown_quote':{'entry':0x36DCD5,'operations':[['flag',0x339]],'steps':[['A'],['A'],['Down','Down','Down','A'],['Right','A'],['A']]},
 'father_name_no':{'entry':0x386C80,'operations':[['flag',0x376]],'steps':[['A'],['A'],['Right','A']]},
 # Historical fixture name; this is the name-check branch of Lloyd's father.
 'pippi_check_name':{'entry':0x386D23,'steps':[['A']]},
 'youngtown_departure':{'entry':0x36E573,'steps':[['A']]*9},
 'concern':{'entry':0x36E832,'steps':[['A'],['A']]},
 'monkey_charm':{'entry':0x377419,'steps':[['A']]*3},
 'fruit_no':{'entry':0x380B42,'steps':[['Right','A'],['A'],['A']]},
 'father_money_no':{'entry':0x384B8B,'steps':[['Right','A'],['A']]},
 'father_money_need_no':{'entry':0x384B8B,'steps':[['A'],['Right','A'],['A']]},
 'balance_prompt':{'entry':0x384C44,'steps':[['B'],['A']]},
 'money_text_only':{'entry':0x384C9A,'steps':[['A'],['A']]},
 'money_rethink':{'entry':0x384D6E,'steps':[['A'],['A'],['A']]},
 'monkey_theft':{'entry':0x38BA92,'operations':[['give',0xAB]],'steps':[['A']]*4},
 'serum_help':{'entry':0x054789,'steps':[['A']]},
 'shop_choice':{'entry':0x37B994,'steps':[['Right','A'],['A'],['A']]},
 'hotel_greeting':{'entry':0x37959C,'steps':[['A'],['Right','A'],['A']]},
}
for c in CASES.values():c['scope']='controlled script/branch entry; no natural encounter or journey certified'
m.CASES=CASES
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);m.run(ap.parse_args())
