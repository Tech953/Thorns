'use strict';
window.renderOpenWorld=function(){
 const pane=$('openworld'),active=state.mode==='open';pane.hidden=!active;if(!active){$('choices').hidden=false;$('actorlabel').hidden=false;$('move-left').hidden=false;$('move-right').hidden=false;return;}
 const p=state.players.find(p=>p.id===session.id),o=p.overland,l=o.location,guide=p.field_guide?.enabled;
 document.body.dataset.region=l.region;
 $('region').textContent=l.region;$('title').textContent=l.title;$('story').textContent=l.text;
 $('cohesion').textContent=`HEALTH ${p.vitals.health}/100`;$('meter').max=100;$('meter').value=p.vitals.health;
 $('actorlabel').hidden=true;$('move-left').hidden=true;$('move-right').hidden=true;
 $('positions').textContent=state.players.map(q=>`${q.name}: [${q.grid}] · ${(Math.abs(q.grid[0]-p.grid[0])+Math.abs(q.grid[1]-p.grid[1]))*5} m · composure ${q.composure}`).join('\n');
 pane.replaceChildren(node('h2',`GRID [${p.grid}] / ${l.facility.toUpperCase()}`));
 pane.append(node('p',l.depth>=40?'REMOTE PERCEPT / UNVERIFIED SEMBLANCE · generated interpretation':'PROCEDURAL SURVEY / ADAPTED GEOGRAPHY · documented regional setting, generated site','survey-status'));
 const grid=node('div','','world-grid');grid.setAttribute('aria-label','Nearby grid, north at top');
 for(const t of o.tiles){const who=state.players.filter(q=>q.grid[0]===t.x&&q.grid[1]===t.y).map(q=>q.name).join(', ');const cell=node('div',`${t.x},${t.y}\n${t.facility}${who?'\n'+who:''}`,who?'occupied':'');cell.title=t.title;grid.append(cell);}pane.append(grid,node('p','LOCAL SURVEY · north ↑ · Manhattan distance · 5 m per tile · names mark occupied tiles','dim'));
 const buttons=node('div','','button-row');
 function button(label,op,data={},parent=buttons){const b=node('button',label);b.disabled=!state.started;b.onclick=()=>action(op,data);parent.append(b);}
 function contextLines(context){
  const lines=[];
  if(context?.livelihood?.length)lines.push(`LIVELIHOOD FIT / ${context.livelihood.join(', ')}`);
  if(context?.relationship)lines.push(`RELATIONSHIP THREAD / ${context.relationship}`);
  return lines;
 }
 function showContext(context,parent=pane){for(const line of contextLines(context))parent.append(node('p',`CONTEXT ONLY · ${line}`,'dim'));}
 for(const [label,dx,dy] of [['↑ NORTH',0,-1],['← WEST',-1,0],['EAST →',1,0],['↓ SOUTH',0,1]])button(label,'ow_move',{dx,dy});pane.append(buttons);
 pane.append(node('p',`${state.hardcore?'HARDCORE':'STANDARD'} · Hunger ${p.vitals.hunger} · Thirst ${p.vitals.thirst} · Sleep debt ${p.vitals.sleep} · Check penalty ${o.penalty}\nInjuries: ${p.vitals.injuries.join(', ')||'none'} · Ailments: ${p.vitals.ailments.join(', ')||'none'}\n${guide?'Energy '+p.vitals.energy+' · Scrap '+p.supplies.scrap:'Credits '+p.credits} · Karma ${p.karma} · Care benefit tier ${p.benefits}/3`));
 pane.append(node('h3','FIELD PROVISIONS'));const supplies=node('div','','button-row');for(const item of ['food','water','medkit']){button(`USE ${item} (${p.supplies[item]})`,'ow_consume',{item},supplies);button(guide?`LOCAL ${item} / ACTUAL STOCK`:`BUY ${item} (${item==='medkit'?6:2} cr)`,'ow_buy',{item},supplies);}pane.append(supplies);
 pane.append(node('h3','REST AND CARE'));const care=node('div','','button-row');button('REST / sanctuary','ow_rest',{},care);button(guide?'SANCTUARY / LOCAL CARE':'CLINIC / discounted care','ow_clinic',{},care);button('SCAVENGE / wilds, ruins','ow_scavenge',{},care);pane.append(care);
 if(l.depth<40){pane.append(node('h3',o.contact?`${o.contact.name} / LOCAL CONTACT`:'LOCAL CONTACT'));const dialogue=node('div','','button-row');for(const topic of ['place','needs','history','access','contracts','plans'])button(`ASK / ${topic.toUpperCase()}`,'ow_talk',{topic},dialogue);pane.append(dialogue);if(o.last_dialogue){pane.append(node('p',o.last_dialogue,'local-dialogue'));showContext(o.last_dialogue_context);if(o.last_dialogue_variation)pane.append(node('p',o.last_dialogue_variation,'local-context-variation'));if(contextLines(o.last_dialogue_context).length)pane.append(node('p','These links do not change replies, checks, standing, or access.','dim'));}}
 pane.append(node('h3','CONTRACT BOARD'));
 const contracts=node('div','','button-row');
 if(p.contract){
  pane.append(node('p',`${p.contract.kind} · target [${p.contract.target}] · ${p.contract.faction} · ${p.contract.reward}${guide?'':' credits + reputation + care discount'}`));
  showContext(p.contract.context);button('ATTEMPT SURVEY AT TARGET','ow_complete',{},contracts);button('ABANDON / -1 karma and reputation','ow_abandon',{},contracts);
 }else{
  const offer=o.contract_preview;
  if(offer){pane.append(node('p',`OFFER / ${offer.kind} · issuer ${offer.faction} · ${offer.description}`));showContext(offer.context);}
  button('ACCEPT SURVEY CONTRACT','ow_contract',{},contracts);
 }
 pane.append(contracts,node('p','Context links use whole-phrase livelihood terms and named issuer matches. They never change offer availability, checks, rewards, standing, or permissions.','dim'));
 const mods=node('details','');mods.append(node('summary',`BIO-MOD CLINIC / ${p.loadout.length}/3 slots`),node('p',guide?'Installation consumes two real scrap at a bounded craft service; removal is free.':'Installation costs 12 credits at a clinic or sanctuary; removal is free. These permits cover bounded prototype equipment only.'));
 for(const [id,m]of Object.entries(o.mods))button(`${p.loadout.includes(id)?'INSTALLED · REMOVE':guide?'INSTALL · 2 SCRAP':'INSTALL · 12 cr'} ${m.label} / ${m.skill}`,'ow_mod',{mod:id},mods);pane.append(mods);
 if(p.event){const e=p.event,box=node('section','','encounter');box.append(node('h3',e.title),node('p',`${e.body}\n${e.faction} · DC ${e.dc}`));showContext(e.context,box);e.approaches.forEach((a,i)=>button(`${a[0]} / ${a[1]} + ${a[2]}`,'ow_encounter',{choice:i},box));button('DECLINE ENCOUNTER','ow_encounter',{choice:3},box);pane.prepend(box);}
};
if(state)renderOpenWorld();
