# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`
- Active milestone: `M10 — Local Desktop Launcher`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7, M8 and M9 work items: `CODE_COMPLETE_UNVERIFIED`.

## M10 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M10-W001 | Installed `kyvernex-ai-app` one-command launcher | P0 | CODE_COMPLETE_UNVERIFIED |
| M10-W002 | Optional local launch profile file | P1 | BACKLOG |

## M10 code evidence
- `src/kyvernex/local_ai_app_cli.py`: starts the existing loopback server and opens the console;
- `pyproject.toml`: installs `kyvernex-ai-app`;
- browser opening can be disabled with `--no-browser`;
- shutdown remains tied to the same local server and bridge lifecycle.

## Product behavior

```text
kyvernex-ai-app --handler examples.plugin_handler:handle --principal andrea
```

## Boundary
M10 launches only the existing local product. It must not add public binding, remote hosting, authentication systems, databases, accounts, background services or release publication. Testing is not the active user-directed workstream and no green claim is made.
