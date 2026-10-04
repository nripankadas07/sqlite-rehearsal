import tempfile,sqlite3,json
from pathlib import Path
from sqlite_rehearsal import rehearse
with tempfile.TemporaryDirectory() as d:
 p=Path(d,'demo.db')
 with sqlite3.connect(p) as db:db.execute('CREATE TABLE orders(id INTEGER PRIMARY KEY)')
 print(json.dumps(rehearse(p,'ALTER TABLE orders ADD COLUMN status TEXT;'),indent=2))
