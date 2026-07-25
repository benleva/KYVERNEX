# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestone: `M7 — Plugin Product Interface`
- Code-complete milestone: `M8 — Universal AI Plugin Bridge`
- Active milestone: `M9 — Local AI Tool Server`
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
| M9-W003 | Local OpenAPI document generated from the canonical routes | P1 | IN_PROGRESS |

## M9 code evidence
- `src/kyvernex/local_ai_server.py`: `127.0.0.1` HTTP server;
- `src/kyvernex/local_ai_server_cli.py`: installed process command;
- `pyproject.toml`: `kyvernex-ai-server` entry point.

## Local routes

```text
GET  /health
GET  /manifest?format=canonical|openai|anthropic|gemini
POST /invoke
```

`POST /invoke` accepts at most 1 MiB and uses the existing `KyvernexAIBridge`. The server does not bind publicly and introduces no external network client or cloud dependency.

## Product rule
M9 remains local-only. Public hosting, authentication services, TLS infrastructure, databases, dashboards and provider-specific execution forks are outside this milestone. Testing is not the active user-directed workstream and no green claim is made.
