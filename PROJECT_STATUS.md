# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestone: **M7 — Plugin Product Interface**
- Code-complete milestone: **M8 — Universal AI Plugin Bridge**
- Active milestone: **M9 — Local AI Tool Server**
- Active sprint: **S012 — Loopback HTTP access**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-026`
- KGO cycle: `KGO-CYCLE-037`
- Development package version: `1.2.0.dev0`

## Product objective
Expose the existing canonical AI bridge through one localhost-only HTTP server that desktop agents and local AI hosts can call without embedding Python.

```text
local AI host
-> http://127.0.0.1:8765
-> KyvernexLocalAIServer
-> KyvernexAIBridge
-> KyvernexPlugin
-> governed runtime
-> bounded host callable
```

## M9 delivered code
### M9-W001 — Localhost HTTP server
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_server.py` provides `KyvernexLocalAIServer`;
- binding is fixed to `127.0.0.1`;
- `GET /health` returns plugin status;
- `GET /manifest?format=canonical|openai|anthropic|gemini` returns the existing manifest;
- `POST /invoke` accepts one canonical invocation object;
- request bodies are bounded to 1 MiB;
- unknown routes return structured JSON errors;
- no external network client, cloud service or provider runtime is introduced.

### M9-W002 — Installed local server command
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_server_cli.py` provides the process entry point;
- `pyproject.toml` installs `kyvernex-ai-server`;
- `--handler module:attribute` selects one explicit host callable;
- `--principal` fixes the governed principal;
- `--port` selects the local TCP port.

## Current use

```text
kyvernex-ai-server --handler examples.plugin_handler:handle --principal andrea --port 8765
```

Endpoints:

```text
GET  http://127.0.0.1:8765/health
GET  http://127.0.0.1:8765/manifest?format=openai
POST http://127.0.0.1:8765/invoke
```

## Boundary
M9 is limited to local loopback transport. It does not expose `0.0.0.0`, TLS termination, authentication services, public hosting, databases, dashboards, accounts or billing. No verification or release claim is made.
