# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**
- Active milestone: **M10 — Local Desktop Launcher**
- Active sprint: **S013 — One-command local app**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-029`
- KGO cycle: `KGO-CYCLE-040`
- Development package version: `1.2.0.dev0`

## Product objective
Start the existing loopback server and open its console with one installed command.

```text
kyvernex-ai-app
-> explicit host callable
-> KyvernexLocalAIServer on 127.0.0.1
-> system browser
-> local KYVERNEX console
```

## Preserved product code
M7, M8 and M9 remain `CODE_COMPLETE_UNVERIFIED`. M10 reuses the same plugin, AI bridge, local server and browser console. No second backend or runtime is introduced.

## M10 delivered code
### M10-W001 — One-command desktop launcher
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_app_cli.py` provides the launcher;
- `pyproject.toml` installs `kyvernex-ai-app`;
- `--handler module:attribute` selects one explicit callable;
- `--principal` fixes the governed principal;
- `--port` selects the loopback port;
- the default behavior opens the local console in the system browser;
- `--no-browser` starts the same local app without opening a browser;
- `Ctrl+C` shuts down server and bridge.

## Current use

```text
kyvernex-ai-app --handler examples.plugin_handler:handle --principal andrea
```

Headless local start:

```text
kyvernex-ai-app --handler examples.plugin_handler:handle --principal andrea --no-browser
```

## Boundary
M10 only launches the already delivered loopback product. It does not add public binding, remote hosting, authentication, databases, accounts, installers, operating-system services or release publication. No verification claim is made.
