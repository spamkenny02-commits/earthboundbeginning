"""Protect sprite footprints and allocate only within original expansion padding.
Format: CoilSnake 346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a, model/eb/sprites.py.
"""
import hashlib,re
POOL_LO,POOL_HI=0x328A70,0x331000
SPRITE_TABLE,GROUPS=0x1F840A,464

def sprite_ranges(data):
    raw=data[0x1DF9:0x1E03]
    if raw[:1]!=b'\xa9' or raw[3:6]!=b'\x85\x0a\xa9' or raw[8:10]!=b'\x85\x0c':raise ValueError('Référence assembleur des sprites divergente')
    table=int.from_bytes(raw[1:3]+raw[6:8],'little')-0xC00000
    if table!=SPRITE_TABLE:raise ValueError('Table des sprites divergente')
    ranges=[(table,table+GROUPS*4)];frames=0
    for i in range(GROUPS):
        a=int.from_bytes(data[table+4*i:table+4*i+4],'little')-0xC00000
        next_a=int.from_bytes(data[table+4*i+4:table+4*i+8],'little')-0xC00000 if i+1<GROUPS else a+25
        if (next_a-a-9)%2:raise ValueError('Description sprite non alignée')
        count=(next_a-a-9)//2
        if not 0<=count<=16 or not 0<=a<a+9+count*2<=len(data):raise ValueError('Description sprite invalide')
        ranges.append((a,a+9+count*2));h,w=data[a],data[a+1]>>4
        if count and not (0<h<=16 and 0<w<=16):raise ValueError('Dimensions sprite invalides')
        for j in range(count):
            pointer=((data[a+8]<<16)|int.from_bytes(data[a+9+j*2:a+11+j*2],'little'))&0xFFFFFC
            lo=pointer-0xC00000;hi=lo+w*h*32
            if not 0<=lo<hi<=len(data):raise ValueError('Image sprite hors ROM')
            ranges.append((lo,hi));frames+=1
    return ranges,frames

def sprite_digest(data):
    ranges,frames=sprite_ranges(data);digest=hashlib.sha256()
    for a,z in ranges:digest.update(data[a:z])
    return digest.hexdigest()

def safe_reserves(source,bases,priors,targets,records):
    if source[POOL_LO:POOL_HI]!=bytes(POOL_HI-POOL_LO):raise ValueError('Zone de remplissage divergente')
    mask=bytearray(len(source));frames=None
    for data in [source,*bases.values()]:
        ranges,frames=sprite_ranges(data)
        for a,z in ranges:mask[a:z]=b'\1'*(z-a)
    for ips in priors.values():
        for a,raw in records(ips):mask[a:a+len(raw)]=b'\1'*len(raw)
    for t in targets:
        if 0<=t<len(mask):mask[t]=1
    safe=bytes(not mask[i] and all(data[i]==0 for data in bases.values()) for i in range(POOL_LO,POOL_HI))
    reserves=[]
    for match in re.finditer(b'\1{8,}',safe):
        a=(POOL_LO+match.start()+3)&~3;z=POOL_LO+match.end()
        if z-a>=8:reserves.append([a,z])
    reserves.sort(key=lambda r:(-(r[1]-r[0]),r[0]))
    return reserves,{'padding_bounds':[f'{POOL_LO:06X}',f'{POOL_HI:06X}'],'sprite_groups':GROUPS,'sprite_frames':frames,'baseline_sprite_sha256':{p:sprite_digest(data) for p,data in bases.items()}}
