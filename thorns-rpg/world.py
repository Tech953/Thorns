"""Procedural encounter and local interaction rules. All numbers are adaptations."""
import re
import secrets
FACTIONS={
 'THORNS':'Caravan confidence and care for entrusted records.',
 'Embrite':'Practical service, maintenance, and non-lethal retrieval.',
 'Druid-Sec':'Stability and care around ecological geometry.',
 'Fractech':'Bounded network work and infrastructure reliability.',
 'WN_LAW':'Respect for regulated expedition access.',
 'KHO / ED.NET':'Demonstrated learning and careful interpretation.',
 'OMNI-META.OPEND':'Respect for CITY_CLOUD_S node permissions.',
 'MMTX<':'Institutional archival fidelity; distinct from local residents.',
 'SEC.IO':'Compliance at restricted boundaries; reputation grants no immunity.',
 'FOOTHILL CUSP residents':'Mutual assistance and respect for ordinary lives.',
 'NanoClad':'Reliable observation and pilgrimage conduct.',
 'CHECKPOINT.RESID community':'Provision, reciprocity, and care for pilgrims.',
 'Lila / CASC':'Care with the prism and voluntary communication.',
}
FACTIONS.update({
 'Sap Core':'Reliability in elixir provision and contractual exchanges.',
 'Lifestring.CO':'Conduct around regulated Life Strings and augmentation.',
 'WN_MED':'Contracted care relationships; no automatic public treatment.',
 'MILI_WN':'Conduct toward mission-bound personnel; no command authority.',
 'WN_EDU':'Learning relationships; reputation is not certification.',
 'The Harvet':'Careful extraction and supply commitments.',
 'ANC.NI':'Reliable work around arcane inks and regulated bio-mods.',
 'MOD_OP':'Craft and verifiable exchange relationships.',
 'SPIDREsec':'Pilgrimage and infrastructure traversal relationships.',
 'initial_VERGE':'Observed conduct around NanoClad pilgrimage networks.',
 'ADMIN.COA':'Institutional trust does not grant admin permissions.',
 'PYRI':'A relationship record for offers, learning and voluntary integration.',
})
REGIONAL={
 'WN_TOWER':['Embrite','Druid-Sec','Fractech','WN_LAW','THORNS','Sap Core','Lifestring.CO','WN_MED','MILI_WN','WN_EDU','The Harvet','ANC.NI','MOD_OP','SPIDREsec'],
 'CITY_CLOUD_S':['KHO / ED.NET','OMNI-META.OPEND'],
 'ENACT_HILLS':['MMTX<','SEC.IO','FOOTHILL CUSP residents','ADMIN.COA','PYRI'],
 'AETHERGALE':['NanoClad','CHECKPOINT.RESID community','Lila / CASC','initial_VERGE'],
 'FOUR_CORNERS':['THORNS','NanoClad'],
}
# Each template supports three distinct resolution methods, with local narrative framing.
TEMPLATES=[
 dict(id='pilgrims',title='A delayed pilgrimage',body='A small group waits beside a route marker. Their transit reference disagrees with the path ahead.',approaches=[('Listen and agree on a safe route.','rapport','contracts'),('Read the conflicting route markers.','percept','percept'),('Repair the portable route reference.','tech','fractech')]),
 dict(id='salvage',title='A salvage dispute',body='Two crews dispute a loose apparatus. No one can establish whose retrieval claim was recorded first.',approaches=[('Mediate a voluntary shared claim.','rapport','contracts'),('Inspect the apparatus for a dated record.','percept','history'),('Stabilize the equipment before anyone moves it.','tech','metallurgy')]),
 dict(id='shelter',title='Shelter under interference',body='A temporary shelter is losing its anchors as a localized distortion passes. The occupants ask for help.',approaches=[('Organize the occupants into a repair team.','rapport','community'),('Secure the physical guide lines.','body','fieldcraft'),('Repair the stressed fasteners.','tech','metallurgy')]),
 dict(id='echo',title='An echo without context',body='A portable recording repeats a message attributed to someone who is not present. Its bearer wants a careful interpretation.',approaches=[('Ask what the bearer actually needs to know.','rapport','teaching'),('Separate observation from remembered semblance.','percept','percept'),('Compare the record against its own index.','tech','archive')]),
 dict(id='lesson',title='The unfinished exercise',body='A travelling student offers a harmless training pattern and asks where their interpretation failed.',approaches=[('Explain the uncertainty without imposing an answer.','rapport','teaching'),('Read the missing geometric relation.','percept','history'),('Correct the bounded practice parameters.','tech','fractech')]),
 dict(id='provision',title='A broken provision schedule',body='A delivery group has resources available but cannot reconcile who is expecting them. The dispute is over allocation, not ownership of an infinite supply.',approaches=[('Negotiate an allocation everyone can accept.','rapport','community'),('Carry the marked supplies to the waiting group.','body','fieldcraft'),('Repair the delivery ledger.','tech','archive')]),
]
TEMPLATES.extend([
 dict(id='ink',title='An ink manifest out of order',body='A sealed shipment of arcane ink has two incompatible manifests. Its custodians request help reconciling the records without opening the seals.',approaches=[('Ask both custodians to compare their commitments.','rapport','contracts'),('Inspect the packaging record and temporal notation.','percept','history'),('Trace the ink batch annotations in the ledger.','tech','needlurgy')]),
 dict(id='seam',title='A bounded seam exercise',body='A portable training console has paused a seam-control lesson. It requests diagnosis of a simulated fault, not access to the live network.',approaches=[('Help its student describe the error.','rapport','teaching'),('Read the percept difference between expected and actual output.','percept','percept'),('Correct the simulated seam parameters.','tech','seamllurgy')]),
 dict(id='crystal',title='The detuned reference',body='A crystallin< reference instrument produces an inconsistent reading. Its owner asks for a second opinion before trusting it.',approaches=[('Negotiate a pause until its limits are clear.','rapport','contracts'),('Compare the visible fracture pattern.','percept','percept'),('Retune the bounded reference apparatus.','tech','crystallin')]),
 dict(id='wood',title='A darkwood cargo record',body='A travelling custodian carries a sealed darkwood sample and an unclear extraction record. The request is for interpretation; the sample stays sealed.',approaches=[('Ask the custodian to document what remains uncertain.','rapport','community'),('Compare the recorded ecological geometry.','percept','druid'),('Repair the damaged record index.','tech','archive')]),
 dict(id='light',title='A borrowed light pattern',body='A traveller carries a copied lightPROKT< observation. They want to distinguish the observer’s notes from the projected record.',approaches=[('Invite the traveller to separate claim from observation.','rapport','teaching'),('Read the projection without claiming to own its subject.','percept','light'),('Check the observation archive for sequencing errors.','tech','archive')]),
 dict(id='rhetoric',title='A contract with shifting emphasis',body='A displayed contract repeats the same words with different emphasis. Its reader asks what is being promised, and what is merely implied.',approaches=[('Identify the rhetorical pressure without imposing agreement.','rapport','memetic'),('Compare the recorded versions.','percept','history'),('Trace the contract display’s node parameters.','tech','fractech')]),
])
ATMOSPHERE={
 'WN_TOWER':['Ash settles on the maintenance rails.','Greatweb overlays shimmer below the walkways.','A distant advertisement repeats through the fog.'],
 'CITY_CLOUD_S':['Mountain wind sounds against the metal terraces.','An educational projection flickers over the freight path.','Upper-sector permission markers remain visible overhead.'],
 'ENACT_HILLS':['Beyond the fields, restricted markers stand undisturbed.','Cooking smoke drifts from the residential paths.','A light projection makes the distant metallurgy gleam.'],
 'AETHERGALE':['Jade and rose contrails cross the dustlands.','A tent seam rattles in the AETHER wind.','Distant ARCrystallin< catches the changing light.'],
 'FOUR_CORNERS':['The route bends between regional networks.','A courier checks a fading transit reference.','Wind carries an uncertain transmission.'],
}
COMPLICATIONS=['The witnesses disagree about sequence.','The simplest record is incomplete.','There is time to help, but little room for guesswork.','A second group is waiting for the result.']

# These are explicit, whole-phrase cues, not free-form interpretation. They add
# descriptive context only; none changes an offer, check, reward, or permission.
WORK_CONTEXTS={
 'route/survey work':('courier','scout','surveyor','cartographer','mapmaker','route mapper','route recorder','guide','pilgrim'),
 'craft/repair work':('mechanic','repairer','artisan','metalworker','craftsperson','technician','engineer','seamllurgist','needlurgist'),
 'supply/trade work':('farmer','trader','merchant','supplier','provisioner','cook','caravan runner','vendor'),
 'care work':('medic','healer','nurse','caregiver','care worker','field medic'),
 'records/research work':('researcher','archivist','historian','scholar','analyst','scribe','record keeper'),
 'teaching/learning work':('teacher','tutor','instructor','educator','student','apprentice'),
 'ecology/stewardship work':('ecologist','botanist','cultivator','forager','gardener','druid'),
}
CONTRACT_WORK_CONTEXTS={
 'Survey':{'route/survey work','records/research work'},
}
CONTACT_TOPIC_WORK_CONTEXTS={
 'place':{'route/survey work','records/research work','ecology/stewardship work'},
 'needs':{'craft/repair work','supply/trade work','care work','ecology/stewardship work'},
 'history':{'route/survey work','records/research work','teaching/learning work'},
 'access':{'route/survey work','records/research work'},
 'contracts':{'route/survey work','records/research work','supply/trade work'},
 'plans':{'route/survey work','craft/repair work','records/research work','teaching/learning work','ecology/stewardship work'},
}
CONTACT_DIALOGUE_VARIATIONS={
 'place':{
  'route/survey work':'Route work frames this approach as a partial path, not a complete map.',
  'records/research work':'The local record is one account; it does not settle the whole region.',
  'ecology/stewardship work':'These conditions are observations, not a guarantee of what lives or grows here.'},
 'needs':{
  'craft/repair work':'A repair lens can clarify the stated need, but no tools or stock change hands in this conversation.',
  'supply/trade work':'Trade experience can help compare the stated need; talking still transfers no stock.',
  'care work':'Care work frames the concern, but this answer is not treatment.',
  'ecology/stewardship work':'A stewardship lens may help interpret the request; no resources appear automatically.'},
 'history':{
  'route/survey work':'A route record can anchor sequence while the wider history stays open.',
  'records/research work':'The contact’s local record remains one source, not a complete account.',
  'teaching/learning work':'A learner’s question can guide what to clarify, not what to conclude.'},
 'access':{
  'route/survey work':'Route knowledge can clarify a boundary, but it does not open one.',
  'records/research work':'A record can document the boundary; it cannot grant authority.'},
 'contracts':{
  'route/survey work':'Survey experience can distinguish route evidence from delivery terms.',
  'records/research work':'Record-keeping can check what is promised, not verify it before delivery.',
  'supply/trade work':'Supply experience can help compare escrow and reward; acceptance remains a separate action.'},
 'plans':{
  'route/survey work':'Route work can make a next step legible, not guarantee a safe crossing.',
  'craft/repair work':'Repair work can suggest a practical sequence, but no materials are committed here.',
  'records/research work':'Research can frame open questions without turning uncertainty into fact.',
  'teaching/learning work':'Teaching can surface the next question; it does not assign a skill bonus.',
  'ecology/stewardship work':'Stewardship can flag local conditions, not guarantee an outcome.'},
}
TEMPLATE_WORK_CONTEXTS={
 'pilgrims':{'route/survey work'},
 'salvage':{'craft/repair work','supply/trade work'},
 'shelter':{'craft/repair work','care work','ecology/stewardship work'},
 'echo':{'records/research work','teaching/learning work'},
 'lesson':{'records/research work','teaching/learning work'},
 'provision':{'supply/trade work','care work'},
 'ink':{'records/research work','supply/trade work'},
 'seam':{'craft/repair work','records/research work'},
 'crystal':{'craft/repair work','records/research work'},
 'wood':{'records/research work','supply/trade work','ecology/stewardship work'},
 'light':{'records/research work','teaching/learning work'},
 'rhetoric':{'records/research work','supply/trade work'},
}
RELATIONSHIP_ALIASES={
 'KHO / ED.NET':('KHO','ED.NET'),
 'FOOTHILL CUSP residents':('FOOTHILL CUSP',),
 'CHECKPOINT.RESID community':('CHECKPOINT.RESID',),
 'Lila / CASC':('Lila','CASC'),
}


def _normalized_phrase(value):
    if not isinstance(value,str):return ''
    return ' '.join(re.findall(r'[a-z0-9]+',value.casefold()))


def _mentions(text,phrase):
    hay=' '+_normalized_phrase(text)+' '
    needle=' '+_normalized_phrase(phrase)+' '
    return needle!='  ' and needle in hay


def character_context(character,work_contexts=(),faction=None):
    """Return recognized character links without exposing or interpreting raw prose."""
    character=character if isinstance(character,dict) else {}
    livelihood=character.get('livelihood','')
    relationship=character.get('relationship','')
    allowed=set(work_contexts or ())
    work=[label for label,aliases in WORK_CONTEXTS.items()
          if label in allowed and any(_mentions(livelihood,alias) for alias in aliases)]
    linked=None
    if faction in FACTIONS:
        aliases=(faction,)+RELATIONSHIP_ALIASES.get(faction,())
        if any(_mentions(relationship,alias) for alias in aliases):linked=faction
    return dict(livelihood=work,relationship=linked)


def contract_context(character,faction,kind='Survey'):
    return character_context(character,CONTRACT_WORK_CONTEXTS.get(kind,()),faction)


def contact_context(character,topic,faction):
    return character_context(character,CONTACT_TOPIC_WORK_CONTEXTS.get(topic,()),faction)


def contact_dialogue_variation(context,topic):
    """Authored narrative aside; never part of an NPC's claimed knowledge."""
    parts=[]
    for label in context.get('livelihood',()):
        line=CONTACT_DIALOGUE_VARIATIONS.get(topic,{}).get(label)
        if line:
            parts.append(line)
            break
    faction=context.get('relationship')
    if faction:
        parts.append('Your character’s record names '+faction+'; this exchange creates no new commitment.')
    return 'Narrative aside: '+' '.join(parts) if parts else ''


def encounter_context(character,template_id,faction):
    return character_context(character,TEMPLATE_WORK_CONTEXTS.get(template_id,()),faction)


def _context_text(context):
    parts=[]
    if context.get('livelihood'):parts.append('livelihood fit: '+', '.join(context['livelihood']))
    if context.get('relationship'):parts.append('relationship thread: '+context['relationship'])
    return '; '.join(parts)


def party_encounter_context(players,template_id,faction):
    result=[]
    for player in players:
        context=encounter_context(player.get('character',{}),template_id,faction)
        if context['livelihood'] or context['relationship']:
            result.append(dict(character=player.get('name','Expedition member'),**context))
    return result

def init(r):
 r.setdefault('reputation',{k:0 for k in FACTIONS});r.setdefault('rep_log',[])
 r.setdefault('procedural',False);r.setdefault('encounter',None);r.setdefault('encounter_history',[])
 r.setdefault('positions',{});r.setdefault('moved',{});r.setdefault('pvp_actions',{})
 r.setdefault('duels',[]);r.setdefault('encounter_serial',0)
 for p in r['players']:
  r['positions'].setdefault(p['id'],0)
  p.setdefault('composure',6+2*p.get('character',{}).get('attributes',{}).get('body',1))

def tier(value):
 return 'Trusted' if value>=6 else 'Welcomed' if value>=3 else 'Wary' if value<=-3 and value>-6 else 'Distrusted' if value<=-6 else 'Unknown / mixed'
def adjust(r,faction,delta,reason):
 init(r);before=r['reputation'][faction];limit=20 if r.get('field_rules',{}).get('enabled') else 10;after=max(-limit,min(limit,before+delta));r['reputation'][faction]=after
 r['rep_log'].append(dict(faction=faction,change=after-before,value=after,reason=reason));r['rep_log']=r['rep_log'][-60:]
def contact(r,origin,success):
 # Concrete acts only. Failure is not a universal moral penalty.
 mapping={'web':'Fractech','fractlands':'Druid-Sec','kho':'KHO / ED.NET','peak':'OMNI-META.OPEND','foothills':'FOOTHILL CUSP residents','archive':'MMTX<','pyri':'FOOTHILL CUSP residents','gale':'NanoClad','undertow':'NanoClad','contact':'Lila / CASC'}
 if success and origin in mapping:adjust(r,mapping[origin],1,'Successful expedition contribution at '+origin+'.')
 if r['node']=='answered':adjust(r,'THORNS',2,'Returned a voluntary account.');adjust(r,'Lila / CASC',2,'Established a bounded channel.')
 if r['node']=='witness':adjust(r,'THORNS',1,'Returned honest findings without extraction.')

def generate(r,region):
 init(r)
 if not r['procedural'] or r['encounter'] or secrets.randbelow(100)>=60:return
 recent=r['encounter_history'][-3:]
 pool=[t for t in TEMPLATES if t['id'] not in recent] or TEMPLATES
 t=secrets.choice(pool);f=secrets.choice(REGIONAL.get(region,REGIONAL['FOUR_CORNERS']))
 v=r['reputation'][f];modifier=-2 if v>=6 else -1 if v>=3 else 2 if v<=-6 else 1 if v<=-3 else 0
 base=secrets.choice([10,11,12,13]);r['encounter_serial']+=1
 # One applicable authored skill per option prevents arbitrary claims of proficiency.
 choices=[dict(label=a,stat=stat,dc=base+modifier,skill=sk,to=r['node'],fail=r['node'],need=None,flag=None,rep_delta=2,approach='check') for a,stat,sk in t['approaches']]
 choices.append(dict(label='Decline and continue the expedition.',stat=None,dc=0,skill=None,to=r['node'],fail=r['node'],need=None,flag=None,rep_delta=0,approach='leave'))
 context=party_encounter_context(r['players'],t['id'],f)
 text=secrets.choice(ATMOSPHERE.get(region,ATMOSPHERE['FOUR_CORNERS']))+'\n\n'+t['body']+' '+secrets.choice(COMPLICATIONS)+'\n\nRepresented contact: '+f+'. Your expedition is '+tier(v).lower()+'. Reputation changes difficulty by '+str(modifier)+'. Declining is permitted.'
 if context:
  text+='\n\nCharacter context (informational only): '+' | '.join(x['character']+' — '+_context_text(x) for x in context)
 r['encounter']=dict(region=region,title=t['title'],text=text,choices=choices,faction=f,id=r['encounter_serial'],template=t['id'],context=context)
 r['encounter_history'].append(t['id']);r['encounter_history']=r['encounter_history'][-20:]

def settle(r,choice,success):
 e=r['encounter']
 if choice['approach']=='check':adjust(r,e['faction'],2 if success else -1,'Random encounter: '+e['title']+' / '+('resolved' if success else 'unresolved commitment'))
 r['encounter']=None

def distance(r,a,b):
 if r.get('mode')=='open':
  pa,pb=[next(p for p in r['players'] if p['id']==i)['grid'] for i in [a,b]]
  return (abs(pa[0]-pb[0])+abs(pa[1]-pb[1]))*5
 return abs(r['positions'][a]-r['positions'][b])*5
def band(m):return 'contact' if m<=5 else 'near' if m<=10 else 'far'
def interaction(r,p,d,check,log):
 init(r);op=d['op'];pid=p['id']
 check(r['started'],'Start the expedition first.')
 from content import NODES
 check(bool(NODES[r['node']]['choices']),'The chapter has ended.')
 if op=='move':
  check(r.get('mode')!='open','Use the grid movement controls.')
  check(r['moved'].get(pid)!=r['turn'],'One move per shared turn.')
  step=d.get('step');check(type(step)==int and step in [-1,1],'Move one position left or right.')
  pos=r['positions'][pid]+step;check(0<=pos<=4,'Edge of the local scene.')
  r['positions'][pid]=pos;r['moved'][pid]=r['turn'];log(r,p['name']+' moved to local position '+str(pos)+'.');return
 tid=d.get('target');target=next((x for x in r['players'] if x['id']==tid),None)
 check(target is not None and tid!=pid,'Choose another present player.')
 m=distance(r,pid,tid)
 if op=='speak':
  check(m<=10,'Local speech reaches 10 metres. Party chat remains available at any distance.')
  speech_turn=p.get('steps',0) if r.get('mode')=='open' else r['turn']
  check(r['pvp_actions'].get(pid)!=speech_turn,'Move before speaking locally again; party chat remains available.')
  message=d.get('message','');check(isinstance(message,str) and 0<len(message.strip())<=160,'Use a message of 1–160 characters.')
  r['chat'].append(dict(name=p['name']+' → '+target['name']+' [local]',text=message));r['chat']=r['chat'][-50:];r['pvp_actions'][pid]=speech_turn;return
 duel=next((x for x in r['duels'] if set(x['players'])=={pid,tid}),None)
 if op=='challenge':
  check(m<=15,'Duel invitations reach 15 metres.')
  check(duel is None,'An invitation or duel already exists for this pair.')
  check(not any(pid in x['players'] or tid in x['players'] for x in r['duels']),'One pending or active duel per player.')
  r['duels'].append(dict(players=[pid,tid],inviter=pid,accepted=False));log(r,p['name']+' invited '+target['name']+' to a non-lethal duel.');return
 check(duel is not None,'No duel invitation for this pair.')
 if op=='accept':
  check(not duel['accepted'] and duel['inviter']!=pid,'Only the invited player can accept.')
  check(m<=15,'Move within 15 metres before accepting.')
  duel['accepted']=True;duel['next']=duel['inviter'];duel['round']=1;log(r,target['name']+' and '+p['name']+' accepted a non-lethal duel.');return
 if op=='disengage':
  r['duels'].remove(duel)
  for x in [p,target]:x['composure']=6+2*x['character']['attributes']['body']
  log(r,p['name']+' ended the invitation or duel. No reputation penalty.');return
 check(op=='duel_action' and duel['accepted'],'Both players must accept a duel.')
 check(duel.get('next',duel['inviter'])==pid,'Wait for the other player’s duel action.')
 style=d.get('style');check(style in ['close','ranged','feint'],'Invalid duel approach.')
 reach={'close':5,'ranged':15,'feint':10}[style];check(m<=reach,'Target is outside this approach’s reach.')
 stat='rapport' if style=='feint' else 'body';sk={'close':'transversal','ranged':'ballistics','feint':'contracts'}[style]
 attack=p['character']['attributes'][stat]+min(2,p['character']['skills'].get(sk,0))+min(2,p['xp']//3)
 defense=10+target['character']['attributes']['percept' if style=='feint' else 'body']
 roll=secrets.randbelow(20)+1;success=roll==20 or (roll!=1 and roll+attack>=defense)
 r['pvp_actions'][pid]=r['turn'];duel['next']=tid;duel['round']=duel.get('round',1)+1
 if success:target['composure']=max(0,target['composure']-(1 if style=='feint' else 2))
 log(r,f"Duel {p['name']} → {target['name']}: {style}, {m} m. D20 {roll} + {attack} vs {defense}: {'hit' if success else 'miss'}. Composure {target['composure']}.")
 if target['composure']==0:
  log(r,target['name']+' conceded the training duel. No extraction, XP, or faction reward.');r['duels'].remove(duel)
  for x in [p,target]:x['composure']=6+2*x['character']['attributes']['body']
