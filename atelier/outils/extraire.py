#!/usr/bin/env python3
"""Extraction prudente, sans modification de la ROM. Python 3, sans dépendances."""
import argparse
import bisect
import collections
import csv
import hashlib
import json
from pathlib import Path
import re

EXPECTED = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'
ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / 'outils/commandes.json').read_text(encoding='utf-8'))
BASE = {int(k): v for k, v in CFG['base'].items()}
SUB = {int(k): {int(a): n for a, n in v.items()} for k, v in CFG['sub'].items()}
SPECIAL = {0x52, 0x8B, 0x8C, 0x8D, 0x8E, 0xAB, 0xAC, 0xAD, 0xAE}
EXTRA_GLYPHS = {0xC8, 0xC9, 0xCA, 0xCB}  # Padding glyphs in train menus; preserve raw.

def render(raw):
    # Preserve special glyphs and literal brackets so decode/encode is unambiguous.
    return ''.join(chr(x - 48) if 0x50 <= x <= 0xAA and x not in SPECIAL
                   else f'[{x:02X}]' for x in raw)

def encode(text):
    out = bytearray()
    i = 0
    while i < len(text):
        if text[i] == '[':
            j = text.index(']', i)
            out.extend(bytes.fromhex(text[i + 1:j]))
            i = j + 1
        else:
            x = ord(text[i]) + 48
            if not 0x50 <= x <= 0xAA or x in SPECIAL:
                raise ValueError('Caractère non défini dans la TBL : ' + repr(text[i]))
            out.append(x)
            i += 1
    return bytes(out)

def length(b, p):
    c = b[p]
    if c not in BASE:
        raise ValueError(f'Opcode non défini {c:02X}')
    n = BASE[c]
    if n is not None:
        return n + 1
    s = b[p + 1]
    if c == 0x1A and s == 0x0C:
        callback = f"{int.from_bytes(b[p+2:p+6], 'little'):06X}"
        if callback not in CFG['asm_callbacks']:
            raise ValueError('Paramètres ASM inconnus : ' + callback)
        return 6 + CFG['asm_callbacks'][callback]
    if c == 9:
        return 2 + 4 * s
    if c == 0x1B:
        return 6 if s in (2, 3) else 2
    if c == 0x1E:
        return 6 if s == 9 else 4
    if c == 0x1F and s == 0xC0:
        return 3 + 4 * b[p + 2]
    if s not in SUB.get(c, {}):
        raise ValueError(f'Sous-commande non définie {c:02X} {s:02X}')
    return 1 + SUB[c][s]

def parse(b, start, max_bytes=8192):
    p = start
    parts, spans, targets, refs = [], [], [], []
    inline = False
    terminal = False
    error = ''
    try:
        while p < min(len(b), start + max_bytes):
            c = b[p]
            if 0x50 <= c <= 0xAE or c in EXTRA_GLYPHS:
                q = p + 1
                while q < len(b) and (0x50 <= b[q] <= 0xAE or b[q] in EXTRA_GLYPHS):
                    q += 1
                parts.append(render(b[p:q]))
                spans.append((p, q))
                p = q
                continue
            n = length(b, p)
            raw = b[p:p + n]
            if len(raw) != n:
                raise ValueError('Commande tronquée')
            parts.append('[' + raw.hex(' ').upper() + ']')
            locs = []
            if c in (8, 10): locs = [p + 1]
            elif c == 6: locs = [p + 3]
            elif c == 9: locs = list(range(p + 2, p + n, 4))
            elif c == 0x1A and raw[1] in (0, 1): locs = list(range(p + 2, p + 18, 4))
            elif c == 0x1B and raw[1] in (2, 3): locs = [p + 2]
            elif c == 0x1F and raw[1] == 0x63: locs = [p + 2]
            elif c == 0x1F and raw[1] == 0xC0: locs = list(range(p + 3, p + n, 4))
            for loc in locs:
                a = int.from_bytes(b[loc:loc + 4], 'little')
                if 0xC00000 <= a < 0x1000000:
                    targets.append(a - 0xC00000)
                    refs.append((loc, a - 0xC00000))
            p += n
            if c == 0x19 and raw[1] == 2:
                inline = True
            elif c == 2 and inline:
                inline = False
            elif c in (2, 10):
                terminal = True
                break
        if not terminal:
            error = 'Limite ou fin de ROM' if not error else error
    except (ValueError, IndexError) as e:
        error = str(e)
    return dict(start=start, end=p, text=''.join(parts), spans=spans,
                targets=targets, refs=refs, terminal=terminal, error=error)

def record(b, p, q, text, source, **extra):
    return dict(id=f'{p:06X}', offset=f'{p:06X}', snes=f'{p + 0xC00000:06X}',
                length=q-p, source=source, text_en=text, text_fr='',
                raw_hex=b[p:q].hex(' ').upper(), **extra)

def parse_scroller(b, p, limit):
    start=p
    parts=[]
    while p<limit:
        c=b[p]
        if c == 10:
            n=5  # Remake replaces original scrolling sequences with a long jump.
        elif c in (1,2,8):
            n=2
        elif c in (0,9):
            n=1
        elif 0x50<=c<=0xAE:
            parts.append(render(b[p:p+1]));p+=1;continue
        else:
            raise ValueError(f'Scroller : octet non défini {c:02X} à {p:06X}')
        if p+n>limit:raise ValueError('Scroller tronqué')
        parts.append('['+b[p:p+n].hex(' ').upper()+']');p+=n
        if c in (0,10):return record(b,start,p,''.join(parts),'scrolling_text')
    raise ValueError('Scroller sans fin')

def save_csv(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', delimiter=';')
        w.writeheader()
        w.writerows(rows)

def extract(rom, output):
    original = rom.read_bytes()
    header = 512 if len(original) % 0x8000 == 512 else 0
    b = original[header:]
    sha = hashlib.sha256(b).hexdigest()
    if sha != EXPECTED:
        raise ValueError('ROM différente de la version analysée : extraction refusée (SHA-256).')
    output.mkdir(parents=True, exist_ok=True)
    # Literal four-byte addresses: evidence, not proof of a runtime reference.
    ptrs = collections.defaultdict(list)
    for m in re.finditer(rb'(?=([\x00-\xff]{2}[\xc0-\xff]\x00))', b):
        p = int.from_bytes(m.group(1), 'little') - 0xC00000
        ptrs[p].append(m.start())
    seeds = set(p for p in ptrs if 0x339A82 <= p < 0x3A0000)
    seeds.add(0x339A85)
    seeds.discard(0x339A82)  # Tail of a 65816 instruction, immediately before the first visible line.
    # Additional inline entry candidates, kept separate from pointer evidence.
    for m in re.finditer(rb'\x02(?=[\x50-\xae]{4})', b[0x339A82:0x3A0000]):
        seeds.add(0x339A82 + m.start() + 1)
    # Cross-check independently located prose, including entry points reached via split ASM pointers.
    for m in re.finditer(rb'[\x50-\xae]{4,}', b[0x339A82:0x3A0000]):
        txt=render(m.group())
        if ' ' in txt and re.search('[a-z]{3}',txt):
            seeds.add(0x339A82+m.start())
    queue = collections.deque(sorted(seeds))
    parsed, commands = {}, collections.Counter()
    while queue:
        p = queue.popleft()
        if p in parsed or not 0x339A82 <= p < 0x3A0000:
            continue
        r = parse(b, p)
        parsed[p] = r
        if r['terminal']:
            queue.extend(r['targets'])
            if r['end'] < 0x3A0000:
                queue.append(r['end'])
    good = []
    issues = []
    for p, r in sorted(parsed.items()):
        readable = ''.join(render(b[a:z]) for a,z in r['spans'])
        if len(re.findall('[A-Za-z]', readable)) < 2:
            continue
        if not r['terminal']:
            issues.append(record(b,p,r['end'],r['text'],'partial_script', error=r['error']))
            continue
        # Long songs/dialogues legitimately contain many line breaks.
        if not re.search('[a-z]{3}|[A-Z][a-z]', readable):
            continue
        assert encode(r['text']) == b[p:r['end']], hex(p)
        good.append(record(b,p,r['end'],r['text'],'script_candidate',
                           literal_pointer_offsets=[f'{x:06X}' for x in ptrs.get(p,[])],
                           evidence='literal_pointer' if p in ptrs else 'sequential_or_inline'))
    # Remove sub-blocks already covered by an earlier parsed entry. All literal pointers are retained separately.
    blocks, end = [], -1
    for r in good:
        p = int(r['offset'],16)
        if p >= end:
            blocks.append(r)
            end = p + r['length']
    # Known fixed fields, validated before inclusion; relocated/invalid table locations are reported.
    fixed, rejected = [], []
    def add_fixed(p, size, source, label):
        if not 0 <= p < len(b):
            rejected.append(dict(source=source,label=label,reason='adresse hors ROM')); return
        raw = b[p:p+size].split(b'\x00')[0]
        if not raw or not all(0x50 <= x <= 0xAE for x in raw) or not re.search('[A-Za-z]',render(raw)):
            rejected.append(dict(source=source,label=label,offset=f'{p:06X}',reason='vide ou encodage incompatible'));return
        fixed.append(record(b,p,p+len(raw),render(raw),source,label=label,capacity_bytes=size))
    for f in CFG['fixed']:
        p=f.get('offset')
        if p is None:
            a=f['asm_pointers'][0]
            p=int.from_bytes(b[a+1:a+3]+b[a+6:a+8],'little')-0xC00000
        add_fixed(p,f['size'],'menu_field',f['group']+'/'+f['label'])
    for f in CFG['fields']:
        if f['table'] in ('FILE_SELECT_TEXT',): continue
        for i,p in enumerate(range(f['offset'],f['offset']+f['size'],f['stride'])):
            add_fixed(p+f['field_offset'],f['field_size'],f['table'],f"{i}/{f['field']}")
    fixed = list({r['id']:r for r in fixed}.values())
    # Dictionary: bank 0/1/2, each with 256 pointers. Preserve both pointer location and bytes.
    dictionary=[]
    for i in range(768):
        loc=0x8CDED+4*i
        p=int.from_bytes(b[loc:loc+4],'little')-0xC00000
        if not 0<=p<len(b):continue
        q=b.find(b'\x00',p,min(p+512,len(b)))
        if q<0 or not all(0x50<=x<=0xAE for x in b[p:q]):continue
        dictionary.append(record(b,p,q,render(b[p:q]),'compression_dictionary',
                                 code=f'{0x15+i//256:02X} {i%256:02X}',pointer_offset=f'{loc:06X}'))
    def readable(text):
        lookup={r['code']:r['text_en'] for r in dictionary}
        text=re.sub(r'\[(1[567] [0-9A-F]{2})\]',lambda m:lookup.get(m[1],m[0]),text)
        text=text.replace('[03][00]','\n').replace('[00]','\n').replace('[01]','\n\n')
        return text
    for r in blocks:r['reading_en']=readable(r['text_en'])
    # This literal is immediately followed by a different bytecode stream (25 ... 42 ...).
    # Keep its exact text bytes independently; do not invent a standard-script terminator.
    inline_text=[record(b,0x386E29,0x386E48,render(b[0x386E29:0x386E48]),
                        'inline_text_literal',script_boundary_verified=False)]
    # Preserve the original EarthBound text banks too, even if unused by the remake.
    legacy=[]
    legacy_issues=[]
    legacy_ranges=[(0x51B12,0x57FC1),(0x58000,0x5FFEC),(0x60000,0x67EEC),
        (0x68000,0x6FFE3),(0x70000,0x77F00),(0x78000,0x7FF40),(0x80000,0x87F23),
        (0x88000,0x8BC2D),(0x8D9ED,0x8FFF3),(0x90000,0x97FB3),(0x98000,0x9FF2F),
        (0x2F4E20,0x2FA37A)]
    for lo,hi in legacy_ranges:
        p=lo
        while p<hi:
            r=parse(b,p,min(8192,hi-p))
            if not r['terminal'] or r['end']>hi:
                legacy_issues.append(dict(offset=f'{p:06X}',region_end=f'{hi:06X}',error=r['error']))
                break
            row=record(b,p,r['end'],r['text'],'original_text_bank',runtime_use='unverified')
            row['reading_en']=readable(row['text_en'])
            assert encode(row['text_en'])==b[p:r['end']]
            legacy.append(row)
            p=r['end']
    # A new jump often overwrites only the first bytes of an old block; linear continuation
    # then starts in leftover bytes. Recover other entry points from literal pointers instead.
    legacy_seen={int(r['offset'],16) for r in legacy}
    for p in sorted(ptrs):
        if p in legacy_seen or not any(lo<=p<hi for lo,hi in legacy_ranges):continue
        hi=next(hi for lo,hi in legacy_ranges if lo<=p<hi)
        r=parse(b,p,min(8192,hi-p))
        if r['terminal'] and r['end']<=hi:
            row=record(b,p,r['end'],r['text'],'original_text_pointer_candidate',
                runtime_use='unverified',literal_pointer_offsets=[f'{x:06X}' for x in ptrs[p]])
            row['reading_en']=readable(row['text_en'])
            assert encode(row['text_en'])==b[p:r['end']]
            legacy.append(row)
    legacy.sort(key=lambda r:int(r['offset'],16))
    scrolling=[]
    scroll_issues=[]
    for lo,hi in [(0x210000,0x21064A),(0x210652,0x210B7E),(0x210005,0x21064A),
                  (0x210657,0x210B7E),(0x210B86,0x210C7A),
                  (0x38AD63,0x38AF70),(0x38AD64,0x38AF70),(0x38AF3D,0x38AF70)]:
        try:
            row=parse_scroller(b,lo,hi)
            row['reading_en']=row['text_en'].replace('[09]','\n')
            assert encode(row['text_en'])==b[lo:lo+row['length']]
            scrolling.append(row)
        except ValueError as e:scroll_issues.append(dict(offset=f'{lo:06X}',error=str(e)))
    intervals=sorted((int(r['offset'],16),int(r['offset'],16)+r['length']) for r in blocks+fixed+legacy+scrolling+inline_text)
    # Merge coverage before looking up fragments: overlapping fields cannot mask a larger interval.
    merged=[]
    for a,z in intervals:
        if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(z,merged[-1][1]))
        else:merged.append((a,z))
    intervals=merged
    starts=[x[0] for x in intervals]
    fragments=[]
    # Exhaustive byte-pattern inventory; not advertised as validated dialogue.
    for m in re.finditer(rb'[\x50-\xae]{2,}',b):
        txt=render(m.group())
        if not re.search('[A-Za-z]{2}',txt):continue
        p,q=m.span();k=bisect.bisect_right(starts,p)-1
        covered=k>=0 and intervals[k][0]<=p and q<=intervals[k][1]
        zone='remake_region' if 0x339A82<=p<0x3A0000 else 'other_or_inherited'
        fragments.append(record(b,p,q,txt,'raw_scan',zone=zone,
                                covered_by_export=covered,review_required=True))
    outputs={'dialogues.json':blocks,'champs_menus_objets_ennemis.json':fixed,
             'dictionnaire_compression.json':dictionary,'fragments_a_verifier.json':fragments,
             'scripts_partiels.json':issues,'champs_non_valides.json':rejected,
             'textes_integres_autre_bytecode.json':inline_text,
             'textes_banques_origine.json':legacy,'textes_defilants.json':scrolling,
             'erreurs_banques_origine.json':legacy_issues,'erreurs_defilants.json':scroll_issues}
    for name,rows in outputs.items():
        (output/name).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    fields=['id','offset','snes','length','source','label','text_en','text_fr']
    save_csv(output/'dialogues.csv',blocks,fields)
    save_csv(output/'menus_objets_ennemis.csv',fixed,fields+['capacity_bytes'])
    save_csv(output/'textes_banques_origine.csv',legacy,fields)
    save_csv(output/'textes_defilants.csv',scrolling,fields)
    save_csv(output/'textes_integres_autre_bytecode.csv',inline_text,fields)
    all_text=blocks+fixed+dictionary+legacy+scrolling+inline_text
    save_csv(output/'TOUS_LES_TEXTES.csv',all_text,fields)
    with (output/'TOUS_LES_TEXTES_lecture.txt').open('w',encoding='utf-8') as f:
        for r in sorted(all_text,key=lambda r:(int(r['offset'],16),r['source'])):
            f.write(f"\n=== {r['source']} / ROM ${r['offset']} / {r['length']} octets ===\n")
            f.write(r.get('reading_en',readable(r['text_en']))+'\n')
    with (output/'dialogues_lecture.txt').open('w',encoding='utf-8') as f:
        for r in blocks:
            f.write(f"\n=== ROM ${r['offset']} / SNES ${r['snes']} / {r['length']} octets ===\n{r['reading_en']}\n")
    supplements=[r for r in fragments if r['zone']=='remake_region'
                 and not r['covered_by_export'] and ' ' in r['text_en']
                 and len(re.findall('[a-z]',r['text_en'])) >= 12]
    save_csv(output/'fragments_remake_complementaires.csv',supplements,fields)
    # Publish the whole raw candidate inventory: short labels must not disappear because
    # they lack a sentence or a terminator. This is a coverage inventory, not a translation list.
    save_csv(output/'inventaire_rom_complet.csv',fragments,
             fields+['zone','covered_by_export','review_required'])
    remaining=[r for r in fragments if not r['covered_by_export']]
    save_csv(output/'fragments_hors_exports_structures.csv',remaining,
             fields+['zone','covered_by_export','review_required'])
    ascii_rows=[]
    for m in re.finditer(rb'[\x20-\x7e]{4,}',b):
        if re.search(rb'[A-Za-z]{3}',m[0]):
            ascii_rows.append(record(b,m.start(),m.end(),m[0].decode('ascii'),'raw_ascii_scan',review_required=True))
    (output/'inventaire_ascii_direct.json').write_text(json.dumps(ascii_rows,indent=2), encoding='utf-8')
    pointer_rows=[dict(target_offset=f'{p:06X}',snes=f'{p+0xC00000:06X}',
                       literal_offsets=[f'{x:06X}' for x in locs]) for p,locs in sorted(ptrs.items())
                  if 0x339A82<=p<0x3A0000]
    (output/'pointeurs_candidats.json').write_text(json.dumps(pointer_rows,indent=2), encoding='utf-8')
    stats=dict(rom_sha256=sha,rom_size=len(b),copier_header_bytes=header,
               dialogue_blocks=len(blocks),dialogue_bytes=sum(r['length'] for r in blocks),
               fixed_fields=len(fixed),dictionary_entries=len(dictionary),
               partial_scripts=len(issues),raw_fragments=len(fragments),
               original_bank_blocks=len(legacy),original_bank_errors=len(legacy_issues),
               scrolling_blocks=len(scrolling),scrolling_errors=len(scroll_issues),
               inline_text_literals=len(inline_text),
               supplementary_prose_fragments=len(supplements),
               raw_ascii_candidates=len(ascii_rows),
               all_detected_fragments_in_inventory=True,all_rom_text_proven=False,
               remake_fragments_uncovered=sum(r['zone']=='remake_region' and not r['covered_by_export'] for r in fragments),
               validated_runtime=False,rom_modified=False,
               roundtrip_verified_blocks=len(blocks))
    (output/'bilan.json').write_text(json.dumps(stats,indent=2), encoding='utf-8')
    print(json.dumps(stats,indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom',type=Path)
    parser.add_argument('--sortie',type=Path,default=ROOT/'extraction')
    args=parser.parse_args()
    extract(args.rom,args.sortie)
