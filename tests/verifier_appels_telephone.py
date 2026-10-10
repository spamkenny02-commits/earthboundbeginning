#!/usr/bin/env python3
"""Refuser un appel mal ciblé, un opcode altéré ou une position variable."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'traduction'))
from appels_telephone import apply_calls,pointer

old=b'\x08'+pointer(0x387a8c)+b'\x02'
calls=[{'block':'35C5D9','offset':'35C5DA','original_target':'387A8C','new_target':'31F260'}]
assert apply_calls('35C5D9',old,old,True,calls)==b'\x08'+pointer(0x31f260)+b'\x02'
assert apply_calls('35C7C8',old,old,False,calls)==old
for raw,stable in [(old,False),(b'\x0a'+old[1:],True),(b'\x08'+pointer(0x387ad2)+b'\x02',True)]:
    try:apply_calls('35C5D9',old,raw,stable,calls)
    except AssertionError:pass
    else:raise AssertionError('Appel non conforme accepté')
print('Positions fixes, opcode et cible originale contrôlés.')
