"""Static credit preview using the actual compressed ROM font (not emulation).
Compression format: pk-hack/CoilSnake, exhal/compress.c at
346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a. No ROM is written.
"""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
import build_v60 as b

def decompress(data,start):
 p=start;out=bytearray()
 def get():
  nonlocal p
  v=data[p];p+=1;return v
 while True:
  head=get()
  if head==255:return bytes(out),p
  cmd=head>>5;n=(head&31)+1
  if cmd==7:cmd=(head>>2)&7;n=(((head&3)<<8)|get())+1
  if len(out)+n*(2 if cmd==2 else 1)>65536:raise ValueError('Bloc graphique trop long')
  if cmd==0:
   out.extend(data[p:p+n]);p+=n
  elif cmd==1:out.extend(bytes([get()])*n)
  elif cmd==2:
   a,z=get(),get();out.extend(bytes([a,z])*n)
  elif cmd==3:
   a=get();out.extend((a+i)&255 for i in range(n))
  else:
   q=get()*256+get()
   for i in range(n):
    v=out[q-i if cmd==6 else q+i]
    if cmd==5:v=int(f'{v:08b}'[::-1],2)
    out.append(v)

def font_from_rom(source):
 a=0x4F1A7;r=source[a:a+10]
 if r[0]!=0xA9 or r[3:6]!=b'\x85\x0e\xa9' or r[8:10]!=b'\x85\x10':raise ValueError('Chargeur de police divergent')
 p=int.from_bytes(r[1:3]+r[6:8],'little')-0xC00000;raw,end=decompress(source,p)
 if len(raw)!=192*16:raise ValueError('Taille de police divergente')
 palettes=[]
 for j in range(8):
  v=int.from_bytes(source[0x21E914+2*j:0x21E916+2*j],'little');palettes.append(((v&31)*255//31,((v>>5)&31)*255//31,((v>>10)&31)*255//31))
 palette_rows=[[1,1,0,1,0,0,0,1,0,0,0,0,1,1,1,1]]*2+[[1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1]]*2+[[1]*16]*8
 tiles=[]
 for i in range(192):
  im=Image.new('RGB',(8,8),'black')
  for y in range(8):
   for x in range(8):
    value=((raw[i*16+y*2]>>(7-x))&1)|(((raw[i*16+y*2+1]>>(7-x))&1)<<1)
    if value:im.putpixel((x,y),palettes[palette_rows[i//16][i%16]*4+value])
  tiles.append(im)
 return tiles,{'compressed_font_offset':f'{p:06X}','compressed_font_end':f'{end:06X}','decompressed_font_sha256':b.sha(raw),'font_tiles':192,'preview_palette':'ROM 21E914; tile palette assignments from pinned CoilSnake credits atlas; index 0 transparent on black'}

def render(raw,tiles,player='NINTEN'):
 entries,height,n=b.decode_staff(raw);im=Image.new('RGB',(256,height),'black');y=0
 for e in entries:
  if e['type']=='space':y+=e['rows']*8;continue
  kind='big' if e['type']=='player_name' else e['type'];text=player if e['type']=='player_name' else e['text'];x=(256-len(text)*8)//2
  for ch in text:
   index=b.MAPS[kind][ch]-64;im.paste(tiles[index],(x,y))
   if kind=='big':im.paste(tiles[index+16],(x,y+8))
   x+=8
  y+=16 if kind=='big' else 8
 assert y==height
 return im
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();source=a.rom.read_bytes();assert b.sha(source)==b.ROM_SHA;f=json.loads((b.ROOT/'tools/v60/v60_fixtures.json').read_text());tiles,meta=font_from_rom(source);old=render(bytes.fromhex(f['source_hex']),tiles);new=render(bytes.fromhex(f['translated_hex']),tiles);a.out.mkdir(exist_ok=True,parents=True)
 for page,start in enumerate(range(0,old.height,448),1):
  end=min(start+448,old.height);sheet=Image.new('RGB',(1032,(end-start)*2+48),(25,25,25));d=ImageDraw.Draw(sheet);d.text((10,5),'STATIC ROM FONT RECONSTRUCTION - NOT AN EMULATOR CAPTURE',fill='white');d.text((10,25),'V59 / ORIGINAL',fill='white');d.text((530,25),'V60 / FRANCAIS',fill='white')
  sheet.paste(old.crop((0,start,256,end)).resize((512,(end-start)*2),Image.Resampling.NEAREST),(0,48));sheet.paste(new.crop((0,start,256,end)).resize((512,(end-start)*2),Image.Resampling.NEAREST),(520,48));sheet.save(a.out/f'generique_{page}.png')
 (a.out/'preview_metadata.json').write_text(json.dumps({'method':'static_native_font_reconstruction','emulator_credits_run':False,'height':old.height,**meta},indent=2)+'\n')
