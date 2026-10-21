import unittest
from unittest.mock import patch
import server as s, overland as o, world as w
import test_game
class OverlandTests(unittest.TestCase):
 setUp=test_game.GameTests.setUp
 tearDown=test_game.GameTests.tearDown
 call=test_game.GameTests.call
 def open(self,hardcore=True):
  self.host=s.mutate(dict(op='create',ruleset='legacy',name='Scout',role='NanoClad Scout',mode='open',hardcore=hardcore,procedural=False))
  self.call('start')
 def test_grid_independence_and_determinism(self):
  self.host=s.mutate(dict(op='create',ruleset='legacy',name='Scout',role='NanoClad Scout',mode='open',procedural=False))
  guest=self.call('join',name='Other',role='Light Reader');self.call('start')
  r=self.call('ow_move',dx=1,dy=0);self.assertEqual(r['players'][0]['grid'],[1,0]);self.assertEqual(r['players'][1]['grid'],[0,0]);self.assertEqual(w.distance(r,self.host['id'],guest['id']),5)
  self.assertEqual(o.tile(r,400,201),o.tile(s.fetch(r['code']),400,201));self.assertIn('projection',o.tile(r,400,201)['text'])
  with self.assertRaises(ValueError):self.call('ow_move',dx=2,dy=0)
  with self.assertRaises(ValueError):self.call('vote',choice=0)
 def test_survival_resources_and_care(self):
  self.open();self.call('ow_move',dx=1,dy=0);r=self.call('ow_move',dx=-1,dy=0);p=r['players'][0];self.assertEqual(p['vitals']['thirst'],10)
  r=self.call('ow_consume',item='water');self.assertEqual(r['players'][0]['vitals']['thirst'],0)
  r=s.fetch(r['code']);p=r['players'][0];p['vitals'].update(injuries=['strain'],ailments=['irritation']);s.save(r)
  r=self.call('ow_clinic');self.assertEqual(r['players'][0]['vitals']['ailments'],[])
  for _ in range(4):self.call('ow_consume',item='food')
  with self.assertRaises(ValueError):self.call('ow_consume',item='food')
 def test_contract_requires_success_and_persists_benefits(self):
  self.open();r=self.call('ow_contract');c=r['players'][0]['contract']
  with self.assertRaises(ValueError):self.call('ow_complete')
  for dx,dy in [(1,0),(1,0),(0,1)]:self.call('ow_move',dx=dx,dy=dy)
  with patch('overland.secrets.randbelow',return_value=0):r=self.call('ow_complete')
  self.assertIsNotNone(r['players'][0]['contract'])
  with patch('overland.secrets.randbelow',return_value=19):r=self.call('ow_complete')
  p=r['players'][0];self.assertIsNone(p['contract']);self.assertEqual(p['benefits'],1);self.assertEqual(p['karma'],2);self.assertEqual(r['reputation'][c['faction']],2)
  self.assertEqual(s.fetch(r['code'])['players'][0]['benefits'],1)
 def test_contract_preview_and_saved_context_do_not_change_terms(self):
  self.open(False);r=s.fetch(self.host['code']);p=r['players'][0]
  p['character'].update(livelihood='Independent courier',relationship='I owe Embrite a safe return');s.save(r)
  preview=self.call('state')['players'][0]['overland']['contract_preview']
  self.assertEqual(preview['context'],{'livelihood':['route/survey work'],'relationship':'Embrite'})
  contract=self.call('ow_contract')['players'][0]['contract']
  self.assertEqual(contract['context'],preview['context'])
  self.assertEqual((contract['kind'],contract['faction'],contract['target'],contract['reward']),
                   ('Survey and return a verified route record','Embrite',[2,1],18))
 def test_mod_cost_limit_and_bonus(self):
  self.open();r=s.fetch(self.host['code']);r['players'][0]['credits']=100;s.save(r)
  for m in ['survey_lens','filter_graft','rest_regulator']:r=self.call('ow_mod',mod=m)
  self.assertEqual(r['players'][0]['credits'],64)
  with self.assertRaises(ValueError):self.call('ow_mod',mod='bio_glass')
  self.call('ow_mod',mod='filter_graft');r=self.call('ow_mod',mod='bio_glass');self.assertEqual(len(r['players'][0]['loadout']),3)
 def test_standard_no_needs_and_rescue(self):
  self.open(False);r=self.call('ow_move',dx=1,dy=0);self.assertEqual(r['players'][0]['vitals']['thirst'],0)
  r=s.fetch(r['code']);r['hardcore']=True;r['players'][0]['vitals'].update(health=1,thirst=99);s.save(r)
  r=self.call('ow_move',dx=1,dy=0);self.assertEqual(r['players'][0]['grid'],[0,0]);self.assertEqual(r['players'][0]['vitals']['health'],35)
 def test_encounter_blocks_movement_and_declines(self):
  self.open(False);r=s.fetch(self.host['code']);r['procedural']=True
  r['players'][0]['character'].update(livelihood='courier',relationship='Embrite');s.save(r)
  with patch('overland.secrets.randbelow',return_value=0),patch('world.secrets.choice',side_effect=lambda values:values[0]):
   r=self.call('ow_move',dx=1,dy=0)
  self.assertIsNotNone(r['players'][0]['event'])
  self.assertEqual(r['players'][0]['event']['context'],{'livelihood':['route/survey work'],'relationship':'Embrite'})
  with self.assertRaises(ValueError):self.call('ow_move',dx=1,dy=0)
  r=self.call('ow_encounter',choice=3);self.assertIsNone(r['players'][0]['event'])
 def test_duel_can_finish_without_story(self):
  self.host=s.mutate(dict(op='create',ruleset='legacy',name='Scout',role='NanoClad Scout',mode='open',procedural=False));g=self.call('join',name='Guest',role='Light Reader');self.call('start');self.call('challenge',target=g['id']);self.call('accept',g,target=self.host['id'])
  with patch('world.secrets.randbelow',return_value=19):
   for i in range(30):
    who,other=(self.host,g) if i%2==0 else (g,self.host)
    r=self.call('duel_action',who,target=other['id'],style='close')
    if not r['duels']:break
  self.assertFalse(r['duels']);self.assertEqual(r['turn'],0)
if __name__=='__main__':unittest.main()
