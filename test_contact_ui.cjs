'use strict';
// UI logic check of context-aside and legacy-fallback rendering using public state.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),{execFileSync}=require('node:child_process');
const bootstrap=`import json,server as s\ns.init_db(':memory:')\nh=s.mutate(dict(op='create',ruleset='legacy',name='Visitor',role='Light Reader',mode='open',procedural=False))\nr=s.fetch(h['code']);r['started']=True;s.save(r)\ns.mutate(dict(**h,op='ow_talk',topic='place',revision=r['revision']))\nr=s.fetch(h['code']);p=r['players'][0];p['character'].update(livelihood='field medic',relationship=r['contacts']['0,0']['faction']);s.save(r)\ns.mutate(dict(**h,op='ow_talk',topic='needs',revision=r['revision']))\nprint(json.dumps(dict(session={'id':h['id']},state=s.public(s.fetch(h['code'])))))\n`;
const fixture=JSON.parse(execFileSync(process.env.PYTHON||'python3',['-c',bootstrap],{cwd:__dirname,encoding:'utf8'}));
 const player=fixture.state.players[0],offer=player.overland.contract_preview;
 if(offer){offer.context={livelihood:['route/survey work'],relationship:'Embrite'};offer.variation='Narrative aside: Route-reading experience frames this survey.';}
 class Element{constructor(tag,text='',cls=''){this.tag=tag;this.textContent=text;this.className=cls;this.children=[];this.hidden=false;}append(...n){this.children.push(...n);}replaceChildren(...n){this.children=n;}prepend(...n){this.children.unshift(...n);}setAttribute(){}}
const ids=new Map(),calls=[];
const context={...fixture,window:{},document:{body:{dataset:{}}},node:(...args)=>new Element(...args),$:(id)=>{if(!ids.has(id))ids.set(id,new Element('div'));return ids.get(id);},action:(...args)=>calls.push(args)};
context.window=context;vm.createContext(context);vm.runInContext(fs.readFileSync(__dirname+'/static/openworld.js','utf8'),context);
function flatten(e){return[e,...e.children.flatMap(flatten)];}
const nodes=flatten(ids.get('openworld')),buttons=nodes.filter(n=>n.tag==='button'&&n.textContent.startsWith('ASK / '));
assert.equal(buttons.length,6);buttons[0].onclick();assert.equal(calls[0][0],'ow_talk');assert.equal(calls[0][1].topic,'place');
assert.ok(nodes.some(n=>n.className==='local-dialogue'&&n.textContent.includes('stated concern')));
assert.ok(nodes.some(n=>n.className==='local-context-variation'&&n.textContent.includes('Care work frames the concern')));
assert.ok(nodes.some(n=>n.className==='local-context-variation'&&n.textContent.includes('Route-reading experience frames this survey')));
assert.equal(nodes.filter(n=>n.textContent.startsWith('CONTEXT ONLY ·')).length,0,'authored asides replace duplicate context labels');
assert.ok(nodes.some(n=>n.textContent.includes('LOCAL CONTACT')));
fixture.state.players[0].overland.last_dialogue_variation='';
fixture.state.players[0].overland.contract_preview.variation='';
context.renderOpenWorld();
const legacyNodes=flatten(ids.get('openworld'));
assert.ok(legacyNodes.some(n=>n.className==='dim'&&n.textContent.includes('CONTEXT ONLY · LIVELIHOOD FIT / care work')),'older dialogue records retain the tag fallback');
assert.ok(legacyNodes.some(n=>n.className==='dim'&&n.textContent.includes('CONTEXT ONLY · LIVELIHOOD FIT / route/survey work')),'older contract previews retain the tag fallback');
fixture.state.players[0].overland.last_dialogue_variation='Narrative aside: Care work frames the concern.';
fixture.state.players[0].contract={kind:'Survey and return a verified route record',target:[2,1],faction:'Embrite',reward:18,context:{livelihood:['route/survey work'],relationship:'Embrite'},variation:'Narrative aside: Route-reading experience frames this brief.'};
fixture.state.players[0].event={title:'A delayed pilgrimage',body:'A small group waits at a route marker.',faction:'Embrite',dc:12,context:{livelihood:['route/survey work'],relationship:'Embrite'},variation:'Narrative aside: Route-reading experience frames the conflicting route references.',approaches:[['Listen','rapport','contracts']]};
context.renderOpenWorld();
const encounterNodes=flatten(ids.get('openworld'));
assert.equal(encounterNodes.filter(n=>n.textContent.startsWith('CONTEXT ONLY ·')).length,0,'contact, active contract and encounter asides replace duplicate labels');
assert.equal(encounterNodes.filter(n=>n.className==='local-context-variation').length,3,'contact, active contract and encounter each show one concise aside');
console.log('PASS: six dialogue topics, contract preview, active contract, encounter, legacy-label fallback and action wiring.');
