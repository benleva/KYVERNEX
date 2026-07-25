# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7` through `M14`
- Active milestone: `M15 — Canonical Tool Call Envelope`
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
| M15-W003 | Local HTTP envelope route reusing the same bridge method | P1 | BACKLOG |

## M15 code evidence
- `src/kyvernex/ai_bridge.py`: strict `invoke_tool_call()` method;
- `src/kyvernex/ai_plugin_cli.py`: direct or envelope payload routing;
- unknown names, fields and mixed payloads fail closed;
- optional envelope id is echoed as `tool_call_id`;
- direct canonical arguments remain supported.

## Product behavior

```json
{"name":"kyvernex_execute","arguments":{"input":{"message":"hello"}}}
```

## Boundary
M15 may expose this same envelope through the existing loopback HTTP process only. It must not create provider-specific runtimes, public hosting, accounts, databases or publication claims. Testing is not the active user-directed workstream and no green claim is made.
