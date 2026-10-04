# User brief and comparison

**User:** Engineer deploying a SQLite-backed application schema change.

**Pain:** Reviewing SQL alone misses constraint failures and exact resulting schema changes; rehearsing against the real file risks writes.

**Need:** Inferred need; not verified requests or proof that general migration runners lack rehearsal features.

**Capability:** Copy a read-only SQLite source into memory, apply migration with external database attachment/PRAGMA blocked, check foreign keys/integrity and report schema delta.

**Acceptance:** ALTER/index delta, byte-identical source on success and failure, attachment/PRAGMA rejection and constraint failure.

**Discovery:** SQLite release and migration review workflows.

**Portfolio:** No existing database migration rehearsal product. This is separate from file sync or environment drift tools.


## Search coverage

GitHub query `sqlite migration in:description`, sorted by stars descending; observation 2026-10-04T12:43:43.177288+00:00. The top ten search results were screened for relevance. Search is not an exhaustive global ranking. Established comparables outside that query were also inspected; highest-star relevant comparable found among this researched set is identified below. Stars are research context, not technical performance.

Highest-star relevant comparable found: [golang-migrate/migrate](https://github.com/golang-migrate/migrate), 18953 stars.

| Comparable | Stars | Last push UTC | License | Workflow and tradeoff |
| --- | ---: | --- | --- | --- |
| [golang-migrate/migrate](https://github.com/golang-migrate/migrate) | 18953 | 2026-09-09T05:06:21Z | NOASSERTION | Established CLI/Go migration execution across multiple databases and migration sources. |
| [pressly/goose](https://github.com/pressly/goose) | 11530 | 2026-10-03T00:22:52Z | NOASSERTION | SQL/Go incremental migrations, several database drivers, and a documented Go install path. |
| [amacneil/dbmate](https://github.com/amacneil/dbmate) | 7433 | 2026-09-30T04:43:25Z | MIT | Standalone cross-framework migration runner with SQLite support; prefer it for actual migration execution and operational history. |

README installation and example workflows and available recent issues were inspected. Push time does not prove active support, and mature alternatives cover broader domains. No competitor installations or equivalent performance workloads were measured. Time to first result and runtime performance comparisons are unmeasured. Tests prove only this implementation. Demand is inferred unless an issue is linked explicitly; no users, adoption or results are fabricated.
