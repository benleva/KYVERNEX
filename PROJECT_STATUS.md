# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Product-code milestone: **M7 — Plugin Product Interface**
- Sprint: **S010 — Usable plugin API**
- Governance mode: **KPM/KGO PRODUCT BOUNDARY**
- KPM cycle: `KPM-CYCLE-022`
- KGO cycle: `KGO-CYCLE-033`
- Development package version: `1.2.0.dev0`

## Direction
M6 test-only work remains paused by user instruction. No unfinished M6 task is reported as complete.

M7 delivered executable plugin product code. No test, clean-install, publication or stable-release claim is made for the M7 code line.

## M7 product path

```text
host code or JSON file
-> kyvernex-plugin / KyvernexPluginSession
-> KyvernexPlugin
-> governed runtime
-> bounded adapter
-> structured response or JSON file
```

## M7 code delivered

### M7-W001 — Public product interface
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/plugin.py` provides `KyvernexPlugin`;
- `src/kyvernex/plugin_cli.py` provides the installed `kyvernex-plugin` command;
- `pyproject.toml` registers the command;
- `src/kyvernex/__init__.py` exports `KyvernexPlugin`.

### M7-W002 — Practical JSON file input and output
Status: `CODE_COMPLETE_UNVERIFIED`

The command supports mutually exclusive inline and file JSON input plus optional JSON response-file output.

### M7-W003 — Persistent local plugin session
Status: `CODE_COMPLETE_UNVERIFIED`

`src/kyvernex/plugin_session.py` keeps one initialized plugin alive across repeated governed calls.

### M7-W004 — Real host callable loading and example
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/plugin_loader.py` loads one explicit `module:attribute` callable;
- `examples/plugin_handler.py` provides a minimal real host handler;
- no discovery, scanning, environment expansion or fallback loading is performed.

### M7-W005 — Development version line
Status: `CODE_COMPLETE_UNVERIFIED`

- package metadata: `1.2.0.dev0`;
- public API `__version__`: `1.2.0.dev0`;
- `KyvernexPlugin` runtime metadata default: `1.2.0.dev0`.

## Current product use

```text
kyvernex-plugin --handler examples.plugin_handler:handle --input-file request.json --output-file response.json --principal andrea
```

## Product boundary
M7 is code-complete but unverified. KPM/KGO stop here because the next milestone needs a concrete host target or product objective. No additional platform, transport, adapter or service is inferred automatically.