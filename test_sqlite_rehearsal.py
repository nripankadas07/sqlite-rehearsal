import tempfile,unittest,sqlite3,hashlib
from pathlib import Path
from sqlite_rehearsal import rehearse
class Tests(unittest.TestCase):
 def setup_db(self,d):
  p=Path(d,'source.db')
  with sqlite3.connect(p) as db:db.executescript('CREATE TABLE orders(id INTEGER PRIMARY KEY);INSERT INTO orders VALUES(1);')
  return p
 def test_schema_diff_source_unchanged(self):
  with tempfile.TemporaryDirectory() as d:
   p=self.setup_db(d);old=p.read_bytes();r=rehearse(p,'ALTER TABLE orders ADD COLUMN status TEXT;CREATE INDEX ix ON orders(status);');self.assertIn('table:orders',r['changed']);self.assertIn('index:ix',r['added']);self.assertEqual(p.read_bytes(),old);self.assertEqual(r['integrity'],['ok'])
 def test_failure_leaves_source_intact(self):
  with tempfile.TemporaryDirectory() as d:
   p=self.setup_db(d);old=p.read_bytes()
   with self.assertRaises(sqlite3.Error):rehearse(p,'DROP TABLE orders;INVALID SQL;')
   self.assertEqual(p.read_bytes(),old)
 def test_attach_and_pragma_denied(self):
  with tempfile.TemporaryDirectory() as d:
   p=self.setup_db(d)
   for sql in [f"ATTACH DATABASE '{d}/escape.db' AS other;",'PRAGMA writable_schema=ON;']:
    with self.assertRaises(sqlite3.Error):rehearse(p,sql)
   self.assertFalse(Path(d,'escape.db').exists())
 def test_constraint_failure(self):
  with tempfile.TemporaryDirectory() as d:
   p=self.setup_db(d)
   with self.assertRaises(sqlite3.IntegrityError):rehearse(p,'INSERT INTO orders VALUES(1);')
 def test_missing_database(self):
  with self.assertRaises(ValueError):rehearse('/definitely-missing-rehearsal.db','SELECT 1;')
