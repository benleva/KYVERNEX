# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`, `M11`, `M12`, `M13`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M12 work items: `CODE_COMPLETE_UNVERIFIED`.

## M13 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M13-W001 | Installed editable local project scaffold generator | P0 | CODE_COMPLETE_UNVERIFIED |
| M13-W002 | Optional immediate launch after scaffold creation | P1 | CODE_COMPLETE_UNVERIFIED |

## M13 code evidence
- `src/kyvernex/local_ai_project_cli.py`: creates an editable handler, strict profile, README and portable start files;
- `pyproject.toml`: installs `kyvernex-ai-project`;
- generated start files change into the project directory before invoking the existing app;
- generated profile uses the explicit local handler reference `handler:handle`;
- `--launch` invokes the existing local app from the generated project directory;
- the previous working directory is restored when the app exits;
- existing project files require `--force` before replacement;
- the generated profile is validated before success is reported.

## Product behavior

```text
kyvernex-ai-project my-kyvernex-project --principal andrea
```

```text
kyvernex-ai-project my-kyvernex-project --principal andrea --launch
```

## Boundary
M13 has no active coding item. It is code-complete but unverified. It produces editable local text and source files and may invoke only the existing loopback app. Package installation, operating-system registration, services, automatic startup, public binding, external network access and release publication remain outside the milestone. No green, clean-install or runtime compatibility claim is made.
