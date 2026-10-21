import tempfile,sqlite3,unittest
from pathlib import Path
import launcher
class LauncherTests(unittest.TestCase):
 def test_migrate_does_not_overwrite(self):
  with tempfile.TemporaryDirectory() as temp:
   src=Path(temp)/'old.db';dst=Path(temp)/'new.db'
   with sqlite3.connect(src) as conn:conn.execute('create table example(value)');conn.execute('insert into example values (42)')
   self.assertTrue(launcher.migrate(dst,src));self.assertFalse(launcher.migrate(dst,src))
   with sqlite3.connect(dst) as conn:self.assertEqual(conn.execute('select value from example').fetchone()[0],42)
