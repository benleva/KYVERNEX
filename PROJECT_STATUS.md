# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestone: **M7 — Plugin Product Interface**
- Active milestone: **M8 — Universal AI Plugin Bridge**
- Active sprint: **S011 — Provider-neutral AI invocation**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-024`
- KGO cycle: `KGO-CYCLE-035`
- Development package version: `1.2.0.dev0`

## Product objective
Deliver one KYVERNEX plugin bridge that AI hosts can invoke through a provider-neutral JSON tool contract.

```text
AI host
-> kyvernex-ai-plugin / KyvernexAIBridge
-> KyvernexPlugin
-> governed runtime
-> bounded host callable
-> structured response
```

## M7 preserved code
M7 remains `CODE_COMPLETE_UNVERIFIED`. It provides the public facade, installed plugin command, explicit handler loading, JSON file workflows, persistent local sessions and the `1.2.0.dev0` development line.

## M8 delivered code
### M8-W001 — Provider-neutral AI bridge
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/ai_bridge.py` provides `KyvernexAIBridge`;
- the bridge exposes one tool named `kyvernex_execute`;
- `manifest()` returns a provider-neutral JSON Schema definition;
- `invoke()` accepts only `input`, optional `context` and optional `request_id`;
- unknown fields fail closed;
- execution remains inside the existing governed plugin path.

### M8-W002 — Installed AI bridge command
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/ai_plugin_cli.py` provides `kyvernex-ai-plugin`;
- `--handler module:attribute` selects one explicit host callable;
- `--manifest` prints the canonical tool definition;
- `pyproject.toml` installs the command;
- `src/kyvernex/__init__.py` exports `KyvernexAIBridge`.

### M8-W003 — Persistent multi-request process
Status: `CODE_COMPLETE_UNVERIFIED`

The installed command now supports:

```text
--stream
```

In stream mode:
- one `KyvernexAIBridge` instance remains alive;
- standard input is interpreted as JSON Lines;
- each non-empty line is one independent invocation;
- each response is emitted immediately as one JSON line;
- malformed requests return a line-specific `FAILED` response without terminating the process;
- the process exits after end-of-file and shuts down the bridge once.

## Current use
Single request:

```text
echo '{"input":{"message":"ciao"}}' | kyvernex-ai-plugin --handler examples.plugin_handler:handle --principal andrea
```

Persistent request stream:

```text
kyvernex-ai-plugin --handler examples.plugin_handler:handle --principal andrea --stream
```

Then send one JSON object per line.

## Active work
- M8-W004 provider format exporters from the same canonical manifest: `IN_PROGRESS`.

## Boundary
M8 builds one AI-neutral bridge. It does not create separate ChatGPT, Claude, Gemini or Copilot runtimes, remote transports, accounts, billing, dashboards or external services. No verification or release claim is made yet.
