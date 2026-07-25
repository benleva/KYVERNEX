# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestone: **M7 — Plugin Product Interface**
- Code-complete milestone: **M8 — Universal AI Plugin Bridge**
- Code-complete milestone: **M9 — Local AI Tool Server**
- Sprint: **S012 — Loopback HTTP access**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-028`
- KGO cycle: `KGO-CYCLE-039`
- Development package version: `1.2.0.dev0`

## Product path

```text
local AI host or browser
-> http://127.0.0.1:8765
-> KyvernexLocalAIServer
-> KyvernexAIBridge
-> KyvernexPlugin
-> governed runtime
-> bounded host callable
```

## M9 code delivered

### M9-W001 — Localhost HTTP server
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_server.py` provides `KyvernexLocalAIServer`;
- binding is fixed to `127.0.0.1`;
- request bodies are bounded to 1 MiB;
- no external network client, cloud service or provider runtime is introduced.

### M9-W002 — Installed local server command
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_server_cli.py` provides `kyvernex-ai-server`;
- one explicit `module:attribute` handler is used;
- the port is selectable while the host remains loopback-only.

### M9-W003 — Generated local OpenAPI document
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_openapi.py` generates OpenAPI `3.1.0`;
- `GET /openapi.json` serves the document;
- the server URL reflects the actual loopback port.

### M9-W004 — Local invocation console
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_page.py` provides one self-contained HTML page;
- `GET /` and `GET /console` serve the page from the existing process;
- the page reads `/health` and `/manifest`;
- the page sends governed requests only to `/invoke`;
- no external script, stylesheet, backend, account, database or remote service is used;
- a content-security policy restricts resources and connections to the same local origin.

## Current routes

```text
GET  /
GET  /console
GET  /health
GET  /manifest?format=canonical|openai|anthropic|gemini
GET  /openapi.json
POST /invoke
```

## Current use

```text
kyvernex-ai-server --handler examples.plugin_handler:handle --principal andrea --port 8765
```

Then open:

```text
http://127.0.0.1:8765/
```

## Boundary
M9 is code-complete but unverified. It remains loopback-only and introduces no public bind, TLS service, authentication system, hosting platform, database, account or billing component. No clean-install, CI, publication or release claim is made.
