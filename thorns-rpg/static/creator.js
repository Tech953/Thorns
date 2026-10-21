'use strict';
window.Creator={ready:false,catalog:null,editing:false};
(()=>{
 const get=id=>document.getElementById(id),el=(t,s)=>{const e=document.createElement(t);e.textContent=s;return e;};
 const C=window.Creator;let role='Needlurgist';
 const holder=get('build-boundary')?.parentElement?.parentElement;
 for(const [key,label,max] of [['appearance','Appearance',1000],['voice','Dialogue voice',500],['mannerisms','Mannerisms',500],['age','Age description',50]]){
  if(!get('build-'+key)&&holder){const wrap=el('label',label),input=document.createElement(key==='age'?'input':'textarea');input.id='build-'+key;input.maxLength=max;wrap.append(input);holder.append(wrap);}
 }
 const fields=['pronouns','origin','form','affiliation','affinity','mod','bio','goal','boundary','appearance','voice','mannerisms','age'];
 function status(s){get('build-message').textContent=s;}
 C.read=()=>{
  if(!C.ready)throw Error('Character catalog is still loading.');
  const c={schema:1,attributes:{},skills:{}};
  fields.forEach(k=>c[k]=get('build-'+k).value);
  Object.keys(C.catalog.attributes).forEach(k=>c.attributes[k]=Number(get('attr-'+k).value));
  Object.keys(C.catalog.skills).forEach(k=>{const n=Number(get('skill-'+k).value);if(n)c.skills[k]=n;});
  if(Object.values(c.attributes).some(v=>!Number.isInteger(v)||v<1||v>4)||Object.values(c.attributes).reduce((a,b)=>a+b,0)!==8)throw Error('Allocate exactly 8 attribute points, with 1–4 in each.');
  if(Object.values(c.skills).some(v=>!Number.isInteger(v)||v<0||v>3)||Object.values(c.skills).reduce((a,b)=>a+b,0)>6)throw Error('Allocate at most 6 proficiency points, with 0–3 in each.');
  return c;
 };
 C.role=()=>role;
 C.set=(r,c)=>{
  if(!C.catalog.roles[r]||!c||typeof c!=='object')throw Error('Invalid character document.');
  const attrs=c.attributes||{},skills=c.skills||{};
  if(Object.keys(attrs).length!==4||Object.keys(attrs).some(k=>!Object.hasOwn(C.catalog.attributes,k))||Object.keys(skills).some(k=>!Object.hasOwn(C.catalog.skills,k)))throw Error('Unknown attribute or proficiency.');
  for(const [k,v] of Object.entries(attrs))if(!Number.isInteger(v)||v<1||v>4)throw Error('Invalid attribute score.');
  for(const [k,v] of Object.entries(skills))if(!Number.isInteger(v)||v<0||v>3)throw Error('Invalid proficiency score.');
  if(Object.values(attrs).reduce((a,b)=>a+b,0)!==8||Object.values(skills).reduce((a,b)=>a+b,0)>6)throw Error('Point budget exceeded.');
  const selects={origin:C.catalog.origins,form:C.catalog.forms,affiliation:C.catalog.affiliations,affinity:C.catalog.affinities,mod:Object.keys(C.catalog.mods)};
  for(const [k,list]of Object.entries(selects))if(!list.includes(c[k]))throw Error('Invalid '+k+'.');
  for(const [k,max]of Object.entries({pronouns:40,bio:700,goal:200,boundary:200}))if(typeof c[k]!=='string'||c[k].length>max)throw Error('Invalid '+k+'.');
  role=r;get('build-role').value=r;fields.forEach(k=>get('build-'+k).value=c[k]||'');
  Object.keys(C.catalog.attributes).forEach(k=>get('attr-'+k).value=attrs[k]);
  Object.keys(C.catalog.skills).forEach(k=>get('skill-'+k).value=skills[k]||0);
  document.querySelectorAll('.role-value').forEach(e=>e.value=r);update();
 };
 function update(){
  let a=0,s=0;Object.keys(C.catalog.attributes).forEach(k=>a+=Number(get('attr-'+k).value));Object.keys(C.catalog.skills).forEach(k=>s+=Number(get('skill-'+k).value));
  get('attribute-total').textContent=`Attributes ${a}/8 · ${a===8?'Ready':'Adjust total to 8'}`;
  get('skill-total').textContent=`Training ${s}/6 · ${6-s} remaining`;
 }
 function bundle(){return {format:'THORNS-character',version:1,role,character:C.read()};}
 function load(raw){if(raw.format!=='THORNS-character'||raw.version!==1)throw Error('Expected THORNS character version 1.');C.set(raw.role,raw.character);status('Character loaded. Name is set separately when creating or joining a room.');}
 get('build-save').onclick=()=>{try{localStorage.setItem('thorns-character-draft',JSON.stringify(bundle()));status('Draft saved in this browser.');}catch(e){status(e.message);}};
 get('build-load').onclick=()=>{try{load(JSON.parse(localStorage.getItem('thorns-character-draft')));}catch(e){status('Could not load draft: '+e.message);}};
 get('build-export').onclick=()=>{try{const b=new Blob([JSON.stringify(bundle(),null,2)],{type:'application/json'}),u=URL.createObjectURL(b),a=el('a','');a.href=u;a.download='THORNS-character.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);status('Character exported without room credentials or earned progress.');}catch(e){status(e.message);}};
 get('build-import').onchange=async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>16384)throw Error('Character file must be under 16 KB.');load(JSON.parse(await f.text()));}catch(e){status(e.message);}finally{e.target.value='';}};
 C.init=(async()=>{try{
  const response=await fetch('/character-catalog');if(!response.ok)throw Error('Character catalog unavailable.');C.catalog=await response.json();
  for(const r of Object.keys(C.catalog.roles))get('build-role').add(new Option(r,r));
  for(const [key,items]of Object.entries({origin:C.catalog.origins,form:C.catalog.forms,affiliation:C.catalog.affiliations,affinity:C.catalog.affinities}))for(const v of items)get('build-'+key).add(new Option(v,v));
  for(const [k,v]of Object.entries(C.catalog.mods))get('build-mod').add(new Option(v.label,k));
  for(const [k,v]of Object.entries(C.catalog.attributes)){const l=el('label',k.toUpperCase()),i=document.createElement('input');i.type='number';i.min=1;i.max=4;i.step=1;i.id='attr-'+k;i.oninput=update;l.append(i,el('small',v));get('build-attributes').append(l);}
  for(const [k,v]of Object.entries(C.catalog.skills)){const l=el('label',v.label),i=document.createElement('select');i.id='skill-'+k;for(let n=0;n<=3;n++)i.add(new Option(String(n),String(n)));i.onchange=update;l.append(i,el('small',v.description+' Source: '+v.source+' / '+v.section+'. '+(v.active?'Used in chapter checks.':k==='ballistics'?'Used in consensual ranged duels.':'Recorded for later chapters.')));get('build-skills').append(l);}
  C.ready=true;C.set(role,C.catalog.presets[role]);get('build-role').onchange=e=>{C.set(e.target.value,C.catalog.presets[e.target.value]);status('Preset applied; attributes and proficiencies reset to this discipline’s defaults.');};
 }catch(e){status(e.message);throw e;}})();
})();
