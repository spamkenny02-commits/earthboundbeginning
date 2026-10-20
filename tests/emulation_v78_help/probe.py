"""Controlled help descriptions and custom-shop stock calibration."""
import argparse,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('base_help78',ROOT/'tests/emulation_v78/probe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CASES={
 'help_crystal':{'entry':0x053D00,'steps':[['A']]*3},
 'help_cap':{'entry':0x053F58,'steps':[['A']]*3},
 'help_egg':{'entry':0x05416D,'steps':[['A']]*3},
 'help_lunch':{'entry':0x054197,'steps':[['A']]*3},
 'help_sauce':{'entry':0x0548FC,'steps':[['A']]*5},
 'help_rust':{'entry':0x054FA2,'steps':[['A']]*4},
 'help_bat':{'entry':0x055EBB,'steps':[['A']]*3},
 'water_guarded':{'entry':0x054733,'steps':[['A']]*3},
 'help_teddy':{'entry':0x053750,'steps':[['A']]*3},
 'help_ribbon':{'entry':0x054055,'steps':[['A']]*3},
 'help_ketchup':{'entry':0x054842,'steps':[['A']]*4},
 'help_salt':{'entry':0x0548A2,'steps':[['A']]*4},
 'stock_0f':{'entry':0x36559E,'steps':[['A']]*3},
 'stock_10':{'entry':0x365592,'steps':[['A']]*2},
 'stock_1c':{'entry':0x36565E,'steps':[['A']]*2},
 'stock_1b':{'entry':0x3656AC,'steps':[['A']]*3},
 'stock_1d':{'entry':0x3656B8,'steps':[['A']]*2},
 'stock_15':{'entry':0x365694,'steps':[['A']]*3},
 'stock_16':{'entry':0x3656A0,'steps':[['A']]*3},
 'stock_02':{'entry':0x365604,'steps':[['A']]*3},
}
for name,c in CASES.items():c['scope']='controlled item-help entry; no possession or natural use certified' if name.startswith('help_') or name=='water_guarded' else 'custom NPC shop wrapper forced; stock display only, no purchase certified'
m.CASES=CASES
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for n in ('rom','core','states-dir','out'):ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--profile',choices=('accents','ascii'),required=True);ap.add_argument('--version',choices=(77,78),type=int,default=78);m.run(ap.parse_args())
