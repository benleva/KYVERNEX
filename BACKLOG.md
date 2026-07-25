# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`
- Active milestone: `M11 — Local Setup Bootstrap`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M10 work items: `CODE_COMPLETE_UNVERIFIED`.

## M11 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M11-W001 | Installed `kyvernex-ai-setup` profile bootstrap command | P0 | CODE_COMPLETE_UNVERIFIED |
| M11-W002 | Optional immediate launch after profile creation | P1 | BACKLOG |

## M11 code evidence
- `src/kyvernex/local_ai_setup_cli.py`: creates and validates one explicit local profile;
- `src/kyvernex/local_ai_profile.py`: existing strict validation reused by setup;
- `pyproject.toml`: installs `kyvernex-ai-setup`;
- existing files require `--force` before replacement;
- no profile discovery or environment fallback is introduced.

## Product behavior

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea
kyvernex-ai-app --profile kyvernex.local.json
```

## Boundary
M11 may simplify explicit local initialization only. It must not add network access, installers, operating-system services, automatic startup, public binding, accounts, databases or release publication. Testing is not the active user-directed workstream and no green claim is made.
