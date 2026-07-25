# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**, **M11**
- Sprint: **S014 — Explicit local initialization**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-032`
- KGO cycle: `KGO-CYCLE-043`
- Development package version: `1.2.0.dev0`

## Product objective delivered
Create one validated local launch profile with a single installed command and optionally start the existing local application immediately.

```text
kyvernex-ai-setup --launch
-> strict JSON profile
-> kyvernex-ai-app --profile ...
-> loopback server
-> local browser console
```

## Preserved product code
M7 through M10 remain `CODE_COMPLETE_UNVERIFIED`. M11 reuses the same strict profile loader and desktop launcher. No second runtime, server, backend or configuration source is introduced.

## M11 code delivered
### M11-W001 — Explicit setup bootstrap command
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_setup_cli.py` provides `kyvernex-ai-setup`;
- `pyproject.toml` installs the command;
- the command writes one explicit UTF-8 JSON profile;
- the generated profile is validated by the existing strict profile loader;
- default output is `kyvernex.local.json`;
- an existing file is never replaced unless `--force` is supplied.

### M11-W002 — Immediate launch after setup
Status: `CODE_COMPLETE_UNVERIFIED`

- `--launch` starts the existing `kyvernex-ai-app` path after successful profile creation;
- the generated profile path is passed explicitly to the launcher;
- browser preference, handler, principal and port come from the validated profile;
- setup failure prevents launch;
- launcher exit status is returned unchanged.

## Current use

Create only:

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea
```

Create and launch:

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea --launch
```

## Boundary
M11 is code-complete but unverified. It creates one explicit local profile and may invoke only the already delivered loopback launcher. It performs no discovery, environment reads, network access, package installation, operating-system registration, background service creation or release publication. No verification claim is made.
