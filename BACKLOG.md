# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestone: `M7 — Plugin Product Interface`
- Code-complete milestone: `M8 — Universal AI Plugin Bridge`
- Code-complete milestone: `M9 — Local AI Tool Server`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7-W001 through M7-W005: `CODE_COMPLETE_UNVERIFIED`;
- M8-W001 through M8-W004: `CODE_COMPLETE_UNVERIFIED`.

## M9 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M9-W001 | Loopback-only HTTP server for the canonical AI bridge | P0 | CODE_COMPLETE_UNVERIFIED |
| M9-W002 | Installed `kyvernex-ai-server` command | P0 | CODE_COMPLETE_UNVERIFIED |
| M9-W003 | Local OpenAPI 3.1 document generated from the server contract | P1 | CODE_COMPLETE_UNVERIFIED |
| M9-W004 | Self-contained local invocation console using the existing routes | P1 | CODE_COMPLETE_UNVERIFIED |

## M9 code evidence
- `src/kyvernex/local_ai_server.py`: loopback server, fixed routes and console delivery;
- `src/kyvernex/local_ai_server_cli.py`: installed process command;
- `src/kyvernex/local_ai_openapi.py`: generated OpenAPI document;
- `src/kyvernex/local_ai_page.py`: self-contained local browser console;
- `pyproject.toml`: `kyvernex-ai-server` entry point.

## Local routes

```text
GET  /
GET  /console
GET  /health
GET  /manifest?format=canonical|openai|anthropic|gemini
GET  /openapi.json
POST /invoke
```

The browser console calls only the same-origin local routes. The server remains bound to `127.0.0.1`; `POST /invoke` accepts at most 1 MiB and uses the existing `KyvernexAIBridge`.

## Boundary
M9 has no active coding item. It is code-complete but unverified. Public hosting, authentication services, TLS infrastructure, databases, accounts, billing and provider-specific runtime forks remain outside the delivered milestone. No green, clean-install, publication or release claim is made.
