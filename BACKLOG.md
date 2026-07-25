# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`, `M11`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M10 work items: `CODE_COMPLETE_UNVERIFIED`.

## M11 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M11-W001 | Installed `kyvernex-ai-setup` profile bootstrap command | P0 | CODE_COMPLETE_UNVERIFIED |
| M11-W002 | Optional immediate launch after profile creation | P1 | CODE_COMPLETE_UNVERIFIED |

## M11 code evidence
- `src/kyvernex/local_ai_setup_cli.py`: creates, validates and optionally launches one explicit local profile;
- `src/kyvernex/local_ai_profile.py`: existing strict validation reused by setup;
- `src/kyvernex/local_ai_app_cli.py`: existing loopback launcher reused by `--launch`;
- `pyproject.toml`: installs `kyvernex-ai-setup`;
- existing files require `--force` before replacement;
- no profile discovery or environment fallback is introduced.

## Product behavior

Create profile:

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea
```

Create and launch:

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea --launch
```

## Boundary
M11 has no active coding item. It is code-complete but unverified. Setup may invoke only the existing local launcher through the generated explicit profile. Network access, installers, operating-system services, automatic startup, public binding, accounts, databases and release publication remain outside the milestone. No green, clean-install or runtime verification claim is made.
