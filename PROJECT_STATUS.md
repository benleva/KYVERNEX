# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestone: **M7 — Plugin Product Interface**
- Active milestone: **M8 — Universal AI Plugin Bridge**
- Active sprint: **S011 — Provider-neutral AI invocation**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-023`
- KGO cycle: `KGO-CYCLE-034`
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

## M8 active code
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

- `src/kyvernex/ai_plugin_cli.py` reads one JSON object from standard input;
- `--handler module:attribute` selects the explicit host callable;
- `--manifest` prints the tool definition;
- `pyproject.toml` installs `kyvernex-ai-plugin`;
- `src/kyvernex/__init__.py` exports `KyvernexAIBridge`.

## Current use

```text
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest
```

```text
echo '{"input":{"message":"ciao"}}' | kyvernex-ai-plugin --handler examples.plugin_handler:handle --principal andrea
```

## Boundary
M8 builds one AI-neutral bridge. It does not create separate ChatGPT, Claude, Gemini or Copilot plugins, remote transports, accounts, billing, dashboards or external services. No verification or release claim is made yet.
