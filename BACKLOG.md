# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7` through `M15`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M14 work items: `CODE_COMPLETE_UNVERIFIED`.

## M15 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M15-W001 | Strict `name` plus `arguments` tool-call envelope on `KyvernexAIBridge` | P0 | CODE_COMPLETE_UNVERIFIED |
| M15-W002 | Automatic direct/envelope routing in single JSON and JSONL CLI modes | P0 | CODE_COMPLETE_UNVERIFIED |
| M15-W003 | Loopback `POST /tool-call` route reusing the same bridge method | P1 | CODE_COMPLETE_UNVERIFIED |

## M15 code evidence
- `src/kyvernex/ai_bridge.py`: strict `invoke_tool_call()` method;
- `src/kyvernex/ai_plugin_cli.py`: direct or envelope payload routing;
- `src/kyvernex/local_ai_server.py`: dedicated `/tool-call` route and shared bounded JSON parsing;
- `src/kyvernex/local_ai_openapi.py`: OpenAPI 3.1 schema for direct arguments and tool-call envelope;
- unknown names, fields and mixed payloads fail closed;
- optional envelope id is echoed as `tool_call_id`;
- direct canonical arguments remain supported through `/invoke`.

## Product behavior

```json
{"id":"call-001","name":"kyvernex_execute","arguments":{"input":{"message":"hello"}}}
```

## Boundary
M15 has no active coding item. It is code-complete but unverified. The envelope is exposed only through the existing loopback process. Provider-specific runtimes, public hosting, accounts, databases, tests and publication claims remain outside the milestone.
