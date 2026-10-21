import copy
import unittest
from unittest.mock import patch
import overland
import server
import test_game


class ContactTests(unittest.TestCase):
    setUp=test_game.GameTests.setUp
    tearDown=test_game.GameTests.tearDown
    call=test_game.GameTests.call

    def open(self):
        self.host=server.mutate(dict(op='create',ruleset='legacy',name='Visitor',role='Light Reader',mode='open',procedural=False))
        self.call('start')

    def test_contact_and_dialogue_survive_reload_without_spending_stocks(self):
        self.open();initial=self.call('state');before=copy.deepcopy(initial['players'][0])
        with patch('overland.secrets.randbelow',return_value=19):first=self.call('ow_talk',topic='access')
        self.assertIn('administrator',first['players'][0]['overland']['last_dialogue'])
        self.assertIn('reputation',first['log'][-3])
        for key in ['supplies','credits','grid','vitals','xp']:
            self.assertEqual(before[key],first['players'][0][key])
        persisted=server.fetch(self.host['code']);self.assertEqual(len(persisted['contacts']),1)
        with patch('overland.secrets.randbelow',return_value=19):second=self.call('ow_talk',topic='access')
        self.assertNotEqual(first['players'][0]['overland']['last_dialogue'],second['players'][0]['overland']['last_dialogue'])
        self.assertEqual(first['players'][0]['overland']['contact']['name'],second['players'][0]['overland']['contact']['name'])

    def test_remote_projection_cannot_spawn_contact_or_grant_access(self):
        self.open();r=server.fetch(self.host['code']);r['players'][0]['grid']=[40,0];server.save(r)
        with self.assertRaises(ValueError):self.call('ow_talk',topic='place')
        self.assertEqual(server.fetch(self.host['code'])['contacts'],{})

    def test_site_limit_blocks_new_movement_and_preserves_current_position(self):
        self.open();r=server.fetch(self.host['code'])
        r['overland_sites']={str(i):{} for i in range(2048)};server.save(r)
        with self.assertRaises(ValueError):self.call('ow_move',dx=1,dy=0)
        self.assertEqual(server.fetch(self.host['code'])['players'][0]['grid'],[0,0])

    def test_practice_cap_includes_equipment_and_negative_standing(self):
        self.open();r=server.fetch(self.host['code']);p=r['players'][0]
        p['character']['skills']['community']=3;p['loadout']=['resonance_link'];r['reputation']['THORNS']=-6
        messages=[]
        with patch('overland.secrets.randbelow',return_value=19):overland.roll(r,p,'rapport','community',10,lambda r,t:messages.append(t),'THORNS')
        self.assertIn('practice 2',messages[0]);self.assertIn('reputation -1',messages[0])

if __name__=='__main__':unittest.main()
