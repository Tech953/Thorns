'use strict';
// UI logic check of the new contact controls using the server's actual public state.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),{execFileSync}=require('node:child_process');
const bootstrap=`import json,server as s\ns.init_db(':memory:')\nh=s.mutate(dict(op='create',ruleset='legacy',name='Visitor',role='Light Reader',mode='open',procedural=False))\nr=s.fetch(h['code']);r['started']=True;s.save(r)\ns.mutate(dict(**h,op='ow_talk',topic='place',revision=r['revision']))\nprint(json.dumps(dict(session={'id':h['id']},state=s.public(s.fetch(h['code'])))))\n`;
const fixture=JSON.parse(execFileSync(process.env.PYTHON||'python3',['-c',bootstrap],{cwd:__dirname,encoding:'utf8'}));
class Element{constructor(tag,text='',cls=''){this.tag=tag;this.textContent=text;this.className=cls;this.children=[];this.hidden=false;}append(...n){this.children.push(...n);}replaceChildren(...n){this.children=n;}setAttribute(){}}
const ids=new Map(),calls=[];
const context={...fixture,window:{},document:{body:{dataset:{}}},node:(...args)=>new Element(...args),$:(id)=>{if(!ids.has(id))ids.set(id,new Element('div'));return ids.get(id);},action:(...args)=>calls.push(args)};
context.window=context;vm.createContext(context);vm.runInContext(fs.readFileSync(__dirname+'/static/openworld.js','utf8'),context);
function flatten(e){return[e,...e.children.flatMap(flatten)];}
const nodes=flatten(ids.get('openworld')),buttons=nodes.filter(n=>n.tag==='button'&&n.textContent.startsWith('ASK / '));
assert.equal(buttons.length,6);buttons[0].onclick();assert.equal(calls[0][0],'ow_talk');assert.equal(calls[0][1].topic,'place');
assert.ok(nodes.some(n=>n.className==='local-dialogue'&&n.textContent.includes('generated')));
assert.ok(nodes.some(n=>n.textContent.includes('LOCAL CONTACT')));
console.log('PASS: six checked contact topics, persisted response, local-contact designation and action wiring.');
