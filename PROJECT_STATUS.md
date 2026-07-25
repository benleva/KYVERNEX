# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**, **M11**, **M12**, **M13**
- Sprint: **S016 — Editable local project generation**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-036`
- KGO cycle: `KGO-CYCLE-047`
- Development package version: `1.2.0.dev0`

## Product objective delivered
Create one editable local project directory containing a host handler, strict profile, portable launch files and a short local README, with optional immediate launch.

```text
kyvernex-ai-project DIRECTORY --launch
-> editable handler.py
-> kyvernex.local.json
-> Windows, macOS and Linux launch files
-> existing kyvernex-ai-app
-> loopback KYVERNEX console
```

## Preserved product code
M7 through M12 remain `CODE_COMPLETE_UNVERIFIED`. M13 reuses the existing strict profile and desktop app contracts. It creates ordinary source and text files only.

## M13 code delivered
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

### M13-W002 — Immediate scaffold launch
Status: `CODE_COMPLETE_UNVERIFIED`

- `--launch` starts the generated project only after successful file creation and profile validation;
- the process changes into the generated project directory before invoking the existing app path;
- `handler:handle` is therefore resolved from the project itself;
- the launcher receives the explicit local profile `kyvernex.local.json`;
- the previous working directory is restored after the local app exits;
- the app exit code is returned unchanged.

## Current use

Create only:

```text
kyvernex-ai-project my-kyvernex-project --principal andrea
```

Create and launch:

```text
kyvernex-ai-project my-kyvernex-project --principal andrea --launch
```

## Boundary
M13 is code-complete but unverified. It creates only an editable local folder and may invoke only the existing loopback application. It does not install dependencies, register operating-system components, create services, expose a public address, access external networks or publish a release. No runtime compatibility, CI or verification claim is made.
