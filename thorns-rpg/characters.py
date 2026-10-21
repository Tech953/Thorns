"""Character rules v1. Numerical scales are game adaptations, not source canon."""
import copy
from content import ROLES
ATTRIBUTES={'body':'Physical resilience, movement and practical execution.','tech':'Craft, repair, node integration and technical control.','percept':'Observation, pattern discrimination and environmental interpretation.','rapport':'Negotiation, teaching, cooperation and voluntary communication.'}
ORIGINS=['WN_TOWER','CITY_CLOUD_S','ENACT_HILLS','AETHERGALE','Unspecified / itinerant']
FORMS=['Biological / augmented','Metal-kin','lightPROKT< concept','Other / unspecified']
AFFILIATIONS=['Independent','THORNS associate','Embrite associate','Sap Core associate','Lifestring.CO associate','Druid-Sec associate','Fractech student','WN_EDU student','ED.NET student','Harvet contractor','ANC.NI apprentice','MOD_OP apprentice','SPIDREsec pilgrim','NanoClad pilgrim','INTERnode researcher','MMTX< associate','WN_LAW aspirant','WN_MED aspirant','MILI_WN aspirant','OMNI-META.OPEND aspirant','SEC.IO aspirant']
# Ratings buy training, never unrestricted permission. Empty scopes mean recorded only in this chapter.
def skill(label,source,section,stat,nodes,description):
 return dict(label=label,source=source,section=section,stat=stat,nodes=nodes,description=description,active=bool(nodes))
SKILLS={
 'transversal':skill('Transversal','WN_TOWER','Leg|Spikes; SPIDREsec','body',['undercroft','mid'],'Movement through steep or compromised infrastructure.'),
 'fieldcraft':skill('Pilgrimage fieldcraft','AETHERGALE','CHECKPOINT.triad; CHECKPOINT.UNDERTOW','body',['fractlands'],'Practical route protection and expedition movement.'),
 'ballistics':skill('Wirelet / crystallin< ballistics','WN_TOWER','MOD_OP; Wirelet','body',[],'Weapon proficiency record; this chapter has no tactical combat.'),
 'needlurgy':skill('Needlurgy / bio-nano ink','WN_TOWER','Needlurgy; ANC.NI','tech',['foothills','contact'],'Fine interface craft; does not authorize restricted augmentation.'),
 'seamllurgy':skill('seamLLurgy / seam control','WN_TOWER','seamLLurgy','tech',['web','contact'],'Bounded seam-interface control, not an exemption from meta regulation.'),
 'fractech':skill('Fractech / nodeTECH','WN_TOWER','Fractech; Greatweb','tech',['web','kho','peak','undertow'],'Node integration and safe parameter handling.'),
 'metallurgy':skill('Metallurgy / salvage','CITY_CLOUD_S','base.EN_KHO','tech',['mid','foothills','pyri'],'Repair, extraction and construction training.'),
 'crystallin':skill('Crystallin< / enneract craft','WN_TOWER','Crystallin<','tech',['gale','contact'],'Crystalline apparatus and enneract-reference handling.'),
 'resource':skill('Meta-break resource acquisition','AETHERGALE','Regional introduction; CHECKPOINT.triad','tech',['foothills'],'Provisioning knowledge; no infinite portable inventory.'),
 'arcane':skill('arcaneTECH / siphon_protocol','AETHERGALE','CHECKPOINT.GALE','tech',['gale'],'AETHER apparatus and energy-acquisition technique.'),
 'archive':skill('Archival / INTERnode analysis','ENACT_HILLS','INTERnode','tech',['archive','kho'],'Index analysis and narrative data comparison.'),
 'rune':skill('runeTECH / spark-core craft','ENACT_HILLS','UPPER RUNEHILLS','tech',['pyri'],'Training with metal-kin patterns; not authority over a person.'),
 'medtech':skill('medTech / extraction care','WN_TOWER','WN_MED','tech',[],'Care proficiency record; no medical-treatment encounter exists yet.'),
 'necra':skill('Necramancer / necra-mod theory','ENACT_HILLS','Necramancer','tech',[],'Theory only at creation. MERC.DOT and other applicable verification are required for practice.'),
 'lifestring':skill('Life Strings / Corded Bio-Glass','WN_TOWER','Lifestring.CO; Corded Bio-Glass','tech',[],'Training record; does not permit extraction or grant resurrection.'),
 'druid':skill('Druid-Sec fractal ecology','WN_TOWER','Druid-Sec; The Harvet','percept',['fractlands'],'Read ecological geometry without assuming faction immunity.'),
 'percept':skill('Percept / semblance discrimination','CITY_CLOUD_S','ED.NET','percept',['undercroft','kho','archive'],'Distinguish representations from evidence.'),
 'light':skill('lightPROKT< interpretation','AETHERGALE','CHECKPOINT.CASC','percept',['kho','undertow'],'Interpret light manifestations without treating them as property.'),
 'aether':skill('AETHER / fractURAL affinity study','AETHERGALE','CHECKPOINT.GALE','percept',['gale','undertow'],'Learn to read concentrations and LYLINE / LLYINE relationships.'),
 'nullsurvey':skill('NULL_FIELD remote survey','NULL_FIELD.OMNI','CONTRAIL_UNDER>CONTRAIL>CONTRAIL; CASCADE.net','percept',['undertow'],'Remote observation only; no access to an unknown interior.'),
 'history':skill('Historical narrative analysis','CITY_CLOUD_S','ED.NET','percept',['archive','kho'],'Evaluate narrative fragments and context.'),
 'contracts':skill('Contract mediation / Merc Tag literacy','WN_TOWER','Merc Tag; The Arcturion','rapport',['web','peak'],'Negotiate within actual scope of a contract.'),
 'community':skill('Community craft / provision','ENACT_HILLS','FOOTHILL CUSP','rapport',['foothills','fractlands'],'Cooperative work and practical mutual assistance.'),
 'teaching':skill('Teaching / integration dialogue','ENACT_HILLS','PYRI; UPPER RUNEHILLS','rapport',['pyri','contact'],'Communicate an offer with room for refusal.'),
 'memetic':skill('Memetic analysis / contract rhetoric','ENACT_HILLS','ADMIN.COA; MMTX<','rapport',['peak'],'Interpret institutional rhetoric; does not grant coercive command.'),
}
MODS={
 'none':dict(label='No installed mod',nodes=[],stat=None,source='Prototype option',gate=None),
 'leg_spikes':dict(label='LEG|SPIKES',nodes=['undercroft','mid'],stat='body',source='WN_TOWER / SPIDREsec',gate='registered'),
 'meta_fingers':dict(label='Meta-Fingers (regulated)',nodes=['web','contact'],stat='tech',source='WN_TOWER / MOD_OP',gate='registered'),
 'bio_glass':dict(label='Corded Bio-Glass interface',nodes=['contact'],stat='tech',source='WN_TOWER / Corded Bio-Glass',gate='registered'),
 'crystallin':dict(label='Crystallin< retrofit',nodes=['gale'],stat='tech',source='WN_TOWER / >CRYSTL-IN',gate='registered'),
}
AFFINITIES=['None declared','Metallurgy','Fractech','Druid-Sec geometry','fractURAL / AETHER','Bio-nano','lightPROKT< study','Necra-mod theory']
PERMITS=['black.dot','Merc Tag','WN_EDU','ED.NET','MERC.DOT','admin.OS','adminENACT']
PRESETS={
 'Needlurgist':{'needlurgy':2,'seamllurgy':1,'crystallin':1,'metallurgy':1,'contracts':1},
 'NanoClad Scout':{'transversal':2,'fieldcraft':2,'aether':1,'nullsurvey':1},
 'Fractech Archivist':{'fractech':2,'archive':2,'percept':1,'history':1},
 'Seam Mediator':{'contracts':2,'teaching':2,'community':1,'memetic':1},
 'Metal-kin Artisan':{'metallurgy':2,'rune':2,'community':1,'transversal':1},
 'Light Reader':{'light':2,'percept':2,'aether':1,'history':1},
}

def require(ok,msg):
 if not ok: raise ValueError(msg)
def text(value,limit):
 require(isinstance(value,str),'Character text must be a string.')
 require(len(value)<=limit and all(ord(c)>=32 or c in '\n\t' for c in value),'Character text is too long or contains control characters.')
 return value.strip()
def default(role,legacy=False):
 return dict(schema=1,pronouns='',origin=ORIGINS[0],form='Metal-kin' if role=='Metal-kin Artisan' else FORMS[0],affiliation=AFFILIATIONS[0],affinity=AFFINITIES[0],bio='',goal='',boundary='',appearance='',voice='',mannerisms='',age='',attributes=copy.deepcopy(ROLES[role]),skills={} if legacy else copy.deepcopy(PRESETS[role]),mod='none',legacy=legacy)
def validate(raw,role):
 require(type(raw)==dict,'Character must be an object.')
 base=default(role)
 require(set(raw)<=set(base)-{'legacy'},'Unexpected character field. XP and credentials are server-managed.')
 require(raw.get('schema',1)==1,'Unsupported character version.')
 base.update(raw);base['legacy']=False
 for field,limit in [('pronouns',40),('bio',700),('goal',200),('boundary',200),('appearance',1000),('voice',500),('mannerisms',500),('age',50)]:base[field]=text(base[field],limit)
 for field,items in [('origin',ORIGINS),('form',FORMS),('affiliation',AFFILIATIONS),('affinity',AFFINITIES),('mod',MODS)]:
  require(isinstance(base[field],str) and base[field] in items,'Invalid '+field+'.')
 a=base['attributes'];require(type(a)==dict and set(a)==set(ATTRIBUTES),'Provide all four attributes.')
 require(all(type(v)==int and 1<=v<=4 for v in a.values()) and sum(a.values())==8,'Attributes must be integers 1–4 totaling 8.')
 sk=base['skills'];require(type(sk)==dict and set(sk)<=set(SKILLS),'Unknown proficiency.')
 require(all(type(v)==int and 0<=v<=3 for v in sk.values()) and sum(sk.values())<=6,'Proficiencies must be integers 0–3 totaling at most 6.')
 base['skills']={k:v for k,v in sk.items() if v}
 return base

def ensure(p):
 if 'character' not in p:p['character']=default(p['role'],legacy=True)
 return p['character']
def sheet(p,r):
 c=copy.deepcopy(ensure(p)); xp=min(2,p['xp']//3)
 c['xp']=p['xp'];c['experience_bonus']=xp;c['baseline_totals']={k:v+xp for k,v in c['attributes'].items()}
 c['unspent_training']=max(0,6-sum(c['skills'].values()))
 c['certifications']={k:'Not verified in this chapter' for k in PERMITS}
 if 'registered' in r['flags']:
  c['certifications']['black.dot']='Expedition registration — limited chapter scope'
  c['certifications']['Merc Tag']='Expedition contract — limited chapter scope'
 if 'certified' in r['flags']:c['certifications']['ED.NET']='Lesson completed — not unrestricted institutional clearance'
 c['mod_status']='No mod' if c['mod']=='none' else ('Active for listed checks only' if 'registered' in r['flags'] else 'Dormant: chapter registration required')
 c['conditions']=['No individual condition recorded']
 if r.get('mode')=='open':
  c['conditions']=p['vitals']['injuries']+p['vitals']['ailments'] or ['No individual condition recorded']
  c['mod_status']='Chapter blueprint; open-world equipment is listed under BIO-MOD CLINIC'
 if r['node']=='marked' and p['id']==r['actor']:c['conditions']=['ENCAP.MARKING / tri.spiral — chapter ended']
 return c

def breakdown(p,r,choice):
 stat=choice['stat'];c=ensure(p)
 if not stat:return None
 eligible=[(c['skills'].get(k,0),k) for k,v in SKILLS.items() if v['stat']==stat and ((choice.get('skill')==k) if r.get('encounter') else r['node'] in v['nodes'])]
 rank,key=max(eligible,default=(0,None))
 training=min(2,rank)
 mod=MODS[c['mod']]; mb=int(not r.get('encounter') and mod['stat']==stat and r['node'] in mod['nodes'] and (not mod['gate'] or mod['gate'] in r['flags']))
 practice=min(2,training+mb)
 discovery=min(3,len(set(r['flags'])&{'trace','reference','consent','aether','pattern','certified'})) if r['node']=='contact' and not r.get('encounter') else 0
 base=c['attributes'][stat]; xp=min(2,p['xp']//3);total=base+xp+practice+discovery
 # Count actual d20 outcomes: natural 1 fails, natural 20 succeeds.
 chance=sum(d==20 or (d!=1 and d+total>=choice['dc']) for d in range(1,21))*5
 return dict(attribute=base,experience=xp,proficiency=training,proficiency_name=SKILLS[key]['label'] if rank else 'None applicable',mod=mb,practice=practice,findings=discovery,total=total,success_percent=chance)

def catalog():
 return dict(schema=1,attributes=ATTRIBUTES,origins=ORIGINS,forms=FORMS,affiliations=AFFILIATIONS,affinities=AFFINITIES,mods=MODS,skills=SKILLS,roles=ROLES,presets={r:default(r) for r in ROLES})
