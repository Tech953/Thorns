"""Open-world prototype rules, not canonical geography or biology."""
import hashlib, random, secrets
import characters, world, generation
import field_rules,field_adventure
MODS={
 'leg_spikes':('LEG|SPIKES','body','transversal'),
 'meta_fingers':('Meta-Fingers','tech','fractech'),
 'bio_glass':('Corded Bio-Glass','tech','medtech'),
 'crystallin':('Crystallin< retrofit','tech','crystallin'),
 'survey_lens':('Survey lens [adaptation]','percept','percept'),
 'filter_graft':('Filter graft [adaptation]','body','fieldcraft'),
 'rest_regulator':('Rest regulator [adaptation]','body','fieldcraft'),
 'resonance_link':('Resonance link [adaptation]','rapport','contracts'),
}
def init(r):
 r.setdefault('mode','chapter');r.setdefault('hardcore',False)
 if r['mode']!='open':return
 r.setdefault('seed',secrets.token_hex(8))
 r.setdefault('overland_sites',{});r.setdefault('contacts',{})
 for p in r['players']:
  p.setdefault('grid',[0,0]);p.setdefault('vitals',dict(health=100,hunger=0,thirst=0,sleep=0,injuries=[],ailments=[]))
  p.setdefault('supplies',dict(food=4,water=6,medkit=2));p.setdefault('credits',30);p.setdefault('karma',0)
  p.setdefault('steps',0);p.setdefault('contract',None);p.setdefault('benefits',0);p.setdefault('contract_serial',0)
  generation.ensure_player(p);p.setdefault('dialogue_log',[])
  p.setdefault('loadout',[]);p.setdefault('licensed',False);p.setdefault('event',None);p.setdefault('recent_events',[])
def tile(r,x,y):
 rng=random.Random(hashlib.sha256(f"{r['seed']}:{x}:{y}".encode()).digest())
 depth=max(abs(x),abs(y));region=['WN_TOWER','CITY_CLOUD_S','ENACT_HILLS','AETHERGALE'][(int(x<0)*2+int(y<0))] if depth<40 else 'OMNI-META-INFI-PARTICULATE'
 facility='sanctuary' if (x==0 and y==0) or (x%8==0 and y%8==0) else rng.choice(['relay','market','clinic','ruin','wilds','wilds'])
 name=rng.choice(['Whispering','Prismatic','Ash-veiled','Recursive','Fractured','Silent'])+' '+rng.choice(['terrace','causeway','hollow','concourse','lattice','observatory'])
 text=f"{name}. {rng.choice(['Cables hum beneath the paving.','Faceted shadows fold across the horizon.','A distant transmission dissolves into static.','Fine luminous dust traces the air.'])} {rng.choice(['Survey stakes disagree about the scale.','Travellers have left a careful route record.','A sealed archive repeats an unfinished account.'])}"
 regional={
  'WN_TOWER':['Darkwood ash drifts through a bio-plast service gantry. Black.dot verification markers punctuate the Greatweb overlays.','A sterile Sap Core advertisement cuts through the haze; worn tools and patched bio-plast tell a different story below it.'],
  'CITY_CLOUD_S':['Metal ribs frame the mountain passage. A bounded educational projection traces geometric lessons across the salvaged surface.','An indexed lattice of metal terraces carries trade references and node permissions; the distant heights remain screened from this survey.'],
  'ENACT_HILLS':['Cooking smoke rises from residential paths below the restricted boundary. An archival light projection records the distinction.','Worked metallurgy and ordinary household repairs share the foothill path; a distant security marker stands apart from civilian life.'],
  'AETHERGALE':['Jade and rose contrails wash across tent fabric and crystalline survey instruments. Dust follows the AETHER currents.','Bio-plast silhouettes pass between tent-constructs as jade and rose light runs across the wind-scoured ground.'],
  'OMNI-META-INFI-PARTICULATE':['A tesseract-like semblance fractures the apparent horizon; scale cannot be verified from the received projection.','A shifting signpost-like record interrupts the projected geometry. Its apparent offers remain unverified observations.']}
 text=f"{name}. {rng.choice(regional[region])} {rng.choice(['The survey leaves gaps in the record.','Nearby route references require interpretation.','This generated site has no verified canonical placement.'])}"
 if depth>=40:text+=' Remote percept projection: generated, unverified semblance beyond ordinary survey. This does not establish passage through RED>GATE> or access permissions.'
 cell=dict(x=x,y=y,region=region,facility=facility,title=name,text=text,depth=depth)
 cell['presentation']=r.get('overland_sites',{}).get(f'{x},{y}') or generation.site_identity(r['seed'],cell)
 # Ordinary seeded sensory detail cannot turn a remote projection into a site.
 if depth<40:
  proxy=dict(cell,feature=facility+' approach',shelter=int(facility=='sanctuary'))
  cell['text']+='\n\n'+generation.describe_site(r,proxy,'daylight','still air')
 return cell
def penalty(p):
 v=p['vitals'];return min(5,len(v['injuries'])+len(v['ailments'])+sum(v[k]>=70 for k in ['hunger','thirst','sleep']))
def roll(r,p,stat,skill,dc,log,faction=None):
 if field_rules.active(r):
  ok,text=field_rules.roll(r,p,stat,skill,dc,'interaction',faction=faction);log(r,text);return ok
 mod=min(2,sum(MODS[m][2]==skill for m in p['loadout']))
 practice=min(2,p['character']['skills'].get(skill,0)+mod)
 reputation=max(-2,min(2,int(r['reputation'].get(faction,0)/5))) if faction else 0
 bonus=p['character']['attributes'][stat]+practice+min(2,p['xp']//3)+reputation-penalty(p)
 die=secrets.randbelow(20)+1;ok=die==20 or (die!=1 and die+bonus>=dc)
 log(r,f"{p['name']}: D20 {die} + {bonus} vs {dc}: {'SUCCESS' if ok else 'SETBACK'} (practice {practice}, equipment {mod} within practice cap, reputation {reputation:+}, condition -{penalty(p)}).")
 return ok

def speak(r,p,here,topic,check,log):
 check(here['depth']<40,'A received projection does not establish a present person to address.')
 check(topic in {'place','needs','history','access','contracts','plans'},'Choose a displayed local dialogue topic.')
 site=f"{here['x']},{here['y']}";a=r['contacts'].get(site)
 if a is None:
  seed=r['seed'];identity='contact:'+site
  name=generation.choose(seed,identity,'given',['Iri','Neri','Sela','Vale','Tali','Orin','Meren','Kest'])+' '+generation.choose(seed,identity,'family',['Reed','Brace','Vane','Thread','Rill','Vale'])
  faction=generation.choose(seed,identity,'faction',world.REGIONAL[here['region']])
  role={'clinic':'Needlurgist','relay':'Fractech Archivist','market':'Seam Mediator','sanctuary':'Seam Mediator'}.get(here['facility'],'NanoClad Scout')
  ch=characters.default(role);ch.update(origin=here['region'],bio=f"{name} keeps a local field record at {here['title']}. This generated contact’s past is limited to the current adaptation; no source character’s biography is assigned.",goal='keep a dependable local record',boundary='No claims of administrator authority')
  a=dict(id=identity,name=name,x=here['x'],y=here['y'],faction=faction,role=role,character=ch,tone=generation.choose(seed,identity,'voice',['plain and careful','warm and measured','terse and exact']),need=generation.choose(seed,identity,'need',['water','food','maintained tools']),attitude=50,health=100,energy=100,activity='keeping the local field record',visitors={})
  r['contacts'][site]=a
 relationship=a['visitors'].setdefault(p['id'],dict(visits=0,trust=0,bond_after=0))
 if field_rules.active(r):
  p['relationships'][a['id']]=relationship
  ok,text=field_rules.roll(r,p,'rapport','contracts' if topic in {'contracts','access'} else 'community',10,'dialogue',faction=a['faction'],npc=a);log(r,text)
 else:ok=roll(r,p,'rapport','contracts' if topic in {'contracts','access'} else 'community',10,log,a['faction'])
 if topic=='place':body=f"This is {here['title']}, a generated {here['facility']} approach in {here['region']}. Our region has its own materials and providers; a local name does not map the whole world."
 elif topic=='needs':body=f"My stated concern is {a['need']}. Talking does not transfer supplies; your own pack remains yours."
 elif topic=='history':body=f"Our local record contains {relationship['visits']} earlier conversations, with trust {relationship['trust']}. Your declared goal is {p['character'].get('goal') or 'not yet stated'}."
 elif topic=='access':body='Affiliation and reputation do not grant administrator authority. RED>GATE> remains a barrier. This local field record grants no restricted access.'
 elif topic=='contracts':body=('The board here can register a survey. Read its coordinates and terms before accepting.' if here['facility'] in {'relay','market','sanctuary'} else 'There is no active board at this approach. A relay or provision stop may have one.')
 else:body=f"I aim to {a['character']['goal']}. My boundary is {a['character']['boundary'].lower()}."
 if not ok:body+=' Those public facts remain available; any further interpretation is provisional.'
 text=generation.dialogue(r,p,a,topic,body,ok,here)
 context=world.contact_context(p.get('character',{}),topic,a['faction'])
 p['dialogue_log'].append(dict(site=p['grid'][:],npc=a['name'],topic=topic,response=text,step=p['steps'],character=dict(name=p['name'],**p['character']),context=context))
 p['dialogue_log']=p['dialogue_log'][-200:];relationship['visits']+=1
 if ok and p['steps']>=relationship['bond_after']:
  relationship['trust']=min(5,relationship['trust']+1);relationship['bond_after']=p['steps']+4
 log(r,text)
def tick(r,p,log):
 p['steps']+=1
 if not r['hardcore']:return
 v=p['vitals']
 for k,n in [('hunger',3),('thirst',5),('sleep',2 if 'rest_regulator' in p['loadout'] else 3)]:v[k]=min(100,v[k]+n)
 v['health']=max(0,v['health']-sum(v[k]>=90 for k in ['hunger','thirst','sleep'])*4-len(v['ailments']))
 if v['health']==0:
  p['grid']=[0,0];v.update(health=35,hunger=40,thirst=40,sleep=40);p['credits']=max(0,p['credits']-15);p['event']=None
  log(r,p['name']+' evacuated to sanctuary; 15-credit rescue cost (limited to available credits). Injuries and ailments remain.');return True
 return False
def view(r,p):
 x,y=p['grid'];a=r.get('contacts',{}).get(f'{x},{y}')
 last=next((d for d in reversed(p.get('dialogue_log',[])) if d['site']==[x,y]),None)
 here=tile(r,x,y);preview=None
 if not p.get('contract') and here['facility'] in {'relay','market','sanctuary'}:
  issuers=world.REGIONAL.get(here['region'],['NanoClad'])
  serial=p.get('contract_serial',0)
  faction=issuers[0] if field_rules.active(r) else issuers[serial%len(issuers)]
  preview=dict(kind='Survey',description='Return a verified route record',faction=faction,
               context=world.contract_context(p.get('character',{}),faction))
 return dict(contact=a,last_dialogue=last.get('response','') if last else '',last_dialogue_context=last.get('context') if last else None,location=here,tiles=[tile(r,x+dx,y+dy) for dy in range(-2,3) for dx in range(-2,3)],penalty=penalty(p),mods={k:dict(label=v[0],skill=v[2],cost=12) for k,v in MODS.items()},contract_preview=preview)
def act(r,p,d,check,log):
 check(r['mode']=='open' and r['started'],'Start an open-world room first.')
 if field_rules.active(r):return field_adventure.native(r,p,d,check,log)
 op=d['op'];here=tile(r,*p['grid']);v=p['vitals']
 check(not p['event'] or op=='ow_encounter','Resolve or decline your encounter first.')
 duel=next((x for x in r['duels'] if p['id'] in x['players']),None)
 check(duel is None,'End your duel invitation or duel before exploring.')
 if op=='ow_move':
  dx,dy=d.get('dx'),d.get('dy');check(type(dx)==int and type(dy)==int and abs(dx)+abs(dy)==1,'Move one orthogonal tile.')
  x,y=p['grid'];check(max(abs(x+dx),abs(y+dy))<=1000000,'Survey coordinate limit reached.')
  destination=f'{x+dx},{y+dy}'
  check(destination in r['overland_sites'] or len(r['overland_sites'])<2048,'This save has reached its 2,048-site record limit. Existing routes remain available.')
  r['overland_sites'].setdefault(destination,tile(r,x+dx,y+dy)['presentation'])
  p['grid']=[x+dx,y+dy]
  if tick(r,p,log):return
  here=tile(r,*p['grid'])
  if r['hardcore'] and here['facility']=='wilds' and secrets.randbelow(5)==0:
   if not roll(r,p,'body','fieldcraft',12,log):
    condition=secrets.choice(['strained leg','abrasions']);v['health']=max(1,v['health']-10)
    if condition not in v['injuries']:v['injuries'].append(condition)
    if 'filter_graft' not in p['loadout'] and 'particulate irritation' not in v['ailments']:v['ailments'].append('particulate irritation')
  if r['procedural'] and secrets.randbelow(100)<30:
   pool=[t for t in world.TEMPLATES if t['id'] not in p['recent_events'][-3:]];t=secrets.choice(pool)
   faction=secrets.choice(world.REGIONAL.get(here['region'],['NanoClad']))
   rep=r['reputation'][faction];dc=12+(-2 if rep>=6 else 2 if rep<=-6 else 0)
   context=world.encounter_context(p.get('character',{}),t['id'],faction)
   p['event']=dict(title=t['title'],body=t['body'],approaches=t['approaches'],faction=faction,dc=dc,template=t['id'],context=context)
   p['recent_events']=(p['recent_events']+[t['id']])[-3:]
 elif op=='ow_talk':
  speak(r,p,here,d.get('topic','place'),check,log)
 elif op=='ow_encounter':
  e=p['event'];check(e is not None,'No encounter.');i=d.get('choice');check(type(i)==int and 0<=i<=3,'Invalid approach.')
  if i<3:
   _,stat,sk=e['approaches'][i];ok=roll(r,p,stat,sk,e['dc'],log);p['xp']+=1
   world.adjust(r,e['faction'],2 if ok else -1,e['title'])
   if ok:p['credits']+=5;p['karma']=min(100,p['karma']+1)
  p['event']=None
 elif op=='ow_consume':
  item=d.get('item');check(item in ['food','water','medkit'],'Unknown supply.');check(p['supplies'][item]>0,'No supply remaining.');p['supplies'][item]-=1
  if item=='medkit':
   v['health']=min(100,v['health']+25)
   if v['injuries']:v['injuries'].pop()
  else:
   key='hunger' if item=='food' else 'thirst';v[key]=max(0,v[key]-40)
 elif op=='ow_rest':
  check(here['facility']=='sanctuary','Rest at a sanctuary.');tick(r,p,log);v['sleep']=0;v['health']=min(100,v['health']+20)
 elif op=='ow_clinic':
  check(here['facility'] in ['clinic','sanctuary'],'Find a clinic or sanctuary.');cost=max(3,12-min(9,p['benefits']*3));check(p['credits']>=cost,'Insufficient credits.');p['credits']-=cost;v.update(health=100,injuries=[],ailments=[])
 elif op=='ow_buy':
  check(here['facility'] in ['market','sanctuary'],'Find a market or sanctuary.');item=d.get('item');check(item in p['supplies'],'Unknown supply.');cost=6 if item=='medkit' else 2;check(p['credits']>=cost,'Insufficient credits.');p['credits']-=cost;p['supplies'][item]+=1
 elif op=='ow_contract':
  check(p['contract'] is None,'Finish or abandon your current contract.');check(here['facility'] in ['relay','market','sanctuary'],'Find a contract board.')
  n=p['contract_serial'];p['contract_serial']+=1;x,y=p['grid'];f=world.REGIONAL.get(here['region'],['NanoClad'])[n%len(world.REGIONAL.get(here['region'],['NanoClad']))]
  p['contract']=dict(target=[x+2+(n%3),y+1],faction=f,reward=18,kind='Survey and return a verified route record',stage='travel',context=world.contract_context(p.get('character',{}),f))
 elif op=='ow_complete':
  c=p['contract'];check(c is not None and p['grid']==c['target'],'Reach your contract coordinates.')
  if not roll(r,p,'percept','percept',10,log):
   tick(r,p,log);return
  p['credits']+=c['reward'];p['xp']+=1;p['benefits']=min(3,p['benefits']+1);p['karma']=min(100,p['karma']+2);world.adjust(r,c['faction'],2,'Completed survey contract');p['contract']=None
 elif op=='ow_abandon':
  check(p['contract'] is not None,'No contract.');world.adjust(r,p['contract']['faction'],-1,'Abandoned commitment');p['karma']=max(-100,p['karma']-1);p['contract']=None
 elif op=='ow_mod':
  check(here['facility'] in ['clinic','sanctuary'],'Installation requires a clinic or sanctuary.');m=d.get('mod');check(isinstance(m,str) and m in MODS,'Unknown mod.')
  if m in p['loadout']:p['loadout'].remove(m)
  else:
   check(len(p['loadout'])<3,'Three installed mod slots. Remove one first.');check(p['credits']>=12,'Installation costs 12 credits.');p['credits']-=12;p['loadout'].append(m);p['licensed']=True
 elif op=='ow_scavenge':
  check(here['facility'] in ['wilds','ruin'],'Scavenge in wilds or ruins.')
  if roll(r,p,'tech','resource',12,log):p['supplies'][secrets.choice(['food','water'])]+=1
  else:v['health']=max(1,v['health']-5)
  tick(r,p,log)
 else:raise ValueError('Unknown open-world action.')
 generation.witness(r,p,dict(action=op),here,list(r['contacts'].values()))
 log(r,p['name']+' / '+op.removeprefix('ow_'))
