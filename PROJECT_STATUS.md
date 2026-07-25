# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7** through **M14**
- Active milestone: **M15 — Canonical Tool Call Envelope**
- Active sprint: **S018 — Host-shaped invocation**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-038`
- KGO cycle: `KGO-CYCLE-049`
- Development package version: `1.2.0.dev0`

## Product objective
Accept real AI host calls shaped as a named tool plus arguments while preserving the existing direct canonical argument form.

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
M15 changes only local invocation shape and routing. It adds no network service, provider runtime, account, database, verification claim, tag or release publication.
