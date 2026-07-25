# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`, `M11`
- Active milestone: `M12 — Portable Local Launchers`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M11 work items: `CODE_COMPLETE_UNVERIFIED`.

## M12 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M12-W001 | Installed cross-platform portable launcher generator | P0 | CODE_COMPLETE_UNVERIFIED |
| M12-W002 | Optional launcher generation from `kyvernex-ai-setup` | P1 | IN_PROGRESS |

## M12 code evidence
- `src/kyvernex/local_ai_shortcut_cli.py`: validates one profile and emits Windows, macOS and Linux launch files;
- `pyproject.toml`: installs `kyvernex-ai-shortcut`;
- POSIX outputs are marked executable;
- generated commands contain only the existing `kyvernex-ai-app --profile` invocation;
- existing output files require `--force` before replacement.

## Product behavior

```text
kyvernex-ai-shortcut --profile kyvernex.local.json
```

```text
kyvernex-ai-shortcut --profile kyvernex.local.json --platform linux --output-dir launchers
```

## Boundary
M12 produces portable files and performs no operating-system registration. Installers, desktop-menu integration, automatic startup, services, public binding, accounts, databases and release publication remain outside the milestone. Testing is not the active user-directed workstream and no green claim is made.
