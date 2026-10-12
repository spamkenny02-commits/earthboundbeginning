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
    regions=plan.get('regions',[{'id':'legacy','start':plan['region_start'],'end':plan['region_end']}])
    limits={r['id']:(int(r['start'],16),int(r['end'],16)) for r in regions}
    assert len(limits)==len(regions), 'Identifiants de réserve dupliqués'
    for first,last in limits.values():
        assert 0<=first<last<=len(original) and original[first:last]==bytes(last-first), 'Zone réservée non vide'
    ordered=sorted(limits.values())
    assert all(b<=c for (a,b),(c,d) in zip(ordered,ordered[1:])), 'Réserves qui se chevauchent'
    # Aucune adresse HiROM littérale ne vise la zone de réserve dans la source.
    assert not any(any(first<=int.from_bytes(original[i:i+4],'little')-0xc00000<last for first,last in limits.values()) for i in range(len(original)-3)), 'Zone déjà référencée'
    rows=plan['blocks'];ranges=[];built={};mapping={};cursors={key:a for key,(a,b) in limits.items()}
    for entry in plan['dictionary'].values():
        pos=int(entry['offset'],16);raw=bytes.fromhex(entry['raw_hex'])
        assert original[pos:pos+len(raw)]==raw
    for row in rows:
        pos=int(row['offset'],16);old=bytes.fromhex(row['raw_hex']);parsed=parse(old,0,len(old)+1)
        assert original[pos:pos+len(old)]==old and parsed['end']==len(old) and parsed['terminal'] and not parsed['error']
        ranges.append((pos,pos+len(old)));out=bytearray();prev=0;positions={0:0}
        spans=text_spans(old);assert len(spans)==len(row['text_fr_segments'])
        for (a,b),seg in zip(spans,row['text_fr_segments']):
            assert (a,b)==(seg['offset'],seg['end']) and expand(old[a:b],plan['dictionary'])==seg['original']
            # Les octets de commande et les frontières du texte ont une position exacte.
            for q in range(prev,a):positions[q]=len(out)+q-prev
            out.extend(old[prev:a]);positions[a]=len(out)
            out.extend(encode(seg['french'],accents));positions[b]=len(out);prev=b
        for q in range(prev,len(old)):positions[q]=len(out)+q-prev
        out.extend(old[prev:])
        region=row.get('region','legacy');cursor=cursors[region];last=limits[region][1]
        assert cursor+len(out)<=last, 'Réserve trop courte : '+row['id']
        built[pos]=(cursor,out);mapping[pos]=cursor
        if row.get('interior_policy')=='preserve_original_aliases':
            for ref,target in parsed['refs']:
                if pos<target<pos+len(old):
                    relative=target-pos
                    assert relative in positions, 'Cible dans un fragment de texte : '+row['id']
                    mapping[target]=cursor+positions[relative]
        cursors[region]=(cursor+len(out)+15)&~15
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
    # Les alias extérieurs restent dans les blocs originaux, toujours intacts.
    # Les nouvelles branches internes utilisent seulement les frontières vérifiées.
    preserved=[]
    policies={int(row['offset'],16):row.get('interior_policy','strict') for row in rows}
    for i in range(len(original)-3):
        target=int.from_bytes(original[i:i+4],'little')-0xc00000
        for a,b in ranges:
            if a<target<b:
                assert policies[a]=='preserve_original_aliases', 'Pointeur intérieur non pris en charge'
                if not any(c<=i<d for c,d in ranges):
                    preserved.append({'offset':f'{i:06X}','target':f'{target:06X}','block':f'{a:06X}'})
    accepted=[]
    for row in rows:
        pos=int(row['offset'],16);dest,out=built[pos]
        # Les arguments de commandes internes sont ajustés après le déplacement.
        parsed=parse(bytes(out),0,len(out)+1,extra_glyphs=range(0xb0,0xc0) if accents else ())
        assert parsed['terminal'] and not parsed['error'] and parsed['end']==len(out)
        internal=[]
        for ref,target in parsed['refs']:
            if target in mapping:
                out[ref:ref+4]=pointer(mapping[target]);internal.append({'offset':f'{dest+ref:06X}','old_target':f'{target:06X}','new_target':f'{mapping[target]:06X}'})
            else:assert not any(a<target<b for a,b in ranges)
        write(dest,bytes(out),row['id']+'-relocated')
        accepted.append({'id':row['id'],'type':'relocated_dialogue','offset':f'{dest:06X}','old_bytes':len(bytes.fromhex(row['raw_hex'])),'new_bytes':len(out),'original_preserved':True,'internal_refs':internal})
    return accepted, {'region_start':plan['region_start'],'region_end':plan['region_end'],
                      'used_end':f'{cursors["legacy"]:06X}',
                      'regions':[{**r,'used_end':f'{cursors[r["id"]]:06X}'} for r in regions],
                      'external_refs':refs,'preserved_original_aliases':preserved}
