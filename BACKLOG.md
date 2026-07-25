# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7, M8 and M9 work items: `CODE_COMPLETE_UNVERIFIED`.

## M10 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M10-W001 | Installed `kyvernex-ai-app` one-command launcher | P0 | CODE_COMPLETE_UNVERIFIED |
| M10-W002 | Strict optional local JSON launch profile | P1 | CODE_COMPLETE_UNVERIFIED |

## M10 code evidence
- `src/kyvernex/local_ai_app_cli.py`: starts the existing loopback server, opens the console and accepts `--profile`;
- `src/kyvernex/local_ai_profile.py`: strict profile loading with four supported fields;
- `examples/local_ai_profile.json`: minimal explicit profile;
- `pyproject.toml`: installed `kyvernex-ai-app` entry point;
- command-line arguments override profile values;
- browser opening remains selectable with `--browser` or `--no-browser`.

## Product behavior

```text
kyvernex-ai-app --profile examples/local_ai_profile.json
```

```text
kyvernex-ai-app --profile examples/local_ai_profile.json --port 9000 --no-browser
```

## Boundary
M10 has no active coding item. It is code-complete but unverified. Profiles are never discovered automatically and do not read environment variables. Public binding, remote hosting, authentication systems, databases, accounts, background services, installers and release publication remain outside the milestone. No green, clean-install or runtime verification claim is made.
