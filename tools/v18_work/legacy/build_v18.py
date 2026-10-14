from pathlib import Path
import sys,json,hashlib,unicodedata
sys.path.insert(0,'/mnt/data/v17_merge')
from fusionner_v17 import records,apply,sha,ROM_SHA
root=Path('/mnt/data'); rom=(root/'EarthBound Beginnings (USA) 1.2(1).sfc').read_bytes(); assert sha(rom)==ROM_SHA
candidates={e['id']:e for e in json.loads((root/'v18_candidates.json').read_text())}
fr={
'371EE3':'Quel idiot!',
'08F715':'*Halète*',
'33D3DB':'Je vois...',
'384384':'Ahahaha... oui!',
'364475':'Bon, tant pis.',
'3838CB':'C est bien aussi.',
'384396':'Reviens bientôt.',
'382186':'Merci beaucoup.',
'353D68':'Tu parles peu, hein?',
'360AB1':'Pas besoin de répondre, beauté.',
'36195C':'Je te croyais raisonnable.',
'34A8D8':'...Je... m en doutais un peu...',
'35457A':'Dis, reste boire un thé avec moi.',
'354665':'Un enfant ne connaît pas les peines de la vie...',
'3547E5':'Respecte tes aînés, ou tu le regretteras plus tard!',
'34AB18':'Les rubans magiques sont pour les filles magiques!'
}
# Keep only changes that fit both encodings, preserving original termination and all pointer bytes.
ACCENTS='éèêëàâîïôùûüçÉÀÇ'
def enc(s,accent):
 s=s.replace('’',"'")
 if not accent:s=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
 b=bytearray()
 for c in s:
  if accent and c in ACCENTS:b.append(0xB0+ACCENTS.index(c))
  elif 32<=ord(c)<=122 and c not in '"[\\]^':b.append(ord(c)+48)
  else:raise ValueError(repr(c))
 return bytes(b)
entries=[]
for ident,f in fr.items():
 c=candidates[ident];start=int(ident,16); n=c['length']-3
 for accent in (True,False):
  if len(enc(f,accent))>n:print('SKIP LENGTH',ident,len(enc(f,accent)),n);break
 else:entries.append({'id':ident,'english':c['english'],'fr':f,'refs':c['refs'],'length':c['length']})
print('accepted',len(entries),'out of',len(fr))
out=root/'v18_local';out.mkdir(exist_ok=True)
pointer_targets=set()
for at in range(len(rom)-3):
 if rom[at+3]==0 and 0xC0<=rom[at+2]<=0xFF:
  t=int.from_bytes(rom[at:at+4],'little')-0xC00000
  if 0<=t<len(rom):pointer_targets.add(t)
for profile in ('accents','ascii'):
 prior=(root/'v17_release'/f'EarthBound_Beginnings_FR_v17_{profile}.ips').read_bytes(); old=records(prior); used=bytearray(len(rom))
 for p,b in old:used[p:p+len(b)]=b'\1'*len(b)
 additions=[]
 for e in entries:
  p=int(e['id'],16);n=e['length'];assert rom[p]==0x70 and rom[p+n-2:p+n]==b'\x13\x02'
  assert rom[p+1:p+n-2]==bytes(ord(c)+48 for c in e['english'])
  assert not any(used[p:p+n]);assert all(rom[int(ref,16):int(ref,16)+4]==(0xC00000+p).to_bytes(4,'little') for ref in e['refs'])
  encoded=enc(e['fr'],profile=='accents'); raw=b'\x70'+encoded.ljust(n-3,b'\x50')+b'\x13\x02';assert len(raw)==n
  additions.append((p,raw))
 for i,(p,b) in enumerate(additions):
  assert all(not(p<q+len(d) and q<p+len(b)) for q,d in additions[:i])
  for target in range(p+1,p+len(b)):
   assert target not in pointer_targets, f'interior pointer {target:06x}'
 addon=bytearray()
 for p,b in additions:addon+=p.to_bytes(3,'big')+len(b).to_bytes(2,'big')+b
 merged=prior[:-3]+addon+b'EOF';assert records(merged)==old+additions
 target=apply(rom,records(merged));assert target==apply(apply(rom,old),additions)
 for p,b in old:assert target[p:p+len(b)]==apply(rom,old)[p:p+len(b)]
 (out/f'EarthBound_Beginnings_FR_v18_{profile}.ips').write_bytes(merged)
 print(profile,'ips',len(merged),'sha',sha(merged),'rom sha',sha(target))
(out/'v18_dialogues_fr.json').write_text(json.dumps({'version':'v18','base':'v17','entries':entries},ensure_ascii=False,indent=2)+'\n')
