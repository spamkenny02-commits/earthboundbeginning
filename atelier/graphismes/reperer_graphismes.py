#!/usr/bin/env python3
"""Extraction en lecture seule. Dépendance : CoilSnake (avec native_comp), Pillow.
Usage : python reperer_graphismes.py ROM.sfc dossier_sortie chemin_CoilSnake
"""
import sys, json, hashlib, traceback
from pathlib import Path
sys.path.insert(0, sys.argv[3])
from coilsnake.model.common.blocks import Block
from coilsnake.model.eb.blocks import EbCompressibleBlock
from coilsnake.model.eb.graphics import EbTileArrangement, EbGraphicTileset
from coilsnake.model.eb.palettes import EbPalette
from coilsnake.model.eb.map_tilesets import EbTileset
from coilsnake.util.eb.pointer import read_asm_pointer, from_snes_address
from coilsnake.modules.eb.CompressedGraphicsModule import CompressedGraphicsModule
from coilsnake.modules.eb.TitleScreenModule import TitleScreenModule
from coilsnake.modules.eb.WindowGraphicsModule import WindowGraphicsModule
from coilsnake.modules.eb.DeathScreenModule import DeathScreenModule
from coilsnake.modules.eb.SoundStoneModule import SoundStoneModule
from coilsnake.modules.eb.SpriteGroupModule import SpriteGroupModule
from coilsnake.modules.eb.StaffModule import StaffModule
from coilsnake.model.eb.fonts import EbCreditsFont
from coilsnake.model.eb.sprites import SpriteGroup
from PIL import Image, ImageDraw

rompath=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
rom=Block(); rom.from_file(str(rompath))
manifest={'rom_sha256':hashlib.sha256(rompath.read_bytes()).hexdigest(),'assets':[], 'errors':[]}
def ptr(p): return from_snes_address(read_asm_pointer(rom,p))
def resource(name, ext, text=False):
    p=out/(name+'.'+ext); p.parent.mkdir(parents=True,exist_ok=True)
    return p.open('w' if text else 'wb')
def run(name, cls):
    try:
        m=cls()
        if name=='sprites':
            table=ptr(0x1df9)
            m.group_pointer_table.from_block(rom,table)
            m.palette_table.from_block(rom,0x30000)
            m.groups=[]
            for i in range(m.group_pointer_table.num_rows):
                gp=m.group_pointer_table[i][0]
                count=8 if i==m.group_pointer_table.num_rows-1 else (m.group_pointer_table[i+1][0]-gp-9)//2
                if not 0<=count<=16: raise ValueError(f'Nombre de sprites incoherent groupe {i}: {count}')
                group=SpriteGroup(count); group.from_block(rom,from_snes_address(gp)); m.groups.append(group)
                off=from_snes_address(gp)
                frames=[f'{from_snes_address(((rom[off+8]<<16)|rom.read_multi(off+9+j*2,2))&0xfffffc):06X}' for j in range(count)]
                manifest['assets'].append({'id':f'sprite_{i:03d}','image':f'SpriteGroups/{i:03d}.png','group_file_offset':f'{off:06X}','frame_graphics_file_offsets':frames,'sprite_pointer_table_file_offset':f'{table:06X}'})
        elif name=='titre':
            m.read_background_data_from_rom(rom); m.read_chars_data_from_rom(rom)
            m.bg_palette[0,128:144]=m.chars_anim_palette.get_subpalette(13)[0,:]
        else: m.read_from_rom(rom)
        if name=='titre':
            m.write_background_data_to_project(resource)
            # Le hack a déplacé la disposition des objets du titre. Export brut fiable.
            ar=EbTileArrangement(32,32)
            for k in range(1024): ar[k%32,k//32].tile=k
            with resource('TitleScreen/Objets/atlas_brut','png') as f:
                ar.image(m.chars_tileset,m.chars_anim_palette.get_subpalette(13)).save(f)
            manifest['title_object_layout_status']='Disposition spécifique au hack non reconstruite ; atlas brut seulement.'
        else: m.write_to_project(resource)
        print(name,'OK',flush=True)
    except Exception as e:
        manifest['errors'].append({'module':name,'error':str(e)})
        traceback.print_exc()
for n,c in [('ecrans_logos_cartes',CompressedGraphicsModule),('titre',TitleScreenModule),('fenetres',WindowGraphicsModule),('defaite',DeathScreenModule),('melodies',SoundStoneModule)]: run(n,c)
run('sprites',SpriteGroupModule)
run('credits_texte',StaffModule)
try:
    f=EbCreditsFont(); f.from_block(rom,0x4f1a7,0x21e914)
    with resource('Polices/credits','png') as target: f.to_files(target)
except Exception as e: manifest['errors'].append({'module':'credits_police','error':str(e)})

# Atlas des 20 banques de décor : les enseignes sont composées de blocs de 32x32.
for i in range(20):
    try:
        g=from_snes_address(rom.read_multi(0x2f105b+i*4,4)); a=from_snes_address(rom.read_multi(0x2f10ab+i*4,4))
        t=EbTileset(); t.minitiles_from_block(rom,g); t.arrangements_from_block(rom,a)
        mapid=next(j for j in range(32) if rom.read_multi(0x2f101b+j*2,2)==i)
        po=from_snes_address(rom.read_multi(0x2f10fb+mapid*4,4))
        pal=EbPalette(6,16); pal.from_block(rom,po)
        for sp in pal.subpalettes: sp[0].r=sp[0].g=sp[0].b=0
        ar=EbTileArrangement(64,256)
        count=0
        for k,v in enumerate(t.arrangements):
            if v is None: continue
            count+=1
            for y in range(4):
                for x in range(4):
                    val=v[y][x]; item=ar[(k%16)*4+x,(k//16)*4+y]
                    item.tile=val&1023; item.subpalette=(val>>10)&7
                    item.is_horizontally_flipped=bool(val&0x4000); item.is_vertically_flipped=bool(val&0x8000)
        p=out/f'Decors/atlas_{i:02d}.png'; p.parent.mkdir(exist_ok=True)
        ar.image(t.minitiles,pal).save(p)
        (out/f'Decors/arrangements_{i:02d}.json').write_text(json.dumps(t.arrangements))
        manifest['assets'].append({'id':f'decor_{i:02d}','image':str(p.relative_to(out)),'graphics_file_offset':f'{g:06X}','arrangement_file_offset':f'{a:06X}','palette_file_offset':f'{po:06X}','map_palette_id':mapid,'arrangements':count,'bpp':4,'compressed':True})
        print('decor',i,'OK',count,flush=True)
    except Exception as e:
        manifest['errors'].append({'module':f'decor_{i:02d}','error':str(e)}); traceback.print_exc()

# Polices brutes : ne pas effacer les caractères 96–127 comme le fait l'export standard.
for i,(w,h) in enumerate([(16,16),(16,16),(8,16),(8,8),(16,16)]):
    try:
        wp=from_snes_address(rom.read_multi(0x3f054+i*12,4)); gp=from_snes_address(rom.read_multi(0x3f058+i*12,4))
        ts=EbGraphicTileset(128,w,h); ts.from_block(rom,gp,bpp=1)
        ar=EbTileArrangement(16,8)
        for k in range(128): ar[k%16,k//16].tile=k
        pal=EbPalette(1,2); pal.from_list([0,0,0,255,255,255])
        p=out/f'Polices/police_{i}.png'; p.parent.mkdir(exist_ok=True)
        ar.image(ts,pal).save(p)
        manifest['assets'].append({'id':f'police_{i}','image':str(p.relative_to(out)),'graphics_file_offset':f'{gp:06X}','widths_file_offset':f'{wp:06X}','bpp':1,'compressed':False})
    except Exception as e: manifest['errors'].append({'module':f'police_{i}','error':str(e)})

locations=[('titre_fond',0xebf2,0xec1d,0xecc6),('titre_lettres',0xec49,None,0x3f492),('Nintendo',0xeea3,0xeebb,0xeed3),('APE',0xeefb,0xef13,0xef2b),('HALKEN',0xef52,0xef6a,0xef82),('ProducedBy',0x4dd73,0x4dd3a,0x4dd9f),('PresentedBy',0x4de1b,0x4dde2,0x4de47),('GasStation',0xf0f0,0xf11b,0xf147),('fenetres_1',0x47c47,None,None),('fenetres_2',0x47caa,None,None),('defaite',0x4c32f,0x4c388,0x4c3c3),('melodies',0x4acf0,None,None),('icones_cartes',0x4d62f,None,0x4d5c4)]
for name,g,a,p in locations:
    item={'id':name,'graphics_file_offset':f'{ptr(g):06X}','graphics_asm_pointer_location':f'{g:06X}'}
    if a is not None: item['arrangement_file_offset']=f'{ptr(a):06X}'
    if p is not None: item['palette_file_offset']=f'{ptr(p):06X}'
    manifest['assets'].append(item)
for i in range(6): manifest['assets'].append({'id':f'carte_{i}','combined_file_offset':f'{from_snes_address(rom.read_multi(0x202190+i*4,4)):06X}','compressed':True})
(out/'inventaire_technique.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('FIN',len(list(out.rglob('*.png'))),'PNG;',len(manifest['errors']),'erreurs',flush=True)
