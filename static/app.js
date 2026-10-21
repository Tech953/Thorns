'use strict';
const $=id=>document.getElementById(id);
let session=null,state=null,busy=false,lastRender='';
try{session=JSON.parse(sessionStorage.getItem('thorns-session'));}catch{}
function error(e){$('error').textContent=e?.message||'';}
function node(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e;}
const lobbySkip=node('a','SKIP TO LOBBY ↓','lobby-skip');lobbySkip.href='#lobby';Array.from($('builder').children).find(e=>e.tagName==='H2')?.after(lobbySkip);$('lobby').tabIndex=-1;
async function api(op,data={}){const response=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...session,op,...data}),signal:AbortSignal.timeout(10000)});const r=await response.json();if(!response.ok)throw Error(r.error||'Connection failed');return r;}
async function action(op,data={}){if(busy)return;busy=true;error(null);try{state=await api(op,{revision:state.revision,...data});render();return true;}catch(e){error(e);await poll();return false;}finally{busy=false;}}
for(const op of ['create','join'])$(op).onsubmit=async e=>{e.preventDefault();if(busy)return;busy=true;error(null);try{await Creator.init;const d=Object.fromEntries(new FormData(e.target));d.character=Creator.read();d.role=Creator.role();if(op==='create'){d.procedural=$('procedural').checked;d.hardcore=$('hardcore').checked;}session=await api(op,d);sessionStorage.setItem('thorns-session',JSON.stringify(session));localStorage.setItem('thorns-recovery',JSON.stringify(session));$('resume').hidden=false;await poll();}catch(e){error(e);}finally{busy=false;}};
async function poll(){if(!session)return;try{state=await api('state');$('connection').textContent='CONNECTED';render();}catch(e){$('connection').textContent='RECONNECTING…';error(e);}}
function render(){if(!state||!session)return;const key=JSON.stringify(state);if(key===lastRender)return;lastRender=key;
 $('lobby').hidden=true;$('game').hidden=false;if(state.started)Creator.editing=false;$('builder').hidden=!Creator.editing;
 document.body.dataset.region=state.scene.region;
 const host=state.host===session.id,ended=state.scene.choices.length===0;
 $('room').textContent=`ROOM ${state.code} / TURN ${state.turn}`;
 $('region').textContent=state.scene.region;$('title').textContent=state.scene.title;$('story').textContent=state.scene.text;
 $('count').textContent=`${state.players.length}/6`;$('cohesion').textContent=`COHESION ${state.cohesion}/10`;$('meter').max=10;$('meter').value=state.cohesion;
 $('party').replaceChildren();for(const p of state.players){const e=node('div',`${p.name}${p.id===session.id?' [YOU]':''}${p.id===state.host?' ◆':''}`,'member');e.append(node('small',`${p.role} / ${p.xp} XP${p.id===state.actor?' / SPECIALIST':''}${Object.hasOwn(state.votes,p.id)?' / VOTED':''}`));$('party').append(e);}
 const actor=$('actor');actor.replaceChildren();for(const p of state.players)actor.add(new Option(p.name+' / '+p.role,p.id));actor.value=state.actor;actor.disabled=!host||Object.keys(state.votes).length>0||ended;
 renderWorld();if(window.renderOpenWorld)renderOpenWorld();
 if(window.FieldGuide)FieldGuide.render(state,session.id,action);
 $('flags').textContent=state.flags.length?state.flags.join(' · '):'No findings yet.';
 $('choices').replaceChildren();state.scene.choices.forEach((c,i)=>{const b=node('button',`${String(i+1).padStart(2,'0')} / ${c.label}`,'choice');if(state.votes[session.id]===i)b.classList.add('selected');const count=Object.values(state.votes).filter(v=>v===i).length;let rule=c.stat?`${c.stat.toUpperCase()} / DC ${c.dc} · +${c.check.total} total · ${c.check.success_percent}% success · attribute ${c.check.attribute}, XP ${c.check.experience}, practice ${c.check.practice}, findings ${c.check.findings} · ${c.check.proficiency_name}`:'NO ROLL';b.append(node('small',rule+` · ${count} VOTE${count===1?'':'S'}`));b.disabled=!state.started;b.onclick=()=>action('vote',{choice:i});$('choices').append(b);});
 $('start').hidden=!host||state.started;$('resolve').hidden=!host||!state.started||ended;$('resolve').disabled=Object.keys(state.votes).length===0;
 $('votingrule').textContent=!state.started?'Gather your party before starting. New players cannot join after launch.':ended?'':`${Object.keys(state.votes).length}/${state.players.length} votes received. All votes resolve automatically; the host may resolve early.`;
 $('ending').hidden=!ended||state.mode==='open';if(state.mode==='open'){$('choices').hidden=true;$('resolve').hidden=true;$('votingrule').textContent='Each player explores independently. Party chat remains global.';}$('log').replaceChildren(...state.log.map(l=>node('li',l)));
 $('codex').replaceChildren();for(const [k,v]of Object.entries(state.codex)){const p=node('p','');p.append(node('strong',k+' — '),document.createTextNode(v));$('codex').append(p);}
 $('chat').replaceChildren(...state.chat.map(m=>node('p',`${m.name}: ${m.text}`)));$('chat').scrollTop=$('chat').scrollHeight;
}
$('start').onclick=()=>action('start');$('resolve').onclick=()=>action('resolve');$('actor').onchange=e=>action('actor',{actor:e.target.value});
$('chat-form').onsubmit=async e=>{e.preventDefault();const text=$('message').value;if(!text.trim())return;if(await action('chat',{message:text}))$('message').value='';};
function exit(){session=null;state=null;lastRender='';sessionStorage.removeItem('thorns-session');$('game').hidden=true;$('lobby').hidden=false;$('builder').hidden=false;Creator.editing=false;$('build-apply').hidden=true;$('build-cancel').hidden=true;error(null);}
$('resume').hidden=!localStorage.getItem('thorns-recovery');$('resume').onclick=()=>{try{session=JSON.parse(localStorage.getItem('thorns-recovery'));sessionStorage.setItem('thorns-session',JSON.stringify(session));poll();}catch(e){error(e);}};
$('exit').onclick=exit;$('new').onclick=exit;$('leave').onclick=async()=>{try{await api('leave',{revision:state.revision});localStorage.removeItem('thorns-recovery');$('resume').hidden=true;exit();}catch(e){error(e);}};
let crt=localStorage.getItem('thorns-crt')!=='off';function crtRender(){document.body.classList.toggle('no-crt',!crt);$('crt').textContent=`CRT EFFECT: ${crt?'ON':'OFF'}`;}crtRender();$('crt').onclick=()=>{crt=!crt;localStorage.setItem('thorns-crt',crt?'on':'off');crtRender();};
poll();setInterval(()=>{if(!busy)poll();},1500);

function renderWorld(){
 $('edit-character').hidden=state.started;
 $('sheets').replaceChildren();
  for(const p of state.players){const s=p.sheet,wrap=node('div','','sheet');wrap.append(node('h3',p.name+(s.pronouns?' / '+s.pronouns:'')));
   const lines=[`${p.role} · ${s.origin} · ${s.form}`,`Affiliation: ${s.affiliation}. Affinity: ${s.affinity}.`,Object.entries(s.attributes).map(([k,v])=>`${k.toUpperCase()} ${v}`).join(' / '),`XP ${s.xp} · experience bonus +${s.experience_bonus} · unspent training ${s.unspent_training}`,`Proficiencies: ${Object.entries(s.skills).map(([k,v])=>`${Creator.catalog?.skills[k]?.label||k} ${v}`).join('; ')||'None'}`,`Mod: ${Creator.catalog?.mods[s.mod]?.label||s.mod} — ${s.mod_status}`,`Conditions: ${s.conditions.join(', ')}`,`Permissions: ${Object.entries(s.certifications).map(([k,v])=>k+': '+v).join('; ')}`];
   lines.forEach(l=>wrap.append(node('p',l)));
   const story=[['Age',s.age],['Livelihood',s.livelihood],['Appearance',s.appearance],['Voice',s.voice],['Mannerisms',s.mannerisms],['History',s.bio],['Goal',s.goal],['Unanswered question',s.question],['Important relationship or promise',s.relationship],['Boundaries',s.boundary]].filter(([,v])=>typeof v==='string'&&v.trim());
   if(story.length){const details=document.createElement('details');details.append(node('summary','CHARACTER STORY / PRESENTATION'));for(const [label,value]of story)details.append(node('p',`${label}: ${value}`));wrap.append(details);}
   $('sheets').append(wrap);
 }
 $('reputation').replaceChildren();for(const [f,v]of Object.entries(state.reputation))$('reputation').append(node('div',`${f}: ${v>0?'+':''}${v} / ${state.reputation_tiers[f]}`,'rep-row'));
 $('rep-log').replaceChildren(...state.rep_log.slice(-8).reverse().map(x=>node('p',`${x.faction} ${x.change>=0?'+':''}${x.change}: ${x.reason}`)));
 const pos=state.positions[session.id],others=state.players.filter(p=>p.id!==session.id);$('positions').textContent=state.players.map(p=>`${p.name}: position ${state.positions[p.id]} (${Math.abs(pos-state.positions[p.id])*5} m from you), composure ${p.composure}`).join('\n');
 const select=$('local-target'),old=select.value;select.replaceChildren(...others.map(p=>new Option(p.name,p.id)));if(others.some(p=>p.id===old))select.value=old;
 $('move-left').disabled=!state.started||pos===0||state.moved[session.id]===state.turn;$('move-right').disabled=!state.started||pos===4||state.moved[session.id]===state.turn;
 const me=state.duels.find(d=>d.players.includes(session.id));$('duel-status').textContent=me?(me.accepted?'Mutual duel active. Either player may end it.':'Invitation pending. Only the invited player may accept.'):'No active duel or invitation.';
 for(const id of ['challenge','accept','disengage','duel-action','local-speak'])$(id).disabled=!state.started||!others.length||!state.scene.choices.length;
}
$('edit-character').onclick=async()=>{try{await Creator.init;const p=state.players.find(p=>p.id===session.id);Creator.set(p.role,p.character,{allowLegacyTraining:true});Creator.editing=true;$('builder').hidden=false;$('build-apply').hidden=false;$('build-cancel').hidden=false;$('builder').scrollIntoView();}catch(e){error(e);}};
$('build-cancel').onclick=()=>{Creator.editing=false;$('builder').hidden=true;};
$('build-apply').onclick=async()=>{try{const c=Creator.read();await action('character',{role:Creator.role(),character:c});}catch(e){error(e);}};
$('move-left').onclick=()=>action('move',{step:-1});$('move-right').onclick=()=>action('move',{step:1});
for(const op of ['challenge','accept','disengage'])$(op).onclick=()=>action(op,{target:$('local-target').value});
$('duel-action').onclick=()=>action('duel_action',{target:$('local-target').value,style:$('duel-style').value});
$('local-speak').onclick=()=>action('speak',{target:$('local-target').value,message:$('local-message').value});
