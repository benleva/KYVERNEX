# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Active milestone: `M7 — Plugin Product Interface`
- Active sprint: `S010 — Usable plugin API`
- Target version: `1.2.0`

## M6 paused state
Completed M6 work remains preserved:
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`.

No unfinished M6 item is reported as complete.

## M7 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M7-W001 | Public `KyvernexPlugin` facade and installed `kyvernex-plugin` command | P0 | CODE_COMPLETE_UNVERIFIED |
| M7-W002 | File-based JSON input and output for practical host use | P0 | BACKLOG |
| M7-W003 | Persistent local plugin session wrapper | P0 | BACKLOG |
| M7-W004 | Minimal developer example using a real host callable | P0 | BACKLOG |
| M7-W005 | Package version move to the `1.2.0` development line | P1 | BACKLOG |

## M7-W001 code
- `src/kyvernex/plugin.py` owns runtime and adapter lifecycle;
- `KyvernexPlugin.execute()` builds the governed request envelope;
- `KyvernexPlugin.status()` exposes the runtime state;
- `KyvernexPlugin.shutdown()` closes the product cleanly;
- `src/kyvernex/plugin_cli.py` exposes one installed command;
- `pyproject.toml` registers `kyvernex-plugin`;
- `src/kyvernex/__init__.py` exports `KyvernexPlugin`.

## Product rule
M7 work must create callable, installable product behavior. Documentation and governance changes may record the work but must not replace code delivery.

Testing is not the active workstream and no green claim is made for M7-W001.