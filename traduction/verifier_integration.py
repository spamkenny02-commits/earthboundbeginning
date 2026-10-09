#!/usr/bin/env python3
"""Vérifications indépendantes des deux ROM reconstruites. Aucune validation d'émulation."""
import argparse,hashlib,json,struct,tempfile
from pathlib import Path
from integrer import ROOT,EXPECTED,ACCENT_CODES,BASES,FONT_SIZES,PROTECTED_TERMINATORS,encode_fr,glyph_decode

def apply_independent(source,patch):
    assert patch.startswith(b'PATCH')
    data=bytearray(source);pos=5
    while patch[pos:pos+3]!=b'EOF':
        addr=int.from_bytes(patch[pos:pos+3],'big');n=struct.unpack('>H',patch[pos+3:pos+5])[0];pos+=5
        if n:payload=patch[pos:pos+n];pos+=n
        else:
            n=struct.unpack('>H',patch[pos:pos+2])[0];payload=bytes([patch[pos+2]])*n;pos+=3
        assert len(payload)==n and addr+n<=len(data)
        data[addr:addr+n]=payload
    assert pos+3==len(patch)
    return bytes(data)

def verify(rom,build):
    raw=rom.read_bytes();source=raw[512:] if len(raw)%0x8000==512 else raw
    assert hashlib.sha256(source).hexdigest()==EXPECTED
    results={}
    menus={x['id']:x for x in json.loads((ROOT/'traduction/menus_objets_fr.json').read_text(encoding='utf-8'))}
    dialogues={x['id']:x for x in json.loads((ROOT/'traduction/dialogues_fr.json').read_text(encoding='utf-8'))}
    for profile in ['accents','ascii']:
        report=json.loads((build/f'rapport_{profile}.json').read_text(encoding='utf-8'));target=(build/f'EarthBound_Beginnings_FR_v05_{profile}.sfc').read_bytes();patch=(build/f'EarthBound_Beginnings_FR_v05_{profile}.ips').read_bytes()
        assert len(target)==len(source)==4194304
        for pos,ref,evidence in PROTECTED_TERMINATORS:
            assert target[pos]==source[pos]==0
            assert target[ref:ref+len(evidence)]==source[ref:ref+len(evidence)]==evidence
        assert apply_independent(source,patch)==target
        assert hashlib.sha256(target).hexdigest()==report['target_sha256']
        checksum=int.from_bytes(target[0xffde:0xffe0],'little');compl=int.from_bytes(target[0xffdc:0xffde],'little')
        assert checksum^compl==0xffff and sum(target)&0xffff==checksum
        assert target[0xffc0:0xffdc]==source[0xffc0:0xffdc]
        checked=0;stable_commands=0
        for change in report['accepted']:
            p=int(change['id'],16)
            if change['type']=='field':
                row=menus[change['id']];fr=encode_fr(row['text_fr'],profile=='accents');assert target[p:p+len(fr)]==fr
                if row['source'] in ('ITEM_CONFIGURATION_TABLE','ENEMY_CONFIGURATION_TABLE'):assert target[p+len(fr)]==0
                if row['source']=='ENEMY_CONFIGURATION_TABLE':
                    assert target[p-1]==0
                    assert target[p+25:p+93]==source[p+25:p+93], 'Stats ennemi modifiées'
            elif change['type']=='relocated_dialogue':
                from extraire import parse
                from compression import text_spans
                plan=json.loads((ROOT/'traduction/textes_relocalises_fr.json').read_text(encoding='utf-8'))
                row=next(r for r in plan['blocks'] if r['id']==change['id'])
                old=bytes.fromhex(row['raw_hex']);dest=int(change['offset'],16)
                new=bytearray(target[dest:dest+change['new_bytes']])
                assert target[p:p+len(old)]==source[p:p+len(old)]==old
                for ref in change['internal_refs']:
                    q=int(ref['offset'],16)-dest
                    assert new[q:q+4]==(0xc00000+int(ref['new_target'],16)).to_bytes(4,'little')
                    new[q:q+4]=(0xc00000+int(ref['old_target'],16)).to_bytes(4,'little')
                cursor=0;previous=0
                for seg in row['text_fr_segments']:
                    a,b=seg['offset'],seg['end'];gap=old[previous:a]
                    assert new[cursor:cursor+len(gap)]==gap;cursor+=len(gap)
                    fr=encode_fr(seg['french'],profile=='accents')
                    assert new[cursor:cursor+len(fr)]==fr;cursor+=len(fr);previous=b
                assert new[cursor:]==old[previous:]
                parsed=parse(bytes(new),0,len(new)+1)
                assert parsed['terminal'] and not parsed['error'] and parsed['end']==len(new)
            elif change['type']=='compressed_dialogue':
                rows=json.loads((ROOT/'traduction/textes_comprimes_fr.json').read_text(encoding='utf-8'))['blocks']
                row=next(r for r in rows if r['id']==change['id']);old=bytes.fromhex(row['raw_hex']);mask=bytearray(len(old))
                for seg in row['text_fr_segments']:
                    a,b=seg['offset'],seg['end'];fr=encode_fr(seg['french'],profile=='accents')
                    assert target[p+a:p+b]==fr.ljust(b-a,b'\x50');mask[a:b]=b'\1'*(b-a)
                assert all(target[p+i]==old[i] for i in range(len(old)) if not mask[i])
            elif change['type']=='dialogue':
                row=dialogues[change['id']];old=bytes.fromhex(row['raw_hex']);spans=row['text_fr_segments'];position=0
                for k,seg in enumerate(spans):
                    a=seg['offset']; b=spans[k+1]['offset'] if k+1<len(spans) else len(old)
                    # La longueur originale du fragment est calculée par son encodage source.
                    from extraire import encode
                    n=len(encode(seg['original']));fr=encode_fr(seg['french'],profile=='accents')
                    if change['stable_offsets_padding']:
                        assert target[p+a:p+a+len(fr)]==fr
                        assert target[p+a+len(fr):p+a+n]==b'\x50'*(n-len(fr))
                        stable_commands+=1
                    else:
                        assert fr in target[p:p+change['new_bytes']]
                if change['stable_offsets_padding']:
                    covered=set(j for seg in spans for j in range(seg['offset'],seg['offset']+len(encode(seg['original']))))
                    assert all(source[p+j]==target[p+j] for j in range(len(old)) if j not in covered)
            checked+=1
        for ref in report['relocation']['external_refs']:
            q=int(ref['offset'],16)
            assert source[q:q+4]==(0xc00000+int(ref['old_target'],16)).to_bytes(4,'little')
            assert target[q:q+4]==(0xc00000+int(ref['new_target'],16)).to_bytes(4,'little')
        glyphs=0
        for i,(w,h) in enumerate(FONT_SIZES):
            wp=int.from_bytes(source[0x3f054+i*12:0x3f058+i*12],'little')-0xc00000;gp=int.from_bytes(source[0x3f058+i*12:0x3f05c+i*12],'little')-0xc00000;size=w//8*h
            if profile=='ascii':
                assert source[gp:gp+128*size]==target[gp:gp+128*size]
                assert source[wp:wp+128]==target[wp:wp+128]
            else:
                assert source[gp:gp+96*size]==target[gp:gp+96*size]
                assert source[gp+112*size:gp+128*size]==target[gp+112*size:gp+128*size]
                for c,code in ACCENT_CODES.items():
                    pos=gp+(code-0x50)*size
                    assert source[pos:pos+size]==b'\xff'*size
                    assert target[pos:pos+size]!=b'\xff'*size
                    pixels=glyph_decode(target[pos:pos+size],w,h)
                    assert any(0 in row for row in pixels)
                    assert target[wp+code-0x50]==source[wp+ord(BASES[c])-0x20]
                    glyphs+=1
        # ROM de source avec en-tête copieur : le retrait reproduit exactement la même application.
        with_header=b'\0'*512+source
        assert apply_independent(with_header[512:],patch)==target
        results[profile]={'passed':True,'translations_checked':checked,'font_glyphs_checked':glyphs,'stable_fragment_positions_checked':stable_commands,'ips_reapplication':True,'headered_source_supported':True,'checksum_verified':True,'runtime_emulator_test':False}
    assert hashlib.sha256(rom.read_bytes()).hexdigest()==hashlib.sha256(raw).hexdigest()
    (build/'verification_integration.json').write_text(json.dumps(results,ensure_ascii=False,indent=2), encoding='utf-8');print(json.dumps(results,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('rom',type=Path);p.add_argument('--build',type=Path,default=ROOT/'build');a=p.parse_args();verify(a.rom,a.build)
