# Validation snapshot

2026-10-04T13:08:36.059808+00:00

Environment: Linux-6.18.44-x86_64-with-glibc2.39; Python 3.12.14. All listed checks passed.

- `python -m unittest discover -v`
- `python -m compileall -q sqlite_rehearsal.py`
- `python demo.py`
- `python -m pip wheel --no-deps --no-build-isolation --wheel-dir /tmp/wheels .`
- `python -m venv /tmp/clean-example/venv`
- `/tmp/clean-example/venv/bin/python -m pip install --no-index /tmp/wheels/sqlite_rehearsal-0.1.0-py3-none-any.whl`
- `/tmp/clean-example/venv/bin/sqlite-rehearsal --help`
- `/tmp/clean-example/venv/bin/python /tmp/clean-example/demo.py`

Fresh virtual environment installed the built wheel without index access; CLI and copied standalone demo ran outside the repository, using the installed module. Input failure cases are covered in tests. No runtime third-party dependencies; setuptools is the build backend. Remote CI covers Python 3.10, 3.12 and 3.14 on Linux after publication. Other operating systems are unverified. Benchmarks and production use are unmeasured.

## Python 3.10 compatibility repair

Initial public CI at a1656bba21d80f7f3275366c1d32d7c57d9423ea failed on Python 3.10.21: successful ALTER/CREATE execution was followed by `sqlite3.DatabaseError: not authorized` at the internal foreign-key check. Python 3.10 does not support clearing an authorizer with None; support was added in Python 3.11. The migration authorizer remains restrictive throughout user SQL. After user SQL finishes, an explicit allow callback permits only the function's own schema/integrity checks. Existing source-byte preservation and ATTACH/PRAGMA rejection tests are unchanged. Local Python 3.12 checks pass; repaired three-version remote CI must pass before LIVE status.

Failure receipt: https://github.com/nripankadas07/sqlite-rehearsal/actions/runs/37205711586
