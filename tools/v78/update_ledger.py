"""Generate the distinct-source ledger, retaining original implantation offsets."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def build():
 f=json.loads((ROOT/'tools/v78/v78_fixtures.json').read_text());entries={}
 def add(en,fr,a):
  e=entries.setdefault(en,{'source':en,'french':fr,'offsets':[],'validation':'static; runtime coverage is case-specific'})
  if e['french']!=fr:
   variants=e.setdefault('translations',[{'french':e['french'],'offsets':list(e['offsets'])}]);v=next((v for v in variants if v['french']==fr),None)
   if v is None:v={'french':fr,'offsets':[]};variants.append(v)
   v['offsets'].append(a);e['french']=' / '.join(v['french'] for v in variants)
  e['offsets'].append(a)
 for e in f['profiles']['accents']['edits']:add(e['english'],e['french'],e['offset'])
 for e in f['menus']:add('No','Non',e['no_definition'])
 for e in f['medical']['entries']:add(e['en'],e['fr'],e['offset'])
 for e in f['medical']['menus']:add('No','Non',e['offset'])
 for e in f['remaining']['entries']:add(e['en'],e['fr'],e['offset'])
 for e in f['remaining']['labels']:add(e['en'],e['fr'],e['offset'])
 for e in f.get('item_help',{}).get('entries',[]):add(e['en'],e['fr'],e['offset'])
 for e in f.get('scoped_help',{}).get('entries',[]):add(e['en'],e['fr'],e['offset'])
 for e in f.get('context_grammar',{}).get('entries',[]):add(e['en'],e['fr'],e['offset'])
 for e in f.get('phone_label',{}).get('entries',[]):add(e['en'],e['fr'],e['offset'])
 for e in f['remaining']['menus']+f['remaining']['moved_scripts']:add('Yes','Oui',e['yes']);add('No','Non',e['no_definition'])
 rows=sorted(entries.values(),key=lambda e:min(e['offsets']));plan=json.loads((ROOT/'tools/v78/validation_v78.json').read_text());assert len(rows)==plan['distinct_new_translations'];assert sum(len(e['offsets']) for e in rows)==plan['changed_text_spans']
 return {'version':'v78','release_pending':True,'distinct_texts':len(rows),'physical_spans':plan['changed_text_spans'],'target':150,'entries':rows}
if __name__=='__main__':
 result=build();(ROOT/'tools/v78/batch_ledger.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['distinct_texts'],result['physical_spans'])
