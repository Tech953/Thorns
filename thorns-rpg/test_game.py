import tempfile, unittest, threading
from unittest.mock import patch
from pathlib import Path
import server as s
from content import NODES
class GameTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); s.init_db(str(Path(self.tmp.name)/'test.db'))
  self.host=s.mutate(dict(op='create',ruleset='legacy',name='Host',role='Needlurgist',procedural=False))
 def tearDown(self): s.DB.close();self.tmp.cleanup()
 def call(self,op,who=None,**kw):
  who=who or self.host
  r=s.fetch(who['code'])
  return s.mutate(dict(**who,op=op,revision=r['revision'],**kw))
 def test_capacity_and_secrets(self):
  for i in range(5): self.call('join',name=str(i),role='Light Reader')
  with self.assertRaises(ValueError): self.call('join',name='Seven',role='Light Reader')
  self.assertNotIn('token',self.call('state')['players'][0])
  with self.assertRaises(ValueError): s.mutate(dict(op='state',code=self.host['code'],token='forged'))
 def test_authority_stale_and_transfer(self):
  guest=self.call('join',name='Guest',role='Light Reader')
  with self.assertRaises(ValueError): self.call('start',guest)
  with self.assertRaises(ValueError): s.mutate(dict(**self.host,op='start',revision=-1))
  self.call('leave');self.assertEqual(self.call('state',guest)['host'],guest['id'])
 def test_six_concurrent_votes_resolve_once(self):
  players=[self.host]+[self.call('join',name=str(i),role='Light Reader') for i in range(5)]
  self.call('start')
  failures=[]
  def vote(p):
   try:
    with s.LOCK:self.call('vote',p,choice=0)
   except Exception as e:failures.append(e)
  threads=[threading.Thread(target=vote,args=(p,)) for p in players]
  for t in threads:t.start()
  for t in threads:t.join()
  self.assertFalse(failures);r=self.call('state');self.assertEqual(r['turn'],1);self.assertEqual(r['node'],'web')
  with self.assertRaises(ValueError):self.call('join',name='Late',role='Light Reader')
 def test_critical_rolls(self):
  self.call('start');self.call('vote',choice=0)
  with patch('server.secrets.randbelow',return_value=0):self.call('vote',choice=0)
  r=self.call('state');self.assertEqual(r['node'],'fractlands');self.assertEqual(r['cohesion'],8)
  with patch('server.secrets.randbelow',return_value=19):self.call('vote',choice=0)
  self.assertIn('wood',self.call('state')['flags'])
 def test_reachable_nodes_and_choice_gates(self):
  visited=set();queue=['arcturion']
  while queue:
   key=queue.pop()
   if key in visited:continue
   visited.add(key)
   for c in NODES[key]['choices']:
    self.assertIn(c['to'],NODES);self.assertIn(c['fail'],NODES);queue.extend([c['to'],c['fail']])
  self.assertEqual(set(NODES)-visited,{'lost'})
  r=s.fetch(self.host['code']);r['node']='archive';self.assertEqual(len(s.options(r)),2);r['flags']=['registered'];self.assertEqual(len(s.options(r)),3)
 def test_both_routes_complete_and_persist(self):
  for route in [0,1]:
   if route:self.host=s.mutate(dict(op='create',ruleset='legacy',name='Other',role='Seam Mediator',procedural=False))
   self.call('start')
   with patch('server.secrets.randbelow',return_value=19):
    for i in [0,0,route,0,0,0,1,0]:self.call('vote',choice=i)
   r=self.call('state');self.assertEqual(r['node'],'answered')
   s.DB.close();s.init_db(str(Path(self.tmp.name)/'test.db'));self.assertEqual(self.call('state')['node'],'answered')
 def test_vote_lock_and_early_resolution(self):
  guest=self.call('join',name='Guest',role='Light Reader');self.call('start');self.call('vote',choice=0)
  with self.assertRaises(ValueError):self.call('actor',actor=guest['id'])
  with self.assertRaises(ValueError):self.call('resolve',guest)
  self.call('resolve');self.assertEqual(self.call('state')['turn'],1)
if __name__=='__main__':unittest.main()
