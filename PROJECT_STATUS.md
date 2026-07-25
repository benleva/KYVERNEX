# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7** through **M15**
- Sprint: **S018 — Host-shaped invocation**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-039`
- KGO cycle: `KGO-CYCLE-050`
- Development package version: `1.2.0.dev0`

## Product objective delivered
Accept real AI host calls shaped as a named tool plus arguments through Python, JSON/JSONL and the existing loopback HTTP server, while preserving the direct canonical argument form.

```text
{name, arguments, optional id}
-> KyvernexAIBridge.invoke_tool_call
-> existing invoke(arguments)
-> governed plugin runtime
```

## M15 delivered code

### M15-W001 — Canonical tool-call envelope
Status: `CODE_COMPLETE_UNVERIFIED`

- `KyvernexAIBridge.invoke_tool_call()` accepts only `name`, `arguments` and optional `id`;
- the tool name must equal `kyvernex_execute`;
- arguments are delegated to the existing strict `invoke()` path;
- an optional call id is returned as `tool_call_id`;
- unknown or mixed fields fail closed.

### M15-W002 — CLI envelope routing
Status: `CODE_COMPLETE_UNVERIFIED`

- `kyvernex-ai-plugin` accepts either direct canonical arguments or the canonical tool-call envelope;
- the same behavior applies to single JSON and persistent JSONL modes;
- payloads mixing envelope and direct fields are rejected;
- no provider-specific runtime or duplicated execution path is introduced.

### M15-W003 — Loopback HTTP envelope route
Status: `CODE_COMPLETE_UNVERIFIED`

- `POST /tool-call` accepts the same strict canonical envelope;
- the route delegates only to `KyvernexAIBridge.invoke_tool_call()`;
- `POST /invoke` remains available for direct canonical arguments;
- both routes retain the existing 1 MiB request-body limit and structured JSON errors;
- `src/kyvernex/local_ai_openapi.py` documents the envelope with OpenAPI 3.1;
- the server remains bound exclusively to `127.0.0.1`.

## Current HTTP routes

```text
GET  /
GET  /console
GET  /health
GET  /manifest
GET  /openapi.json
POST /invoke
POST /tool-call
```

## Example

```json
{
  "id": "call-001",
  "name": "kyvernex_execute",
  "arguments": {
    "input": {"message": "hello"}
  }
}
```

## Boundary
M15 is code-complete but unverified. It changes only local invocation shape and routing. It adds no public bind, provider runtime, account, database, verification claim, tag or release publication.
