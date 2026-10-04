import argparse,json,sqlite3,time,math
from pathlib import Path
from contextlib import closing
def schema(db):
    return {f'{kind}:{name}':sql for kind,name,sql in db.execute("SELECT type,name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name")}
def rehearse(source,migration,timeout=5):
    source=Path(source).resolve()
    if not source.is_file():raise ValueError('source database must already exist')
    if not math.isfinite(timeout) or timeout<=0 or timeout>60:raise ValueError('timeout must be in (0,60] seconds')
    memory=sqlite3.connect(':memory:');before={}
    try:
        uri=source.as_uri()+'?mode=ro'
        with closing(sqlite3.connect(uri,uri=True,timeout=1)) as original:original.backup(memory)
        before=schema(memory);memory.execute('PRAGMA foreign_keys=ON');deadline=time.monotonic()+timeout
        def authorize(action,a,b,c,d):
            if action in (sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH,sqlite3.SQLITE_PRAGMA):return sqlite3.SQLITE_DENY
            if action==sqlite3.SQLITE_FUNCTION and str(b).lower()=='load_extension':return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        memory.set_authorizer(authorize);memory.set_progress_handler(lambda:int(time.monotonic()>deadline),1000)
        memory.executescript(migration)
        # Python 3.10 cannot disable the authorizer with None. User SQL is done;
        # permit only this function's own schema/integrity validation phase.
        memory.set_authorizer(lambda *_args: sqlite3.SQLITE_OK);memory.set_progress_handler(None,0)
        foreign_keys=[list(x) for x in memory.execute('PRAGMA foreign_key_check')]
        integrity=[x[0] for x in memory.execute('PRAGMA integrity_check')]
        after=schema(memory)
        return {'added':{k:after[k] for k in sorted(after.keys()-before.keys())},'removed':{k:before[k] for k in sorted(before.keys()-after.keys())},'changed':{k:{'before':before[k],'after':after[k]} for k in sorted(before.keys()&after.keys()) if before[k]!=after[k]},'foreign_key_violations':foreign_keys,'integrity':integrity,'source_modified':False}
    finally:memory.close()
def main():
    p=argparse.ArgumentParser();p.add_argument('database');p.add_argument('migration');p.add_argument('--timeout',type=float,default=5);a=p.parse_args()
    try:r=rehearse(a.database,Path(a.migration).read_text(),a.timeout)
    except (ValueError,OSError,sqlite3.Error) as e:p.exit(2,str(e)+'\n')
    print(json.dumps(r,indent=2));return int(bool(r['foreign_key_violations'] or r['integrity']!=['ok']))
if __name__=='__main__':raise SystemExit(main())
