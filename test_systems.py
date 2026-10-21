import copy, unittest
from unittest.mock import patch
import characters as c
import world as w
import server as s
import test_game
class SystemsTests(unittest.TestCase):
 setUp=test_game.GameTests.setUp
 tearDown=test_game.GameTests.tearDown
 call=test_game.GameTests.call
 def test_point_budgets_and_injection(self):
  raw=c.default('Needlurgist');raw.pop('legacy')
  self.assertEqual(c.validate(raw,'Needlurgist')['attributes']['tech'],4)
  partial=copy.deepcopy(raw);partial['skills']={}
  with self.assertRaises(ValueError):c.validate(partial,'Needlurgist')
  partial['schema']=1
  grandfathered=c.validate(partial,'Needlurgist',allow_legacy_training=True)
  self.assertEqual(grandfathered['schema'],1);self.assertEqual(sum(grandfathered['skills'].values()),0)
  with self.assertRaises(ValueError):c.validate(partial,'Needlurgist')
  for kind in ['over','bool','unknown','privilege','skill','negative']:
   bad=copy.deepcopy(raw)
   if kind=='over':bad['attributes']['tech']=5
   if kind=='bool':bad['attributes']['body']=True
   if kind=='unknown':bad['skills']['omnipotence']=3
   if kind=='privilege':bad['admin.OS']='verified'
   if kind=='skill':bad['skills']={'fractech':3,'archive':3,'teaching':1}
   if kind=='negative':bad['skills']['fractech']=-1
   with self.assertRaises(ValueError):c.validate(bad,'Needlurgist')
 def test_customize_lock_and_legacy(self):
  raw=c.default('Needlurgist');raw.pop('legacy');raw['attributes']={'body':2,'tech':2,'percept':2,'rapport':2}
  self.call('character',character=raw);self.assertEqual(self.call('state')['players'][0]['sheet']['attributes']['tech'],2)
  self.call('start')
  with self.assertRaises(ValueError):self.call('character',character=raw)
  r=s.fetch(self.host['code']);del r['players'][0]['character'];s.save(r)
  restored=self.call('state')['players'][0]['sheet'];self.assertTrue(restored['legacy']);self.assertEqual(restored['skills'],{})
 def test_story_fields_and_grandfathered_training(self):
  stored=c.default('Needlurgist',legacy=True);stored['skills']={'archive':1}
  for field in ('livelihood','question','relationship'):stored.pop(field)
  r=s.fetch(self.host['code']);p=r['players'][0];p['character']=stored;s.save(r)
  story=copy.deepcopy(stored);story.pop('legacy')
  story.update(livelihood='Trail mechanic',question='Who mapped the undercroft?',relationship='Owes a safe return to Mira')
  self.call('character',character=story)
  sheet=self.call('state')['players'][0]['sheet']
  self.assertEqual(sheet['schema'],1);self.assertEqual(sheet['skills'],{'archive':1})
  for field in ('livelihood','question','relationship'):
   self.assertEqual(sheet[field],story[field])
  changed=copy.deepcopy(story);changed['skills']={'archive':2}
  with self.assertRaises(ValueError):self.call('character',character=changed)
  completed=copy.deepcopy(story);completed['skills']={'archive':1,'fractech':3,'community':2}
  self.call('character',character=completed)
  sheet=self.call('state')['players'][0]['sheet']
  self.assertEqual(sheet['schema'],2);self.assertEqual(sum(sheet['skills'].values()),6)
 def test_check_breakdown_and_mod_gate(self):
  r=s.fetch(self.host['code']);p=r['players'][0];r['node']='web';p['character']['mod']='meta_fingers';p['character']['skills']={}
  a=c.breakdown(p,r,s.options(r)[0]);self.assertEqual(a['mod'],0)
  r['flags']=['registered'];b=c.breakdown(p,r,s.options(r)[0]);self.assertEqual(b['mod'],1)
  p['character']['skills']['fractech']=3;b=c.breakdown(p,r,s.options(r)[0]);self.assertEqual(b['practice'],2)
  self.assertTrue(5<=b['success_percent']<=95)
 def test_encounter_reputation_and_no_immediate_repeat(self):
  r=s.fetch(self.host['code']);r['procedural']=True
  history=[]
  with patch('world.secrets.randbelow',return_value=0):
   for _ in range(8):
    w.generate(r,'WN_TOWER');e=r['encounter'];self.assertNotIn(e['template'],history[-3:]);history.append(e['template'])
    before=r['reputation'][e['faction']];w.settle(r,e['choices'][0],True);self.assertEqual(r['reputation'][e['faction']],min(10,before+2))
  f='THORNS';w.adjust(r,f,100,'test');self.assertEqual(r['reputation'][f],10);w.adjust(r,f,-100,'test');self.assertEqual(r['reputation'][f],-10)
 def test_encounter_difficulty_and_decline(self):
  r=s.fetch(self.host['code']);r['procedural']=True
  for f in w.FACTIONS:r['reputation'][f]=6
  with patch('world.secrets.randbelow',return_value=0):w.generate(r,'CITY_CLOUD_S')
  self.assertTrue(8<=r['encounter']['choices'][0]['dc']<=11)
  before=copy.deepcopy(r['reputation']);w.settle(r,r['encounter']['choices'][-1],True);self.assertEqual(r['reputation'],before)
 def test_context_links_require_recognized_whole_phrases(self):
  context=w.character_context(
   {'livelihood':'Trail courier and cartographer','relationship':'I promised Lila a safe return.'},
   {'route/survey work'},'Lila / CASC')
  self.assertEqual(context,{'livelihood':['route/survey work'],'relationship':'Lila / CASC'})
  unmatched=w.character_context(
   {'livelihood':'courierly consultant','relationship':'A distant admirer'},
   {'route/survey work'},'Embrite')
  self.assertEqual(unmatched,{'livelihood':[],'relationship':None})
 def test_context_notes_do_not_change_generated_encounter_rules(self):
  plain=s.fetch(self.host['code']);plain['procedural']=True
  linked=copy.deepcopy(plain)
  linked['players'][0]['character'].update(livelihood='Courier',relationship='I owe Embrite a safe return')
  with patch('world.secrets.randbelow',return_value=0),patch('world.secrets.choice',side_effect=lambda values:values[0]):
   w.generate(plain,'WN_TOWER')
  with patch('world.secrets.randbelow',return_value=0),patch('world.secrets.choice',side_effect=lambda values:values[0]):
   w.generate(linked,'WN_TOWER')
  a,b=plain['encounter'],linked['encounter']
  self.assertEqual((a['template'],a['faction'],a['choices']),(b['template'],b['faction'],b['choices']))
  self.assertEqual(a['context'],[])
  self.assertEqual(b['context'],[{'character':'Host','livelihood':['route/survey work'],'relationship':'Embrite'}])
  self.assertIn('Narrative aside: Host — Route-reading experience',b['text'])
  self.assertEqual(b['variation'],w.party_encounter_variation(b['context'],b['template']))
 def test_contract_and_encounter_asides_are_deterministic_and_context_only(self):
  contract={'livelihood':['records/research work'],'relationship':'Embrite'}
  note=w.contract_context_variation(contract)
  self.assertIn('Records work',note)
  self.assertIn('adds no terms',note)
  self.assertEqual(note,w.contract_context_variation(contract))
  encounter={'livelihood':['care work'],'relationship':'Embrite'}
  note=w.encounter_context_variation(encounter,'shelter')
  self.assertIn('shelter’s failing anchors',note)
  self.assertIn('not a diagnosis or treatment',note)
  self.assertEqual(note,w.encounter_context_variation(encounter,'shelter'))
  self.assertEqual('',w.encounter_context_variation({},'shelter'))
 def test_pvp_consent_range_and_turn_limit(self):
  guest=self.call('join',name='Guest',role='Light Reader');self.call('start')
  with self.assertRaises(ValueError):self.call('duel_action',target=guest['id'],style='close')
  self.call('challenge',target=guest['id'])
  with self.assertRaises(ValueError):self.call('accept',target=guest['id'])
  self.call('accept',guest,target=self.host['id'])
  with patch('world.secrets.randbelow',return_value=19):self.call('duel_action',target=guest['id'],style='close')
  with self.assertRaises(ValueError):self.call('duel_action',target=guest['id'],style='close')
  r=s.fetch(self.host['code']);r['positions'][guest['id']]=4;r['pvp_actions']={};s.save(r)
  with self.assertRaises(ValueError):self.call('duel_action',target=guest['id'],style='ranged')
  self.call('disengage',guest,target=self.host['id']);self.assertFalse(self.call('state')['duels'])
 def test_distance_speech_move_and_leave(self):
  guest=self.call('join',name='Guest',role='Light Reader');self.call('start');self.call('move',step=1)
  with self.assertRaises(ValueError):self.call('move',step=1)
  self.call('speak',target=guest['id'],message='Stay near the guide line.')
  r=s.fetch(self.host['code']);r['positions'][guest['id']]=4;r['pvp_actions']={};s.save(r)
  with self.assertRaises(ValueError):self.call('speak',target=guest['id'],message='Too far')
  self.call('challenge',target=guest['id']);self.call('leave',guest);self.assertFalse(self.call('state')['duels'])
 def test_procedural_round_trip_and_persistence(self):
  r=s.fetch(self.host['code']);r['procedural']=True;s.save(r);self.call('start')
  with patch('world.secrets.randbelow',return_value=0):self.call('vote',choice=0)
  r=self.call('state');self.assertIsNotNone(r['encounter']);original=r['node']
  self.call('vote',choice=3);r=self.call('state');self.assertEqual(r['node'],original);self.assertIsNone(r['encounter'])
  self.assertIn('reputation',r);self.assertIn('character',r['players'][0]);self.assertEqual(r['turn'],2)
if __name__=='__main__':unittest.main()
