#!/usr/bin/env python3
"""THORNS: authoritative, persisted, 1–6 player cooperative RPG. Python stdlib only."""
import argparse, collections, copy, json, os, secrets, sqlite3, threading, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from content import NODES, ROLES, CODEX
import characters
import world
import overland
import field_rules
import field_adventure
ROOT=Path(__file__).resolve().parent
LOCK=threading.RLock()
DB=None

def check(ok,msg):
 if not ok: raise ValueError(msg)
def save(r):
 DB.execute('INSERT OR REPLACE INTO rooms VALUES (?, ?, ?)',(r['code'],time.time(),json.dumps(r)))
 DB.commit()
def fetch(code):
 row=DB.execute('SELECT state FROM rooms WHERE code=?',(code,)).fetchone()
 check(row,'Room not found. Check the code and server address.')
 r=json.loads(row[0])
 for p in r['players']: characters.ensure(p)
 world.init(r);overland.init(r);field_adventure.setup(r)
 return r
def log(r,msg):
 r['log'].append(msg); r['log']=r['log'][-100:]
def options(r): return [x for x in (r.get('encounter') or NODES[r['node']])['choices'] if not x['need'] or x['need'] in r['flags']]
def public(r):
 world.init(r);overland.init(r)
 s=copy.deepcopy(r)
 for p in s['players']:
  p.pop('token',None); p['sheet']=characters.sheet(p,r)
  if r['mode']=='open':p['overland']=overland.view(r,p)
  p['field_guide']=field_rules.public(r,next(x for x in r['players'] if x['id']==p['id']),field_adventure.cell(r,p))
 s['scene']=copy.deepcopy(r.get('encounter') or NODES[r['node']]); s['scene']['choices']=copy.deepcopy(options(r))
 actor=next(p for p in r['players'] if p['id']==r['actor'])
 for choice in s['scene']['choices']: choice['check']=characters.breakdown(actor,r,choice)
 s['roles']=ROLES; s['codex']=CODEX
 s['reputation_tiers']={k:world.tier(v) for k,v in r['reputation'].items()};s['factions']=world.FACTIONS
 return s
def identity(r,token):
 p=next((p for p in r['players'] if secrets.compare_digest(p['token'],token)),None)
 check(p is not None,'Session not recognized. Rejoin the room.'); return p
def person(d):
 name=str(d.get('name','')).strip()[:24]; role=d.get('role')
 check(name and all(ord(c)>=32 for c in name),'Enter a character name.')
 check(isinstance(role,str) and role in ROLES,'Choose a valid role.')
 return dict(id=secrets.token_hex(6),token=secrets.token_urlsafe(32),name=name,role=role,xp=0,character=characters.validate(d['character'],role) if 'character' in d else characters.default(role))
def resolve(r):
 origin=r['node'];is_encounter=bool(r.get('encounter'))
 counts=collections.Counter(r['votes'].values()); check(counts,'At least one vote is required.')
 best=max(counts.values()); tied=sorted(k for k,v in counts.items() if v==best)
 choice_index=secrets.choice(tied); choice=options(r)[choice_index]
 if len(tied)>1: log(r,'Tied vote: server randomly selected one of the tied choices.')
 actor=next(p for p in r['players'] if p['id']==r['actor'])
 log(r,actor['name']+' leads: '+choice['label'])
 success=True
 if choice['stat']:
  die=field_rules.die(r,20,actor['id']+':chapter:'+origin) if field_rules.active(r) else secrets.randbelow(20)+1
  parts=characters.breakdown(actor,r,choice); bonus=parts['total']
  log(r,f"Bonus: attribute {parts['attribute']} + experience {parts['experience']} + practice {parts['practice']} (training/equipment capped at 2) + findings {parts['findings']}.")
  success=die==20 or (die!=1 and die+bonus>=choice['dc'])
  log(r,f"D20 {die} + {bonus} {choice['stat']} = {die+bonus} vs {choice['dc']}: {'SUCCESS' if success else 'SETBACK'}.")
  if field_rules.active(r):
   outcome=field_rules.grade(die,bonus,choice['dc']);log(r,'Field Guide outcome: '+outcome)
   if success:field_rules.award(r,actor,'chapter:'+origin+':'+str(r['encounter']['id'] if is_encounter else 'story'))
  else:actor['xp']+=1
  if not success: r['cohesion']=max(0,r['cohesion']-2)
 if success and choice['flag'] and choice['flag'] not in r['flags']: r['flags'].append(choice['flag'])
 if is_encounter: world.settle(r,choice,success)
 else:
  r['node']=choice['to'] if success else choice['fail']
  world.contact(r,origin,success)
 if r['cohesion']<=0: r['node']='lost'
 if r['node']=='resid' and not is_encounter: r['cohesion']=10; log(r,'CHECKPOINT.RESID restores expedition cohesion to 10.')
 r['votes']={}; r['turn']+=1
 if not is_encounter:
  r['positions']={p['id']:0 for p in r['players']};r['duels']=[]
  for p in r['players']:p['composure']=6+2*characters.ensure(p)['attributes']['body']
  log(r,'Arrived: '+NODES[r['node']]['title'])
  if NODES[r['node']]['choices']:world.generate(r,NODES[r['node']]['region'])
 else: log(r,'Encounter closed. Returning to '+NODES[r['node']]['title'])

def mutate(d):
 op=d.get('op'); code=str(d.get('code','')).upper().strip()
 if op=='create':
  check(DB.execute('SELECT COUNT(*) FROM rooms').fetchone()[0]<1000,'Server room limit reached.')
  p=person(d)
  while True:
   code=''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(8))
   if not DB.execute('SELECT 1 FROM rooms WHERE code=?',(code,)).fetchone(): break
  r=dict(code=code,host=p['id'],players=[p],actor=p['id'],node='arcturion',started=False,turn=0,revision=0,cohesion=10,flags=[],votes={},log=['Expedition assembled at the Arcturion.'],chat=[])
  check(type(d.get('procedural',True))==bool,'Procedural setting must be boolean.')
  check(d.get('mode','chapter') in ['chapter','open'],'Invalid mode.')
  check(type(d.get('hardcore',False))==bool,'Hardcore must be boolean.')
  r['mode']=d.get('mode','chapter');r['hardcore']=d.get('hardcore',False)
  r['procedural']=d.get('procedural',True);world.init(r);overland.init(r)
  check(d.get('ruleset','field-guide-1') in {'legacy','field-guide-1'},'Invalid ruleset.')
  field_adventure.setup(r,new=d.get('ruleset','field-guide-1')=='field-guide-1')
  save(r); return dict(code=code,token=p['token'],id=p['id'])
 r=fetch(code)
 if op=='join':
  check(not r['started'],'This expedition has started. Ask the host to create a new room.')
  check(len(r['players'])<6,'This room already has six players.')
  p=person(d); r['players'].append(p);overland.init(r);field_adventure.setup(r)
  if field_rules.active(r):field_rules.ensure_player(p,new=True)
  r['revision']+=1; save(r)
  return dict(code=code,token=p['token'],id=p['id'])
 p=identity(r,str(d.get('token','')))
 if op=='state': return public(r)
 if op=='chat':
  msg=str(d.get('message','')).strip()[:300]; check(msg,'Enter a message.')
  r['chat'].append(dict(name=p['name'],text=msg)); r['chat']=r['chat'][-50:]
 else:
  check(d.get('revision')==r['revision'],'The room changed. Review the latest state and try again.')
  if op=='start': check(p['id']==r['host'] and not r['started'],'Only the host can start the lobby.'); r['started']=True
  elif op in {'field_adopt','field_session','field_goal','field'}:
   if op=='field_adopt':
    check(p['id']==r['host'] and not field_rules.active(r),'Only the host can adopt the new rules once.')
    check(not r['votes'] and not r.get('encounter') and not r['duels'],'Close pending votes, chapter encounters and duels first.')
    field_rules.enable(r);field_adventure.setup(r);log(r,'Field Guide rules adopted; prior identities, XP and inventory retained.')
   elif op=='field_session':
    check(p['id']==r['host'] and field_rules.active(r),'Only the host can begin a session.')
    check(not any(v.get('encounter',{}).get('combat') and not v['encounter']['combat']['finished'] for v in r['field_sites'].values()),'Finish active encounters first.')
    r['field_rules']['session']+=1;log(r,'Host declared a new tabletop session.')
   elif op=='field_goal':
    check(p['id']==r['host'] and field_rules.active(r),'Only the host can record an agreed goal.')
    member=next((x for x in r['players'] if x['id']==d.get('target')),None);check(member,'Choose a party member.')
    field_rules.award(r,member,'goal:'+str(r['field_rules']['session']),1,goal=True)
   else:
    name=d.get('action');target=d.get('target','')
    check(name in field_rules.ACTS and isinstance(target,str) and len(target)<=200,'Invalid field action.')
    field_adventure.field(r,p,name,target,log)
  elif isinstance(op,str) and op.startswith('ow_'):
   overland.act(r,p,d,check,log)
  elif op in ['move','speak','challenge','accept','disengage','duel_action']:
   check(not field_rules.current(r,p) or op=='disengage','Finish the local field encounter before starting another interaction.')
   world.interaction(r,p,d,check,log)
  elif op=='character':
   check(not r['started'],'Character editing locks when the expedition starts.')
   role=d.get('role',p['role'])
   check(isinstance(role,str) and role in ROLES,'Invalid discipline.')
   updated=characters.validate(d.get('character'),role)
   name=d.get('name',p['name'])
   check(isinstance(name,str) and 0<len(name.strip())<=24 and all(ord(c)>=32 for c in name),'Invalid character name.')
   p.update(name=name.strip(),role=role,character=updated,composure=6+2*updated['attributes']['body'])
  elif op=='actor':
   check(p['id']==r['host'],'Only the host can select the specialist.')
   check(not r['votes'],'Change specialist before voting begins.')
   check(any(x['id']==d.get('actor') for x in r['players']),'Unknown specialist.')
   r['actor']=d['actor']
  elif op=='vote':
   check(r['mode']=='chapter','Use open-world actions in this room.')
   check(r['started'],'The host must start the expedition.')
   i=d.get('choice'); check(type(i)==int and 0<=i<len(options(r)),'Invalid choice.')
   r['votes'][p['id']]=i
   if len(r['votes'])==len(r['players']): resolve(r)
  elif op=='resolve':
   check(r['mode']=='chapter','Use open-world actions in this room.')
   check(p['id']==r['host'] and r['started'],'Only the host can resolve a running expedition.')
   resolve(r)
  elif op=='leave':
   check(len(r['players'])>1,'The last player can close the browser; the saved room remains.')
   for duel in r['duels']:
    if p['id'] in duel['players']:
     for member in r['players']:
      if member['id'] in duel['players']: member['composure']=6+2*member['character']['attributes']['body']
   r['duels']=[x for x in r['duels'] if p['id'] not in x['players']]
   r['players']=[x for x in r['players'] if x['id']!=p['id']]; r['votes'].pop(p['id'],None)
   field_rules.release_seat(r,p['id'])
   if r['host']==p['id']: r['host']=r['players'][0]['id']
   if r['actor']==p['id']: r['actor']=r['host']; r['votes']={}
   elif r['started'] and r['votes'] and len(r['votes'])==len(r['players']):resolve(r)
  else: raise ValueError('Unknown action.')
  r['revision']+=1
 save(r); return public(r)

class Handler(BaseHTTPRequestHandler):
 def reply(self,status,payload,ctype='application/json'):
  body=payload if isinstance(payload,bytes) else json.dumps(payload).encode()
  self.send_response(status); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(body)))
  self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff')
  self.send_header('Content-Security-Policy',"default-src 'self'; img-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'")
  self.end_headers(); self.wfile.write(body)
 def do_GET(self):
  path=urlparse(self.path).path
  files={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript'),'/openworld.js':('openworld.js','text/javascript'),'/creator.js':('creator.js','text/javascript'),'/style.css':('style.css','text/css'),'/world-map.jpg':('world-map.jpg','image/jpeg'),'/needle-map.jpg':('needle-map.jpg','image/jpeg')}
  if path=='/character-catalog': return self.reply(200,characters.catalog())
  if path=='/health': return self.reply(200,{'ok':True,'version':'0.6.0'})
  if path=='/field-guide.js':return self.reply(200,(ROOT/'static/field-guide.js').read_bytes(),'text/javascript')
  if path=='/field-catalog':return self.reply(200,field_rules.CATALOG)
  if path not in files: return self.reply(404,{'error':'Not found'})
  name,mime=files[path]; self.reply(200,(ROOT/'static'/name).read_bytes(),mime)
 def do_POST(self):
  try:
   check(self.path=='/api','Not found')
   check(self.headers.get('Content-Type','').split(';')[0]=='application/json','JSON required.')
   size=int(self.headers.get('Content-Length','0')); check(0<size<=8192,'Invalid request size.')
   self.connection.settimeout(10)
   d=json.loads(self.rfile.read(size)); check(isinstance(d,dict),'JSON object required.')
   with LOCK: result=mutate(d)
   self.reply(200,result)
  except (ValueError,TypeError,KeyError) as e: self.reply(400,{'error':str(e)})
 def log_message(self,*args): pass

def init_db(path):
 global DB
 DB=sqlite3.connect(path,check_same_thread=False)
 DB.execute('CREATE TABLE IF NOT EXISTS rooms (code TEXT PRIMARY KEY, updated REAL, state TEXT)'); DB.commit()
if __name__=='__main__':
 a=argparse.ArgumentParser(); a.add_argument('--host',default='0.0.0.0'); a.add_argument('--port',type=int,default=int(os.environ.get('PORT','8765'))); a.add_argument('--db',default=str(ROOT/'thorns-saves.sqlite3')); args=a.parse_args()
 init_db(args.db)
 print(f'THORNS running at http://localhost:{args.port} — LAN: use this computer’s LAN IP and port. Ctrl+C stops.',flush=True)
 ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
