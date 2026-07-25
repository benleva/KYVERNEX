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
| M7-W002 | File-based JSON input and output for practical host use | P0 | CODE_COMPLETE_UNVERIFIED |
| M7-W003 | Persistent local plugin session wrapper | P0 | CODE_COMPLETE_UNVERIFIED |
| M7-W004 | Explicit real host-callable loading and minimal example | P0 | CODE_COMPLETE_UNVERIFIED |
| M7-W005 | Package version move to the `1.2.0` development line | P1 | IN_PROGRESS |

## Product code evidence

- `src/kyvernex/plugin.py`: compact host-facing plugin facade;
- `src/kyvernex/plugin_cli.py`: installed CLI with inline or file JSON input, optional file output and explicit handler selection;
- `src/kyvernex/plugin_loader.py`: exact `module:attribute` callable loader without discovery;
- `src/kyvernex/plugin_session.py`: persistent local multi-call session;
- `examples/plugin_handler.py`: real minimal application handler;
- `pyproject.toml`: installed `kyvernex-plugin` command.

## Product behavior now available

```text
kyvernex-plugin --handler examples.plugin_handler:handle --input-file request.json --output-file response.json --principal andrea
```

Python hosts may use either `KyvernexPlugin` for one owned plugin instance or `KyvernexPluginSession` for repeated calls.

## Product rule
M7 work must create callable, installable product behavior. Governance changes record the implementation but do not replace it. Testing is not the active workstream and no green claim is made for M7 code.
