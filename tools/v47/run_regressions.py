"""Run historical suites in isolated processes; set ROM_PATH to the original ROM."""
import os
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SUITES={
 'v47':('test_v47','test_v47_offline'),
 'v46':('test_v46','test_v46_offline','test_v46_prep'),
 'v45':('test_v45','test_v45_offline'),
 'v44':('test_v44','test_v44_offline'),
 'v43':('test_v43','test_v43_offline'),
 'v42':('test_v42','test_v42_offline'),
 'v41':('test_v41','test_v41_offline'),
 'v40':('test_v40','test_v40_offline'),
 'v39':('test_v39','test_v39_offline'),
 'v38':('test_v38','test_v38_offline'),
 'v37':('test_v37_offline',),'v36':('test_v36_offline',),
 'v35':('test_v35','test_v35_offline'),'v34':('test_v34',),
 'v33':('test_v33_rom','test_v33_offline'),
 'v29':('test_v29_rom','test_v29_offline'),'boy_girl':('test_boy_girl',),
}
if not os.environ.get('ROM_PATH'):
    raise SystemExit('ROM_PATH must point to the original USA 1.2 ROM')
failed=[]
for folder,tests in SUITES.items():
    print('\nSuite '+folder,flush=True)
    proc=subprocess.run([sys.executable,'-m','unittest',*tests,'-q'],cwd=ROOT/'tools'/folder)
    if proc.returncode:failed.append(folder)
if failed:raise SystemExit('Failed suites: '+', '.join(failed))
