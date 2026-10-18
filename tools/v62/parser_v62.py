"""Isolated script parser extension for the ROM-proven no-operand 1A 21.
The historical extraire module and its command table are never mutated.
"""
import importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('_ebb_parser_v62',ROOT/'atelier/outils/extraire.py')
parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
if 0x21 in parser.SUB[0x1A]:raise ValueError('Extension déjà définie dans le parseur historique')
parser.SUB[0x1A][0x21]=1 # Subcommand byte only; total length two bytes.
parse,length=parser.parse,parser.length

def spans_fr(raw):
 p=parse(raw,0,len(raw)+1,extra_glyphs=range(0xB0,0xC0))
 if p['error'] or not p['terminal'] or p['end']!=len(raw):raise ValueError('Contexte non fermé')
 spans=[];start=None;pos=0
 while pos<len(raw):
  c=raw[pos]
  if 0x50<=c<0xC0 or c in (0xC8,0xC9,0xCA,0xCB,0x15,0x16,0x17):
   if start is None:start=pos
   pos+=2 if c in (0x15,0x16,0x17) else 1
  else:
   if start is not None:spans.append((start,pos));start=None
   pos+=length(raw,pos)
 if start is not None:spans.append((start,pos))
 return spans

def commands(raw):
 out=bytearray();cursor=0
 for a,z in spans_fr(raw):out.extend(raw[cursor:a]);cursor=z
 out.extend(raw[cursor:]);return bytes(out)
