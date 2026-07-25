# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`, `M11`, `M12`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M11 work items: `CODE_COMPLETE_UNVERIFIED`.

## M12 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M12-W001 | Installed cross-platform portable launcher generator | P0 | CODE_COMPLETE_UNVERIFIED |
| M12-W002 | Optional launcher generation from `kyvernex-ai-setup` | P1 | CODE_COMPLETE_UNVERIFIED |

## M12 code evidence
- `src/kyvernex/local_ai_shortcut_cli.py`: validates one profile and emits Windows, macOS and Linux launch files;
- `src/kyvernex/local_ai_setup_cli.py`: optionally generates launchers during explicit profile setup;
- `pyproject.toml`: installs `kyvernex-ai-shortcut`;
- POSIX outputs are marked executable;
- generated commands contain only the existing `kyvernex-ai-app --profile` invocation;
- setup supports `--launchers`, `--launcher-platform` and `--launcher-dir`;
- existing output files require `--force` before replacement.

## Product behavior

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea --launchers
```

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea --launchers --launcher-platform linux --launcher-dir launchers --launch
```

## Boundary
M12 has no active coding item. It is code-complete but unverified. It produces portable text files and performs no operating-system registration. Installers, desktop-menu integration, automatic startup, services, public binding, accounts, databases and release publication remain outside the milestone. No green, clean-install or runtime compatibility claim is made.
