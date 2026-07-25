# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**, **M11**, **M12**
- Active milestone: **M13 — Local Project Scaffold**
- Active sprint: **S016 — Editable local project generation**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-035`
- KGO cycle: `KGO-CYCLE-046`
- Development package version: `1.2.0.dev0`

## Product objective
Create one editable local project directory containing a host handler, strict profile, portable launch files and a short local README.

```text
kyvernex-ai-project
-> editable handler.py
-> kyvernex.local.json
-> Windows, macOS and Linux launch files
-> existing kyvernex-ai-app
-> loopback KYVERNEX console
```

## Preserved product code
M7 through M12 remain `CODE_COMPLETE_UNVERIFIED`. M13 reuses the existing strict profile and desktop app contracts. It creates ordinary source and text files only.

## M13 delivered code
### M13-W001 — Editable local project generator
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_project_cli.py` provides `kyvernex-ai-project`;
- `pyproject.toml` installs the command;
- the default output directory is `kyvernex-local-project`;
- generated `handler.py` exposes `handle(request, authority)` and is intended for direct editing;
- generated profile references the local handler explicitly as `handler:handle`;
- generated launch files change into the project directory before invoking `kyvernex-ai-app`;
- Windows, macOS and Linux start files are included;
- POSIX files receive executable permission bits;
- existing scaffold files require `--force` before replacement;
- the generated profile is validated before success is reported.

## Current use

```text
kyvernex-ai-project my-kyvernex-project --principal andrea
```

Generated files:

```text
my-kyvernex-project/handler.py
my-kyvernex-project/kyvernex.local.json
my-kyvernex-project/start-kyvernex.cmd
my-kyvernex-project/start-kyvernex.command
my-kyvernex-project/start-kyvernex.sh
my-kyvernex-project/README.md
```

## Active work
- M13-W002 optional immediate launch of the generated project through the existing app path: `IN_PROGRESS`.

## Boundary
M13 creates only an editable local folder. It does not install dependencies, register operating-system components, create services, expose a public address, access the network or publish a release. No runtime compatibility or verification claim is made.
