// Contrôles JavaScript et événements de l'éditeur avec un DOM simulé ; aucun test de rendu navigateur.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'atelier_fr.html'),'utf8');
const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
scripts.forEach(code=>new vm.Script(code));
class Element{
  constructor(tag='div'){this.tag=tag;this.children=[];this.value='';this.style={};this.disabled=false;this.readOnly=false;}
  append(...children){this.children.push(...children);}
  replaceChildren(...children){this.children=children;}
  click(){if(this.onclick)this.onclick();}
}
const elements={};
const document={getElementById:id=>elements[id]||(elements[id]=new Element()),createElement:tag=>new Element(tag)};
let exported='';
const context=vm.createContext({document,console,setTimeout:fn=>fn(),
  Blob:class{constructor(parts){this.text=parts.join('');}},
  URL:{createObjectURL:blob=>{exported=blob.text;return 'blob:test';},revokeObjectURL:()=>{}}});
vm.runInContext(scripts[0],context);vm.runInContext(scripts[1],context);
elements.mode.value='translation';
const {parseCSV,makeCSV,frenchBytes}=context.AtelierCore;
const fixture=[['a;b','quote "inside"','multi\nline'],['é','','last']];
assert.strictEqual(JSON.stringify(parseCSV(makeCSV(fixture))),JSON.stringify(fixture));
assert.strictEqual(frenchBytes('Non'),3);assert.strictEqual(frenchBytes('@École [8B]'),8);
assert.throws(()=>frenchBytes('[1F 02 74]'));assert.throws(()=>parseCSV('"abc'));
(async()=>{
  const folder=process.argv[2]||path.join(root,'build');
  const csv=fs.readFileSync(path.join(folder,'traductions.csv'),'utf8');
  const original=parseCSV(csv);
  assert.strictEqual(JSON.stringify(parseCSV(makeCSV(original))),JSON.stringify(original));
  await elements.csvFile.onchange({target:{files:[{name:'traductions.csv',text:async()=>csv}]}});
  assert(!elements.export.disabled);
  elements.search.value='380F4C';elements.search.oninput();
  assert.strictEqual(elements.list.children.length,6);elements.list.children[0].click();
  const initial=elements.french.value;
  elements.french.value='[1F 02 74]';elements.french.oninput();assert(elements.export.disabled);
  elements.reset.click();assert.strictEqual(elements.french.value,initial);
  elements.french.value='@Bonjour ! ';elements.french.oninput();assert(!elements.export.disabled);
  elements.export.click();
  const modified=parseCSV(exported);assert.strictEqual(modified.length,original.length);
  assert(modified.slice(1).some(row=>row[1]==='380F4C'&&row[2]==='0'&&row[4]==='@Bonjour ! '));
  for(let i=1;i<modified.length;i++)assert.deepStrictEqual(Array.from(modified[i].slice(0,4)),Array.from(original[i].slice(0,4)));
  const output=path.join(root,'tests/local_ui_v09');fs.mkdirSync(output,{recursive:true});
  fs.writeFileSync(path.join(output,'traductions_modifiees.csv'),exported);
  elements.search.value='15D4B2';elements.search.oninput();elements.list.children[0].click();
  elements.french.value='Le cauchemar';elements.french.oninput();assert(elements.export.disabled);
  elements.reset.click();assert(!elements.export.disabled);
  const catalogue=fs.readFileSync(path.join(folder,'couverture/catalogue.json'),'utf8');
  await elements.jsonFile.onchange({target:{files:[{name:'catalogue.json',text:async()=>catalogue}]}});
  elements.search.value='Pippi';elements.search.oninput();elements.list.children[0].click();
  assert(elements.french.disabled&&elements.reset.disabled);
  console.log('Éditeur : CSV, recherche, édition, suffixes PSI, commandes, rétablissement, export et catalogue OK (DOM simulé).');
})().catch(error=>{console.error(error);process.exit(1);});
