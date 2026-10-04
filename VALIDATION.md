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
