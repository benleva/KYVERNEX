# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**
- Active milestone: **M11 — Local Setup Bootstrap**
- Active sprint: **S014 — Explicit local initialization**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-031`
- KGO cycle: `KGO-CYCLE-042`
- Development package version: `1.2.0.dev0`

## Product objective
Create one validated local launch profile with a single installed command, then use that profile with the existing desktop launcher.

```text
kyvernex-ai-setup
-> strict JSON profile
-> kyvernex-ai-app --profile ...
-> loopback server
-> local browser console
```

## Preserved product code
M7 through M10 remain `CODE_COMPLETE_UNVERIFIED`. M11 does not add another runtime, server, backend or configuration source.

## M11 delivered code
### M11-W001 — Explicit setup bootstrap command
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_setup_cli.py` provides `kyvernex-ai-setup`;
- `pyproject.toml` installs the command;
- the command writes one explicit UTF-8 JSON profile;
- the generated profile is validated by the existing strict profile loader;
- default output is `kyvernex.local.json`;
- an existing file is never replaced unless `--force` is supplied;
- supported values remain only handler, principal, port and browser preference.

## Current use

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea
kyvernex-ai-app --profile kyvernex.local.json
```

Alternative output:

```text
kyvernex-ai-setup --output config/kyvernex.json --handler examples.plugin_handler:handle --no-browser
```

## Boundary
M11 creates only a local profile file named explicitly by the user. It performs no discovery, environment reads, network access, package installation, operating-system registration, background service creation or release publication. No verification claim is made.
