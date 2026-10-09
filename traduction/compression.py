"""Plages de texte comprenant les références au dictionnaire anglais (15/16/17).
Ces références produisent du texte ; les commandes de jeu restent hors des plages.
"""
from extraire import length,parse,render

def text_spans(raw):
    parsed=parse(raw,0,len(raw)+1)
    if not parsed['terminal'] or parsed['end']!=len(raw) or parsed['error']:
        raise ValueError('Routine de texte non fermée')
    spans=[];start=None;pos=0
    while pos<len(raw):
        c=raw[pos]
        if 0x50<=c<=0xae or c in (0xc8,0xc9,0xca,0xcb,0x15,0x16,0x17):
            if start is None:start=pos
            pos+=2 if c in (0x15,0x16,0x17) else 1
        else:
            if start is not None:spans.append((start,pos));start=None
            pos+=length(raw,pos)
    if start is not None:spans.append((start,pos))
    return spans

def expand(raw,dictionary):
    out=[];p=0
    while p<len(raw):
        if raw[p] in (0x15,0x16,0x17):
            out.append(dictionary[raw[p:p+2].hex(' ').upper()]['text_en']);p+=2
        else:out.append(render(raw[p:p+1]));p+=1
    return ''.join(out)
