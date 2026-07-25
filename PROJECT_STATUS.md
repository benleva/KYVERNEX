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
- KPM cycle: `KPM-CYCLE-027`
- KGO cycle: `KGO-CYCLE-038`
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
- request bodies are bounded to 1 MiB;
- no external network client, cloud service or provider runtime is introduced.

### M9-W002 — Installed local server command
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_server_cli.py` provides the process entry point;
- `pyproject.toml` installs `kyvernex-ai-server`;
- one explicit `module:attribute` handler is used.

### M9-W003 — Generated local OpenAPI document
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_openapi.py` generates OpenAPI `3.1.0`;
- the document describes `/health`, `/manifest`, `/invoke` and itself;
- the server URL is generated from the actual loopback address and bound port;
- `GET /openapi.json` serves the document;
- the invocation schema accepts only `input`, optional `context` and optional `request_id`.

## Current routes

```text
GET  /health
GET  /manifest?format=canonical|openai|anthropic|gemini
GET  /openapi.json
POST /invoke
```

## Active work
- M9-W004 minimal local invocation page using only the existing HTTP routes: `IN_PROGRESS`.

## Boundary
M9 remains loopback-only. It does not expose `0.0.0.0`, TLS termination, authentication services, public hosting, databases, accounts or billing. The planned local page may call only this same server and may not introduce another backend. No verification or release claim is made.
