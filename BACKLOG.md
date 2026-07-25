# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`, `M11`, `M12`
- Active milestone: `M13 — Local Project Scaffold`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M12 work items: `CODE_COMPLETE_UNVERIFIED`.

## M13 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M13-W001 | Installed editable local project scaffold generator | P0 | CODE_COMPLETE_UNVERIFIED |
| M13-W002 | Optional immediate launch after scaffold creation | P1 | IN_PROGRESS |

## M13 code evidence
- `src/kyvernex/local_ai_project_cli.py`: creates an editable handler, strict profile, README and portable start files;
- `pyproject.toml`: installs `kyvernex-ai-project`;
- generated start files change into the project directory before invoking the existing app;
- generated profile uses the explicit local handler reference `handler:handle`;
- existing project files require `--force` before replacement;
- the generated profile is validated before success is reported.

## Product behavior

```text
kyvernex-ai-project my-kyvernex-project --principal andrea
```

The generated folder contains `handler.py`, `kyvernex.local.json`, three portable launch files and `README.md`.

## Boundary
M13 produces editable local text and source files only. Package installation, operating-system registration, services, automatic startup, public binding, network access and release publication remain outside the milestone. Testing is not the active user-directed workstream and no green claim is made.
