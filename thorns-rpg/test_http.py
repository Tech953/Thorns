"""Start a temporary local server; exercise the actual HTTP boundary."""
import json, tempfile, threading, unittest
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from pathlib import Path
import server as s
class HTTPTests(unittest.TestCase):
 def test_multiplayer_custom_build_and_validation(self):
  with tempfile.TemporaryDirectory() as tmp:
   s.init_db(str(Path(tmp)/'rooms.db'))
   http=s.ThreadingHTTPServer(('127.0.0.1',0),s.Handler)
   thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
   url='http://127.0.0.1:'+str(http.server_port)
   def call(data):
    with urlopen(Request(url+'/api',data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})) as r:return json.load(r)
   try:
    with urlopen(url+'/character-catalog') as r:catalog=json.load(r)
    c=catalog['presets']['Needlurgist'];c.pop('legacy');c['attributes']={'body':2,'tech':2,'percept':2,'rapport':2}
    h=call(dict(op='create',ruleset='legacy',name='Custom',role='Needlurgist',character=c,procedural=False))
    ps=[h]+[call(dict(op='join',code=h['code'],name='Guest '+str(i),role='Light Reader')) for i in range(5)]
    r=call(dict(**h,op='state'));self.assertEqual(r['players'][0]['sheet']['attributes']['tech'],2)
    self.assertEqual(len(r['reputation']),25)
    call(dict(**h,op='start',revision=r['revision']))
    for p in ps:
     r=call(dict(**p,op='state'));r=call(dict(**p,op='vote',revision=r['revision'],choice=0))
    self.assertEqual(r['turn'],1);self.assertEqual(r['node'],'web');self.assertIn('success_percent',r['scene']['choices'][0]['check'])
    with self.assertRaises(HTTPError):call(dict(**h,op='character',revision=r['revision'],character=c))
    h2=call(dict(op='create',ruleset='legacy',name='Explorer',role='NanoClad Scout',mode='open',hardcore=True,procedural=False))
    explorers=[h2]+[call(dict(op='join',code=h2['code'],name='Explorer '+str(i),role='Light Reader')) for i in range(5)]
    r=call(dict(**h2,op='state'));r=call(dict(**h2,op='start',revision=r['revision']))
    for explorer in explorers:
     r=call(dict(**explorer,op='state'));r=call(dict(**explorer,op='ow_move',revision=r['revision'],dx=1,dy=0))
    self.assertTrue(all(p['grid']==[1,0] and p['vitals']['thirst']==5 for p in r['players']))
    self.assertTrue(all(len(p['overland']['tiles'])==25 for p in r['players']))
    for path in ['/','/app.js','/creator.js','/openworld.js','/style.css','/world-map.jpg','/needle-map.jpg']:
     with urlopen(url+path) as response:self.assertEqual(response.status,200);response.read()
   finally:http.shutdown();http.server_close();thread.join();s.DB.close()
if __name__=='__main__':unittest.main()
