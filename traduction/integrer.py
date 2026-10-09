#!/usr/bin/env python3
"""Première réinsertion française en place, avec contrôles structurels.
Python 3, bibliothèque standard uniquement. La ROM d'entrée n'est jamais modifiée.
"""
import argparse,bisect,hashlib,json,re,unicodedata
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'atelier/outils'))
from extraire import parse,render,EXPECTED
ACCENTS='éèêëàâîïôùûüçÉÀÇ'
ACCENT_CODES={c:0xb0+i for i,c in enumerate(ACCENTS)}
BASES=dict(zip(ACCENTS,'eeeeaaiiouuucEAC'))
# Le NUL de Row Back est aussi une chaîne vide chargée par le code C186CE.
PROTECTED_TERMINATORS=[(0x04550e,0x0186ce,bytes.fromhex('A9 0E 55 85 0A A9 C4 00 85 0C'))]
FONT_SIZES=[(16,16),(16,16),(8,16),(8,8),(16,16)]

def encode_fr(s,accents=True):
    s=s.replace('Œ','Oe').replace('œ','oe').replace('’',"'").replace('–','-').replace('…','...')
    if not accents:s=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
    raw=bytearray()
    for part in re.split(r'(\[(?:8B|8C|8D|8E|AB|AC|AD|AE)\])',s):
        if re.fullmatch(r'\[(?:8B|8C|8D|8E|AB|AC|AD|AE)\]',part):
            # Glyphes natifs : conserver les suffixes des PSI sans les redessiner.
            raw.append(int(part[1:-1],16));continue
        for c in part:
            if accents and c in ACCENT_CODES:raw.append(ACCENT_CODES[c])
            elif 0x20<=ord(c)<=0x7a and c not in '"[\\]^':raw.append(ord(c)+0x30)
            else:raise ValueError('Caractère non représentable : '+repr(c))
    return bytes(raw)

def glyph_decode(raw,w,h):
    return [[(raw[(x//8)*h+y]>>(7-x%8))&1 for x in range(w)] for y in range(h)]
def glyph_encode(tile,w,h):
    return bytes(sum(tile[y][x+j]<<(7-j) for j in range(8)) for x in range(0,w,8) for y in range(h))

def accented_tile(base,c,w,h):
    t=[row[:] for row in base]
    pts=[(x,y) for y in range(h) for x in range(w) if t[y][x]==0]
    if not pts:raise ValueError('Glyphe de base vide')
    xmin=min(x for x,y in pts);xmax=max(x for x,y in pts);ymin=min(y for x,y in pts);ymax=max(y for x,y in pts)
    mid=(xmin+xmax)//2
    if c in 'çÇ':
        y=min(ymax+1,h-1)
        for x in [mid,mid+1]: t[y][min(x,w-1)]=0
        if y+1<h:t[y+1][max(0,mid-1)]=0
        return t
    if ymin<2:
        # Police 8x8 : réserver deux lignes à l'accent en comprimant verticalement.
        t=[[1]*w for _ in range(h)]
        for y in range(2,h):
            sy=ymin+(y-2)*(ymax-ymin+1)//(h-2)
            for x in range(w):t[y][x]=base[min(sy,ymax)][x]
        y=0
    else:y=ymin-2
    if c in 'éÉ': points=[(mid+1,y),(mid,y+1)]
    elif c in 'èàùÀ':points=[(mid-1,y),(mid,y+1)]
    elif c in 'ëïü':points=[(mid-1,y),(mid+1,y)]
    else:points=[(mid,y),(mid-1,y+1),(mid+1,y+1)]
    for x,y in points:t[y][max(0,min(x,w-1))]=0
    return t

def patch_fonts(original,data,changes):
    records=[]
    for i,(w,h) in enumerate(FONT_SIZES):
        widths=int.from_bytes(original[0x3f054+i*12:0x3f058+i*12],'little')-0xc00000
        gfx=int.from_bytes(original[0x3f058+i*12:0x3f05c+i*12],'little')-0xc00000
        size=w//8*h
        for c,code in ACCENT_CODES.items():
            target=gfx+(code-0x50)*size
            before=original[target:target+size]
            if before!=b'\xff'*size:raise ValueError(f'Glyphe non libre : police {i}, {code:02X}')
            src=ord(BASES[c])-0x20
            base=glyph_decode(original[gfx+src*size:gfx+(src+1)*size],w,h)
            pixels=accented_tile(base,c,w,h); raw=glyph_encode(pixels,w,h)
            assert glyph_decode(raw,w,h)==pixels,'Échec aller-retour graphique'
            data[target:target+size]=raw
            data[widths+code-0x50]=original[widths+src]
            changes.extend([(target,target+size),(widths+code-0x50,widths+code-0x50+1)])
            records.append({'font':i,'character':c,'code':f'{code:02X}','offset':f'{target:06X}'})
    return records

def ips_patch(source,target):
    result=bytearray(b'PATCH');p=0
    while p<len(source):
        if source[p]==target[p]:p+=1;continue
        start=p
        while p<len(source) and source[p]!=target[p] and p-start<65535:p+=1
        result.extend(start.to_bytes(3,'big'));result.extend((p-start).to_bytes(2,'big'));result.extend(target[start:p])
    return bytes(result+b'EOF')
def apply_ips(source,patch):
    if patch[:5]!=b'PATCH':raise ValueError('Patch IPS invalide')
    data=bytearray(source);p=5
    while patch[p:p+3]!=b'EOF':
        offset=int.from_bytes(patch[p:p+3],'big');size=int.from_bytes(patch[p+3:p+5],'big');p+=5
        if not size:
            size=int.from_bytes(patch[p:p+2],'big');raw=bytes([patch[p+2]])*size;p+=3
        else:raw=patch[p:p+size];p+=size
        if len(raw)!=size or offset+size>len(data):raise ValueError('Patch tronqué ou hors ROM')
        data[offset:offset+size]=raw
    return bytes(data)

def integrate(rom,out,accents=True):
    src=rom.read_bytes();header=512 if len(src)%0x8000==512 else 0;original=src[header:]
    if hashlib.sha256(original).hexdigest()!=EXPECTED:raise ValueError('Mauvaise ROM source (SHA-256).')
    for pos,ref,evidence in PROTECTED_TERMINATORS:
        assert original[pos]==0 and original[ref:ref+len(evidence)]==evidence,'Référence de chaîne vide différente'
    data=bytearray(original);changes=[];report={'profile':'accents' if accents else 'ascii','source_sha256':EXPECTED,'accepted':[],'rejected':[]}
    targets=sorted(set(int.from_bytes(m[1],'little')-0xc00000 for m in re.finditer(rb'(?=([\x00-\xff]{2}[\xc0-\xff]\x00))',original)))
    patched_intervals=[]
    def write(p,raw,id):
        q=p+len(raw)
        if any(p<b and a<q for a,b in patched_intervals):raise ValueError('Chevauchement : '+id)
        data[p:q]=raw;changes.append((p,q));patched_intervals.append((p,q))
    rows=json.loads((ROOT/'traduction/menus_objets_fr.json').read_text(encoding='utf-8'))
    for row in rows:
        p=int(row['offset'],16);old=bytes.fromhex(row['raw_hex']);cap=row['capacity_bytes']
        assert original[p:p+len(old)]==old,'Champ source différent'
        raw=encode_fr(row['text_fr'],accents);terminated=original[p+len(old)]==0
        if row['source']=='ENEMY_CONFIGURATION_TABLE':
            # CoilSnake eb.yml : premier octet = The Flag ; nom de 25 octets, stride 94.
            assert cap==25 and (p-0x15958a)%94==0 and 0x15958a<=p<0x15958a+21714
            if len(raw)>=cap:raise ValueError('Nom ennemi trop long : '+row['id'])
            assert row.get('article_in_name') and original[p-1] in (0,1)
            write(p-1,b'\0',row['id']+'-article')
            encoded=(raw+b'\0').ljust(cap,b'\0')
        elif row['source']=='ITEM_CONFIGURATION_TABLE':
            # Table native vérifiée : nom de 25 octets au début d'un enregistrement de 39 octets.
            assert cap==25 and (p-0x155000)%39==0 and 0x155000<=p<0x157700
            if len(raw)>=cap: raise ValueError('Nom objet trop long : '+row['id'])
            encoded=(raw+b'\0').ljust(cap,b'\0')
        elif terminated:
            end=p+len(old)
            while end<p+cap and original[end]==0:end+=1
            allowed=end-p-1 if end>p+len(old) else len(old)
            if len(raw)>allowed:
                report['rejected'].append({'id':row['id'],'type':'field','reason':'capacité réelle insuffisante','needed':len(raw),'available':allowed,'english':row['text_en'],'french':row['text_fr']});continue
            encoded=raw+b'\0'
            if len(encoded)<=len(old)+1:encoded=encoded.ljust(len(old)+1,b'\0')
        else:
            allowed=len(old)
            if len(raw)>allowed:
                report['rejected'].append({'id':row['id'],'type':'field','reason':'champ fixe trop court','needed':len(raw),'available':allowed,'english':row['text_en'],'french':row['text_fr']});continue
            encoded=raw.ljust(allowed,b'\x50')
        if any(p<=zero<p+len(encoded) and encoded[zero-p]!=0 for zero,_,_ in PROTECTED_TERMINATORS):
            report['rejected'].append({'id':row['id'],'type':'field','reason':'terminateur partagé utilisé comme chaîne vide ; traduction trop longue'});continue
        write(p,encoded,row['id']);report['accepted'].append({'id':row['id'],'type':'field','english':row['text_en'],'french':row['text_fr'],'bytes':len(encoded)})
    rows=json.loads((ROOT/'traduction/dialogues_fr.json').read_text(encoding='utf-8'))
    for row in rows:
        p=int(row['offset'],16);old=bytes.fromhex(row['raw_hex']);parsed=parse(old,0,len(old)+1)
        assert original[p:p+len(old)]==old
        if not parsed['terminal'] or parsed['end']!=len(old):raise ValueError('Bloc non fermé : '+row['id'])
        # Un déplacement à l'intérieur d'un bloc ne doit invalider aucun point d'entrée.
        k=bisect.bisect_right(targets,p)
        stable_offsets=k<len(targets) and targets[k]<p+len(old)
        if stable_offsets and any(len(encode_fr(seg['french'],accents))>b-a for (a,b),seg in zip(parsed['spans'],row['text_fr_segments'])):
            report['rejected'].append({'id':row['id'],'type':'dialogue','reason':'pointeur intérieur et fragment français trop long ; relocation nécessaire'});continue
        outblock=bytearray();last=0;control_bytes=bytearray()
        assert len(row['text_fr_segments'])==len(parsed['spans'])
        for (a,b),seg in zip(parsed['spans'],row['text_fr_segments']):
            assert seg['offset']==a and seg['original']==render(old[a:b])
            controls=old[last:a];control_bytes.extend(controls);outblock.extend(controls)
            fragment=encode_fr(seg['french'],accents)
            if stable_offsets:fragment=fragment.ljust(b-a,b'\x50')
            outblock.extend(fragment);last=b
        outblock.extend(old[last:]);control_bytes.extend(old[last:])
        if len(outblock)>len(old):
            report['rejected'].append({'id':row['id'],'type':'dialogue','reason':'texte trop long ; relocation nécessaire','needed':len(outblock),'available':len(old)});continue
        # Relecture indépendante : retirer seulement les plages de texte, retrouver les commandes.
        check=bytes(outblock);p2=0;check_controls=bytearray();inline=False
        from extraire import length
        while p2<len(check):
            if 0x50<=check[p2]<=0xae or (accents and 0xb0<=check[p2]<=0xbf) or check[p2] in (0xc8,0xc9,0xca,0xcb):p2+=1;continue
            n=length(check,p2);check_controls.extend(check[p2:p2+n]);p2+=n
        assert check_controls==control_bytes,'Commandes modifiées : '+row['id']
        write(p,bytes(outblock).ljust(len(old),b'\0'),row['id']);report['accepted'].append({'id':row['id'],'type':'dialogue','old_bytes':len(old),'new_bytes':len(outblock),'stable_offsets_padding':stable_offsets})
    # Routines anglaises compressées : les codes 15/16/17 sont des références de texte.
    # Les commandes de jeu, paramètres et positions restent strictement identiques.
    from compression import text_spans,expand
    compressed=json.loads((ROOT/'traduction/textes_comprimes_fr.json').read_text(encoding='utf-8'))
    for entry in compressed['dictionary'].values():
        dp=int(entry['offset'],16);dr=bytes.fromhex(entry['raw_hex'])
        assert original[dp:dp+len(dr)]==dr,'Dictionnaire source différent'
    for row in compressed['blocks']:
        p=int(row['offset'],16);old=bytes.fromhex(row['raw_hex']);spans=text_spans(old)
        assert original[p:p+len(old)]==old
        assert len(spans)==len(row['text_fr_segments'])
        new=bytearray(old);mask=bytearray(len(old));too_long=False
        for (a,b),seg in zip(spans,row['text_fr_segments']):
            assert (a,b)==(seg['offset'],seg['end']) and expand(old[a:b],compressed['dictionary'])==seg['original']
            fr=encode_fr(seg['french'],accents)
            if len(fr)>b-a:too_long=True;break
            new[a:b]=fr.ljust(b-a,b'\x50');mask[a:b]=b'\1'*(b-a)
        if too_long:
            report['rejected'].append({'id':row['id'],'type':'compressed_dialogue','reason':'fragment comprimé trop court ; relocation requise'});continue
        assert all(new[i]==old[i] for i in range(len(old)) if not mask[i]),'Commande ou paramètre modifié'
        write(p,bytes(new),row['id']);report['accepted'].append({'id':row['id'],'type':'compressed_dialogue','old_bytes':len(old),'new_bytes':len(new),'commands_and_offsets_preserved':True})
    # Introduction du remake : conserver toutes les commandes de défilement, modifier uniquement les lignes.
    scroll=json.loads((ROOT/'traduction/introduction_fr.json').read_text(encoding='utf-8'))
    for row in scroll:
        p=int(row['offset'],16);old=bytes.fromhex(row['raw_hex']);text=row['text_en'];tokens=re.split(r'(\[[0-9A-F ]+\])',text)
        literals=[t for t in tokens if t and not t.startswith('[')]
        assert len(literals)==len(row['french_lines'])
        fr=iter(row['french_lines']);new=bytearray();controls=bytearray()
        for t in tokens:
            if not t:continue
            if t.startswith('['):r=bytes.fromhex(t[1:-1]);new.extend(r);controls.extend(r)
            else:new.extend(encode_fr(next(fr),accents))
        if len(new)>len(old):raise ValueError('Introduction trop longue')
        assert old[-1]==0 and new[-1]==0
        write(p,bytes(new).ljust(len(old),b'\0'),row['id']);report['accepted'].append({'id':row['id'],'type':'intro','old_bytes':len(old),'new_bytes':len(new)})
    from relocaliser import relocate
    moved,report['relocation']=relocate(original,write,encode_fr,accents)
    report['accepted'].extend(moved)
    report['font_glyphs']=patch_fonts(original,data,changes) if accents else []
    # Checksum HiROM. La somme des quatre octets checksum/complément reste 0x1FE.
    data[0xffdc:0xffe0]=b'\xff\xff\0\0';checksum=sum(data)&0xffff
    data[0xffdc:0xffde]=(checksum^0xffff).to_bytes(2,'little');data[0xffde:0xffe0]=checksum.to_bytes(2,'little');changes.append((0xffdc,0xffe0))
    assert sum(data)&0xffff==checksum
    allowed=bytearray(len(data))
    for a,b in changes:allowed[a:b]=b'\1'*(b-a)
    assert all(allowed[i] for i in range(len(data)) if original[i]!=data[i]),'Mutation hors plages autorisées'
    assert data[0xffc0:0xffdc]==original[0xffc0:0xffdc],'En-tête hors checksum modifié'
    patch=ips_patch(original,data);assert apply_ips(original,patch)==bytes(data),'Échec application IPS'
    assert all(data[pos]==0 for pos,_,_ in PROTECTED_TERMINATORS),'Chaîne vide partagée écrasée'
    report['protected_terminators']=[{'offset':f'{pos:06X}','reference':f'{ref:06X}','preserved':data[pos]==0} for pos,ref,_ in PROTECTED_TERMINATORS]
    report.update(target_sha256=hashlib.sha256(data).hexdigest(),source_rom_unchanged=hashlib.sha256(rom.read_bytes()).hexdigest()==hashlib.sha256(src).hexdigest(),rom_size=len(data),checksum=f'{checksum:04X}',accepted_count=len(report['accepted']),rejected_count=len(report['rejected']),bytes_changed=sum(a!=b for a,b in zip(original,data)),commands_preserved=True,ips_roundtrip_passed=True,runtime_validated=False)
    out.mkdir(parents=True,exist_ok=True);suffix='accents' if accents else 'ascii'
    (out/f'EarthBound_Beginnings_FR_v05_{suffix}.ips').write_bytes(patch)
    (out/f'rapport_{suffix}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2), encoding='utf-8')
    (out/f'EarthBound_Beginnings_FR_v05_{suffix}.sfc').write_bytes(data)
    print(json.dumps({k:report[k] for k in ['profile','accepted_count','rejected_count','bytes_changed','target_sha256','runtime_validated']},ensure_ascii=False,indent=2))
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('rom',type=Path);p.add_argument('--sortie',type=Path,default=ROOT/'build');p.add_argument('--sans-accents',action='store_true');p.add_argument('--appliquer',type=Path,help='Appliquer un patch IPS existant au lieu de construire la traduction')
    args=p.parse_args()
    if args.appliquer:
        src=args.rom.read_bytes();header=512 if len(src)%0x8000==512 else 0;src=src[header:]
        if hashlib.sha256(src).hexdigest()!=EXPECTED:raise ValueError('Mauvaise ROM source')
        result=apply_ips(src,args.appliquer.read_bytes());args.sortie.mkdir(parents=True,exist_ok=True);(args.sortie/'EarthBound_Beginnings_FR.sfc').write_bytes(result)
    else:integrate(args.rom,args.sortie,not args.sans_accents)
