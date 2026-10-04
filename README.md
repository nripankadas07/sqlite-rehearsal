# sqlite-rehearsal

Rehearse SQLite migrations in memory and report schema changes without modifying the source.

An offline Python 3.10+ MVP with no runtime dependencies.

## Install and first useful result

```sh
git clone https://github.com/nripankadas07/sqlite-rehearsal.git
cd sqlite-rehearsal
python -m venv .venv
# POSIX; on Windows use .venv\Scripts\activate
. .venv/bin/activate
python -m pip install .
sqlite-rehearsal --help
python demo.py
```

The demo creates temporary synthetic inputs and prints the actual report; it does not require accounts, services, API keys or user data. CLI exit status: 0 = accepted/clean; 1 = review findings; 2 = invalid input or operational error. For SQLite, schema changes are informational and status 1 means validation violations.

## CLI example

```sh
sqlite-rehearsal source.db migration.sql --timeout 5
```

The migration is a UTF-8 SQL file you trust. Rehearsal copies the database to memory and leaves its original data unchanged.

## Validate

```sh
python -m unittest discover -v
python -m compileall -q sqlite_rehearsal.py
python demo.py
```

## Limits

Local trusted SQLite inputs only. Not a security sandbox for arbitrary hostile SQL; memory allocation and backup duration are not fully bounded. Source backup may observe WAL state and source is opened read-only; no deployment or rollback execution. PRAGMA statements and ATTACH are deliberately unsupported in migrations. Virtual-table extensions are not supported.

See [RESEARCH.md](RESEARCH.md) for the user brief and dated comparisons, [VALIDATION.md](VALIDATION.md) for exact check coverage, and [SUPPORT.md](SUPPORT.md) for contributions and security reporting. MIT licensed; original implementation, with standard-library dependencies. No competitor code or prose copied.
