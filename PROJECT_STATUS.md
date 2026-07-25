# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Active milestone: **M7 — Plugin Product Interface**
- Active sprint: **S010 — Usable plugin API**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-021`
- KGO cycle: `KGO-CYCLE-032`
- Target version: `1.2.0`

## Direction
M6 test-only work remains paused by user instruction. No unfinished M6 task is reported as complete.

M7 delivers executable product behavior rather than additional governance layers.

## M7 product path

```text
host code or JSON file
-> kyvernex-plugin / KyvernexPluginSession
-> KyvernexPlugin
-> governed runtime
-> bounded adapter
-> structured response or JSON file
```

## Product code delivered

### M7-W001 — Public product interface
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/plugin.py` provides `KyvernexPlugin`;
- `src/kyvernex/plugin_cli.py` provides the installed `kyvernex-plugin` command;
- `pyproject.toml` registers the command;
- `src/kyvernex/__init__.py` exports `KyvernexPlugin`.

### M7-W002 — Practical JSON file input and output
Status: `CODE_COMPLETE_UNVERIFIED`

The command supports mutually exclusive `--input` and `--input-file` sources plus optional `--output-file` response persistence.

### M7-W003 — Persistent local plugin session
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/plugin_session.py` keeps one initialized plugin alive across repeated calls;
- the session fixes a principal and capability set;
- each call receives a monotonically increasing session sequence;
- shutdown is terminal and reusable through a context manager.

### M7-W004 — Real host callable loading and example
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/plugin_loader.py` loads one explicit `module:attribute` callable;
- no discovery, scanning, environment expansion or fallback loading is performed;
- `examples/plugin_handler.py` is a real minimal host handler;
- the installed command accepts `--handler MODULE:ATTRIBUTE`.

## Current command examples

Inline JSON with built-in local handler:

```text
kyvernex-plugin --input '{"message":"ciao"}' --principal andrea
```

Real application handler:

```text
kyvernex-plugin --handler examples.plugin_handler:handle --input '{"message":"ciao"}' --principal andrea
```

File workflow:

```text
kyvernex-plugin --handler examples.plugin_handler:handle --input-file request.json --output-file response.json --principal andrea
```

## Active work
- M7-W005 package transition to the `1.2.0` development line: `IN_PROGRESS`

## Continuation rule
Continue with executable packaging and product code. Do not return to test-only work unless explicitly requested. Do not claim verification, clean installation or release evidence that has not been observed.
