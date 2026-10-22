"""Thorns adapters for the common Field Guide. Original chapter mode is retained."""
import copy
import hashlib
import characters
import field_rules as rules


def cell(w,p):
    import overland
    if w.get('mode')!='open':
        return dict(region='FOUR_CORNERS',title='Chapter expedition')
    c=overland.tile(w,*p['grid'])
    c.update(shelter=int(c['facility']=='sanctuary'),stability=80)
    return c


def setup(w,new=False):
    w.setdefault('seed',hashlib.sha256(w['code'].encode()).hexdigest()[:16])
    rules.ensure_world(w)
    if new:rules.enable(w,new=True)
    if not rules.active(w) or w.get('mode')!='open':return
    for player in w['players']:
        cm=player.get('contract')
        if cm:
            cm.setdefault('id',player['id']+':carried-contract:'+str(player.get('contract_serial',0)))
            cm.setdefault('escrow',{})
    if 'field_companions' not in w:
        w['field_companions']=[]
        for n,(name,role,goal,boundary) in enumerate([
            ('Sela Brace','Metal-kin Artisan','leave a working shelter for the next traveler','No abandonment of injured travelers'),
            ('Neri Reed','Seam Mediator','keep agreements understandable to everyone involved','No forced memory extraction')]):
            ch=characters.default(role)
            ch.update(pronouns='she/her' if n==0 else 'they/them',
                      bio=f'{name} learned around a communal repair bench in WN_TOWER. A storm scattered the workshop. A worn route washer preserves a tangible part of that history; its owner keeps competing accounts beside the evidence.',
                      goal=goal,boundary=boundary,appearance='Patched route layers and a carefully ordered tool wrap.',
                      voice='warm and deliberate' if n else 'plain and exact',mannerisms='checks a seam before replying')
            identity='field-companion:'+str(n)
            w['field_companions'].append(dict(id=identity,name=name,role=role,character=ch,
                x=0,y=0,pos=[0,0],faction='THORNS',health=100,energy=100,attitude=55,
                inventory=dict(food=3,water=4,scrap=2,seed=1,medkit=1),injuries=[],ailments=[],
                personal_reputation={},owner=None,memory=[],items=['route washer','field staff'],
                engagement=dict(phase='observe',task='support',events=[])))


def cycle(w,p,log,world_clock=True):
    p['steps']+=1;v=p['vitals']
    v['energy']=max(0,v['energy']-3)
    if w['hardcore']:
        for k,n in [('hunger',2),('thirst',4),('sleep',2 if 'rest_regulator' in p['loadout'] else 3)]:
            v[k]=min(100,v[k]+n)
        v['health']=max(0,v['health']-sum(v[k]>=90 for k in ['hunger','thirst','sleep'])*4-len(v['ailments']))
    rules.companion_cycle(w,p)
    if world_clock:rules.after_cycle(w,p,cell(w,p))
    f=w['field_rules']
    if world_clock and f['cycle']%4==0:
        phases=['observe','plan','work','reflect','recover']
        for a in w['field_companions']:
            phase=a['engagement']['phase']
            if a['energy']<15 or a['health']<35:phase='recover'
            if phase=='recover' or a['engagement']['task']=='rest':
                shelter=cell(w,dict(grid=a['pos']))['shelter']
                a['energy']=min(100,a['energy']+(14 if shelter else 6))
                if shelter:a['health']=min(100,a['health']+4)
            a['engagement']['events'].append(dict(cycle=f['cycle'],text=phase+' at '+str(a['pos'])))
            a['engagement']['events']=a['engagement']['events'][-30:]
            a['engagement']['phase']=phases[(phases.index(phase)+1)%5]
    if v['health']==0:
        p['grid']=[0,0];v.update(health=40,energy=40,hunger=35,thirst=35,sleep=35)
        log(w,p['name']+' is recovered to the local sanctuary; conditions and obligations remain.')
        return True
    return False


def finish(w,p,result,log):
    for _ in range(result.get('cycles',0)):
        cycle(w,p,log)
    pending=result.get('pending')
    e=rules.scene(w,p)
    if pending and pending['kind']=='full_rest' and e and any(rules.live(a) and a['disposition']=='defensive' for a in e['actors']):
        pending=None;result['text']+=' A defensive arrival interrupts the rest; its reserved rations remain spent.'
    rules.recovery(p,pending)
    if e and e.get('combat') and e['combat'].pop('conclude_pending',False):
        # One concluding cycle per participant, one shared watch-clock advance.
        first=True
        for ident in e['combat']['pcs']:
            member=next((x for x in w['players'] if x['id']==ident),None)
            if member:
                cycle(w,member,log,world_clock=first);first=False
    log(w,p['name']+': '+result['text']+(' '+result['mechanics'] if result.get('mechanics') else ''))


def field(w,p,action,target,log):
    rules.require(w['started'],'Begin the expedition first.')
    rules.require(w.get('mode')=='open' or action=='field_grow','Physical field play uses Open world mode.')
    rules.require(not any(p['id'] in x['players'] for x in w['duels']),'End your training duel before entering a field encounter.')
    finish(w,p,rules.handle(w,p,action,target,cell(w,p)),log)


def stock(w,p):
    return w['field_sites'].setdefault(rules.site_key(p),{}).setdefault('stock',dict(food=6,water=8,medkit=2,scrap=4,seed=2))


def native(w,p,d,check,log):
    import overland,world,generation
    op=d['op'];here=cell(w,p);inv=p['supplies'];rules.begin_action(p)
    check(not rules.current(w,p),'Finish the active field encounter before ordinary exploration.')
    if op=='ow_move':
        dx,dy=d.get('dx'),d.get('dy')
        check(type(dx)==int and type(dy)==int and abs(dx)+abs(dy)==1,'Move one surveyed connection.')
        check(not rules.bulk(p)['blocked'],'Transfer supplies before moving a load above twice capacity.')
        x,y=p['grid'];check(max(abs(x+dx),abs(y+dy))<=1000000,'Survey coordinate limit reached.')
        k=f'{x+dx},{y+dy}';check(k in w['overland_sites'] or len(w['overland_sites'])<2048,'The 2,048-site record is full.')
        w['overland_sites'].setdefault(k,overland.tile(w,x+dx,y+dy)['presentation']);p['grid']=[x+dx,y+dy]
        _,text=rules.roll(w,p,'body','transversal',10,'travel',support=True)
        finish(w,p,dict(text='You cross into '+cell(w,p)['title']+'.',mechanics=text,cycles=1),log);return
    if op=='ow_talk':overland.speak(w,p,here,d.get('topic','place'),check,log);return
    if here['depth']>=40:raise ValueError('Received semblance provides no verified person, material stock or services. Return to a surveyed site.')
    if op in {'ow_consume','ow_rest'}:
        item=d.get('item');action='field_breather' if op=='ow_rest' else {'food':'field_eat','water':'field_drink','medkit':'field_treat'}.get(item)
        check(action,'Choose a recorded supply.');field(w,p,action,'',log);return
    out='';cycles=1;mechanics=''
    if op=='ow_contract':
        check(here['facility'] in {'relay','market','sanctuary'} and not p['contract'],'Find a board and finish any current commitment.')
        provider=stock(w,p);check(provider['food']>=2 and provider['water']>=2 and provider['seed']>=1,'The board cannot reserve another reward from its real provision stock yet.')
        p['contract_serial']+=1;n=p['contract_serial'];x,y=p['grid'];f=world.REGIONAL[here['region']][0]
        cm=dict(id=p['id']+':contract:'+str(n),kind='Survey',faction=f,target=[x+2+(n%3),y+1],
                issuer=here['title'],issuer_pos=p['grid'][:],recipient='route recorder at the destination',scope='one truthful route survey',
                evidence='Percept/percept DC 10 at the destination',deadline=None,exit='Abandon freely; −1 issuer standing',
                context=world.contract_context(p.get('character',{}),f),
                escrow=dict(food=2,water=2,seed=1),reward='2 food, 2 water, 1 seed, 2 XP, +2 issuer standing')
        for k,n in cm['escrow'].items():provider[k]-=n
        p['contract']=cm;cycles=0;out='The board reserves its stated reward for '+cm['id']+'. Destination '+str(cm['target'])+'.'
    elif op=='ow_complete':
        cm=p['contract'];check(cm and p['grid']==cm['target'],'Reach the exact commitment coordinates.')
        check(all(inv.get(k,0)+v<=99 for k,v in cm.get('escrow',{}).items()),'Make room for the reward.')
        ok,mechanics=rules.roll(w,p,'percept','percept',10,'survey',faction=cm['faction'],support=True)
        if ok:
            paid=p.setdefault('paid_contracts',[]);check(cm['id'] not in paid,'This commitment is already paid.')
            for k,n in cm['escrow'].items():inv[k]=inv.get(k,0)+n
            paid.append(cm['id']);xp=rules.award(w,p,'contract:'+cm['id'],2)
            world.adjust(w,cm['faction'],2,'Witnessed route submission');p['personal_reputation'][cm['faction']]=rules.clamp(p['personal_reputation'].get(cm['faction'],0)+2,-20,20)
            p['contract']=None;p['benefits']=min(3,p['benefits']+1);out=f'Commitment paid once from its escrow; {xp} XP within the session cap.'
        else:out='The evidence remains incomplete; the reserved commitment stays open.'
    elif op=='ow_abandon':
        cm=p['contract'];check(cm,'No active commitment.')
        if cm.get('issuer_pos'):
            provider=w['field_sites'].get(','.join(map(str,cm['issuer_pos'])),{}).get('stock',{})
            for key,amount in cm.get('escrow',{}).items():provider[key]=provider.get(key,0)+amount
        world.adjust(w,cm['faction'],-1,'Closed commitment');p['contract']=None;cycles=0
        # Reserved goods return to the issuer, not the player.
        out='The commitment ends. Its reserved supplies stay with its issuer.'
    elif op=='ow_buy':
        check(here['facility'] in {'market','sanctuary'},'Find a local provision/craft service.')
        item=d.get('item');check(item in {'food','water','medkit'},'Choose a listed provision.')
        s=stock(w,p);check(s[item]>0 and inv[item]<99,'The service needs actual stock and your pack needs room.')
        cost=0 if here['facility']=='sanctuary' else 2 if item=='medkit' else 1
        check(inv['scrap']>=cost,'This local preparation consumes '+str(cost)+' scrap as material.')
        inv['scrap']-=cost;s[item]-=1;inv[item]+=1
        out='One '+item+' is transferred from finite local stock. Scrap is preparation material; no currency is awarded.'
    elif op=='ow_scavenge':
        check(here['facility'] in {'wilds','ruin'},'Accessible salvage lies in wilds or ruins.')
        s=stock(w,p);check(s['scrap']>0,'The accessible salvage budget is exhausted.')
        ok,mechanics=rules.roll(w,p,'tech','resource',12,'salvage',support=True)
        if ok:
            n=min(2,s['scrap'],99-inv['scrap']);s['scrap']-=n;inv['scrap']+=n
            rules.award(w,p,'site:'+rules.site_key(p)+':salvage')
            out=f'Recovered {n} actual local scrap; the site budget diminishes.'
        else:out='No reliable material is recovered.'
    elif op=='ow_mod':
        check(here['facility'] in {'clinic','sanctuary'},'Use a bounded craft service.')
        m=d.get('mod');check(m in overland.MODS,'Choose a listed mod.')
        if m in p['loadout']:p['loadout'].remove(m);out='The mod is removed without refund.'
        else:
            check(len(p['loadout'])<3 and inv['scrap']>=2,'Three slots; installation consumes two actual scrap.')
            inv['scrap']-=2;p['loadout'].append(m);p['licensed']=True
            if 'black.dot' not in p['credentials']:p['credentials'].append('black.dot')
            p.setdefault('credential_records',[]).append(dict(issuer=here['title'],holder=p['id'],activity='bounded field mod '+m,place=p['grid'][:],expiry=None,evidence='Physical service record'))
            out='Mod installed within the recorded field scope; no administrator access follows.'
    elif op=='ow_clinic':
        check(here['facility']=='sanctuary','A generated clinic is not evidence of WN_MED client eligibility. Local sanctuary care is available.')
        p['vitals'].update(health=100,injuries=[],ailments=[]);out='Local sanctuary care treats recorded conditions. Needs and provisions remain separate.'
    elif op=='ow_encounter':
        check(p.get('event') is not None,'No legacy event remains.');p['event']=None;cycles=0
        out='The carried legacy event is closed without altering its prior rewards.'
    else:raise ValueError('Unknown open-world action.')
    generation.witness(w,p,dict(action=op),here,list(w['contacts'].values()))
    finish(w,p,dict(text=out,mechanics=mechanics,cycles=cycles),log)
