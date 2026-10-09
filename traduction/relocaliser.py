"""Déplacement explicite de routines fermées et de leurs références HiROM.

Le plan est limité à des références connues et vérifiées dans la ROM source.
Les anciennes routines restent intactes. Aucun pointeur 16 bits n'est supposé.
"""
import json
from pathlib import Path
from extraire import parse
from compression import text_spans, expand

def pointer(pos):
    return (0xc00000 + pos).to_bytes(4, 'little')

def relocate(original, write, encode, accents):
    plan=json.loads((Path(__file__).parent/'textes_relocalises_fr.json').read_text(encoding='utf-8'))
    first,last=int(plan['region_start'],16),int(plan['region_end'],16)
    assert original[first:last]==bytes(last-first), 'Zone réservée non vide'
    # Aucune adresse HiROM littérale ne vise la zone de réserve dans la source.
    assert not any(first<=int.from_bytes(original[i:i+4],'little')-0xc00000<last for i in range(len(original)-3)), 'Zone déjà référencée'
    rows=plan['blocks'];ranges=[];built={};mapping={};cursor=first
    for entry in plan['dictionary'].values():
        pos=int(entry['offset'],16);raw=bytes.fromhex(entry['raw_hex'])
        assert original[pos:pos+len(raw)]==raw
    for row in rows:
        pos=int(row['offset'],16);old=bytes.fromhex(row['raw_hex']);parsed=parse(old,0,len(old)+1)
        assert original[pos:pos+len(old)]==old and parsed['end']==len(old) and parsed['terminal'] and not parsed['error']
        ranges.append((pos,pos+len(old)));out=bytearray();prev=0
        spans=text_spans(old);assert len(spans)==len(row['text_fr_segments'])
        for (a,b),seg in zip(spans,row['text_fr_segments']):
            assert (a,b)==(seg['offset'],seg['end']) and expand(old[a:b],plan['dictionary'])==seg['original']
            out.extend(old[prev:a]);out.extend(encode(seg['french'],accents));prev=b
        out.extend(old[prev:]);assert cursor+len(out)<=last
        built[pos]=(cursor,out);mapping[pos]=cursor;cursor=(cursor+len(out)+15)&~15
    # Les références entrantes sont une liste fermée : toute référence oubliée bloque.
    refs=[]
    for row in rows:
        pos=int(row['offset'],16);needle=pointer(pos);found=[];p=0
        while True:
            p=original.find(needle,p)
            if p<0:break
            found.append(p);p+=1
        assert found==sorted(int(x,16) for x in row['incoming_refs']), 'Références entrantes différentes'
        for ref in found:
            if not any(a<=ref<b for a,b in ranges):
                write(ref,pointer(mapping[pos]),f'ref-{ref:06X}')
                refs.append({'offset':f'{ref:06X}','old_target':f'{pos:06X}','new_target':f'{mapping[pos]:06X}'})
    # Un pointeur intérieur inattendu exige un plan plus précis, pas une supposition.
    for i in range(len(original)-3):
        target=int.from_bytes(original[i:i+4],'little')-0xc00000
        assert not any(a<target<b for a,b in ranges), 'Pointeur intérieur non pris en charge'
    accepted=[]
    for row in rows:
        pos=int(row['offset'],16);dest,out=built[pos]
        # Les arguments de commandes internes sont ajustés après le déplacement.
        parsed=parse(bytes(out),0,len(out)+1)
        assert parsed['terminal'] and not parsed['error'] and parsed['end']==len(out)
        internal=[]
        for ref,target in parsed['refs']:
            if target in mapping:
                out[ref:ref+4]=pointer(mapping[target]);internal.append({'offset':f'{dest+ref:06X}','old_target':f'{target:06X}','new_target':f'{mapping[target]:06X}'})
            else:assert not any(a<target<b for a,b in ranges)
        write(dest,bytes(out),row['id']+'-relocated')
        accepted.append({'id':row['id'],'type':'relocated_dialogue','offset':f'{dest:06X}','old_bytes':len(bytes.fromhex(row['raw_hex'])),'new_bytes':len(out),'original_preserved':True,'internal_refs':internal})
    return accepted, {'region_start':plan['region_start'],'region_end':plan['region_end'],'used_end':f'{cursor:06X}','external_refs':refs}
