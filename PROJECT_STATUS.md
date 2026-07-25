# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**, **M11**
- Active milestone: **M12 — Portable Local Launchers**
- Active sprint: **S015 — Cross-platform local start files**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-033`
- KGO cycle: `KGO-CYCLE-044`
- Development package version: `1.2.0.dev0`

## Product objective
Generate readable launch files for Windows, macOS and Linux from one explicit validated local profile.

```text
kyvernex-ai-shortcut --profile kyvernex.local.json
-> start-kyvernex.cmd
-> start-kyvernex.command
-> start-kyvernex.sh
-> kyvernex-ai-app --profile ...
```

## Preserved product code
M7 through M11 remain `CODE_COMPLETE_UNVERIFIED`. M12 calls only the existing local application command and does not install or register anything in the operating system.

## M12 delivered code
### M12-W001 — Portable launcher generator
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_shortcut_cli.py` provides `kyvernex-ai-shortcut`;
- `pyproject.toml` installs the command;
- one explicit profile is resolved and validated before generation;
- `--platform all|windows|macos|linux` selects output files;
- Windows output is `start-kyvernex.cmd`;
- macOS output is `start-kyvernex.command`;
- Linux output is `start-kyvernex.sh`;
- POSIX launch files receive executable permission bits;
- existing files require `--force` before replacement;
- every generated file invokes only `kyvernex-ai-app --profile <absolute path>`.

## Current use

```text
kyvernex-ai-shortcut --profile kyvernex.local.json
```

Single platform:

```text
kyvernex-ai-shortcut --profile kyvernex.local.json --platform windows
```

## Active work
- M12-W002 optional launcher generation from `kyvernex-ai-setup`: `IN_PROGRESS`.

## Boundary
M12 creates portable text launch files only. It does not create installers, Start-menu entries, desktop registrations, login items, system services, automatic startup, network access or release publication. No verification claim is made.
