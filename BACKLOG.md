# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Product-code milestone: `M7 — Plugin Product Interface`
- Development package version: `1.2.0.dev0`

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
| M7-W005 | Package, API and facade version move to `1.2.0.dev0` | P1 | CODE_COMPLETE_UNVERIFIED |

## Product code evidence

- `src/kyvernex/plugin.py`: compact host-facing plugin facade;
- `src/kyvernex/plugin_cli.py`: installed CLI with inline or file JSON input, optional file output and explicit handler selection;
- `src/kyvernex/plugin_loader.py`: exact `module:attribute` callable loader without discovery;
- `src/kyvernex/plugin_session.py`: persistent local multi-call session;
- `examples/plugin_handler.py`: real minimal application handler;
- `pyproject.toml`: installed `kyvernex-plugin` command and package version `1.2.0.dev0`;
- `src/kyvernex/__init__.py`: public API version `1.2.0.dev0`.

## Product behavior now available

```text
kyvernex-plugin --handler examples.plugin_handler:handle --input-file request.json --output-file response.json --principal andrea
```

Python hosts may use either `KyvernexPlugin` for one owned plugin instance or `KyvernexPluginSession` for repeated calls.

## Boundary
M7 contains no active coding item. It is code-complete but unverified. A new milestone must name a concrete host, platform or product outcome before additional code is authorized. Testing remains outside the current user-directed workstream.