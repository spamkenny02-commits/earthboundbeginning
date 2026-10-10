"""Sous-programmes français réservés aux quatre appels du téléphone.

Les anciens sous-programmes anglais et leurs autres appelants sont conservés.
Les conditions de personnage/groupe reprennent les octets de la ROM vérifiée.
"""
import json
from pathlib import Path

def pointer(offset):
    return (0xc00000 + offset).to_bytes(4, 'little')

def prepare(original, write, encode, accents):
    plan=json.loads((Path(__file__).parent/'appels_telephone_fr.json').read_text(encoding='utf-8'))
    start,end=int(plan['region_start'],16),int(plan['region_end'],16)
    assert original[start:end]==bytes(end-start), 'Réserve téléphone non vide'
    targets={int.from_bytes(original[i:i+4],'little')-0xc00000 for i in range(len(original)-3)}
    assert not any(start<=p<end for p in targets), 'Réserve téléphone déjà référencée'
    for guard in plan['guards']:
        p=int(guard['offset'],16);raw=bytes.fromhex(guard['raw_hex'])
        assert original[p:p+len(raw)]==raw, 'Conditions de téléphone différentes'
    routines=[];by_id={};intervals=[]
    for row in plan['helpers']:
        dest=int(row['offset'],16)
        if row['kind']=='possessive':
            gate=bytearray(original[0x387a8c:0x387a97])
            first=encode(row['singular'],accents)+b'\x02'
            gate[7:11]=pointer(dest+len(gate)+len(first))
            second=encode(row['named_prefix'],accents)+original[0x387a9c:0x387a9f]+b'\x02'
            raw=bytes(gate)+first+second
        else:
            assert row['kind']=='party'
            gate=bytearray(original[0x387ad2:0x387ae4])
            first=encode(row['singular'],accents)+b'\x02'
            second=encode(row['plural'],accents)+b'\x02'
            alternate=dest+len(gate)+len(first)
            gate[5:9]=pointer(alternate);gate[14:18]=pointer(alternate)
            raw=bytes(gate)+first+second
        assert start<=dest<dest+len(raw)<=end
        assert not any(dest<b and a<dest+len(raw) for a,b in intervals)
        intervals.append((dest,dest+len(raw)));write(dest,raw,'telephone-'+row['id'])
        by_id[row['id']]=dest
        routines.append({'id':row['id'],'offset':f'{dest:06X}','raw_hex':raw.hex(' ')})
    calls=[]
    for row in plan['calls']:
        q=int(row['offset'],16);old=int(row['original_target'],16)
        assert original[q-1]==8 and original[q:q+4]==pointer(old)
        calls.append(dict(row,new_target=f"{by_id[row['helper']]:06X}"))
    return {'region_start':plan['region_start'],'region_end':plan['region_end'],'routines':routines,'calls':calls}

def apply_calls(block, old, translated, stable, calls):
    base=int(block,16);out=bytearray(translated)
    for row in calls:
        if row['block']!=block:continue
        assert stable, 'Appel contextuel exige des positions fixes'
        q=int(row['offset'],16)-base
        assert old[q-1]==8 and out[q-1]==8
        assert old[q:q+4]==out[q:q+4]==pointer(int(row['original_target'],16))
        out[q:q+4]=pointer(int(row['new_target'],16))
    return bytes(out)
