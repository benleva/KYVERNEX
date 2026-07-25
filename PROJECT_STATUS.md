# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7** through **M15**
- Runtime evidence: **LOCAL_APP_SMOKE_VERIFIED**
- Sprint: **S018 — Host-shaped invocation**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-040`
- KGO cycle: `KGO-CYCLE-051`
- Development package version: `1.2.0.dev0`

## Verified local product path

On 26 July 2026 the operator executed the development package in GitHub Codespaces and supplied terminal and browser evidence for this path:

```text
editable install
-> kyvernex-ai-smoke
-> generated local project
-> explicit profile
-> loopback app on 127.0.0.1:8765
-> private Codespaces port forwarding
-> browser console
-> governed execute
-> generated local handler
-> SUCCEEDED response
```

Observed runtime facts:

- editable installation reported `Successfully installed kyvernex-1.2.0.dev0`;
- the app reported `status: READY`;
- the browser console loaded;
- adapter status was `HEALTHY`;
- capability `governed.execute` was active;
- network and process authority remained disabled;
- repository authority remained `FORBIDDEN`;
- the browser invocation returned `status: SUCCEEDED` and `error: null`;
- principal `andrea`, handler marker `local-project` and the submitted input were preserved.

Detailed evidence and limits are recorded in `RUNTIME_SMOKE_EVIDENCE.md`.

## M15 delivered code

### M15-W001 — Canonical tool-call envelope
Status: `CODE_COMPLETE_SMOKE_COVERED`

- `KyvernexAIBridge.invoke_tool_call()` accepts only `name`, `arguments` and optional `id`;
- the tool name must equal `kyvernex_execute`;
- arguments are delegated to the existing strict `invoke()` path;
- an optional call id is returned as `tool_call_id`;
- unknown or mixed fields fail closed.

### M15-W002 — CLI envelope routing
Status: `CODE_COMPLETE_PARTIALLY_VERIFIED`

- `kyvernex-ai-plugin` accepts either direct canonical arguments or the canonical tool-call envelope;
- the same behavior applies to single JSON and persistent JSONL modes;
- payloads mixing envelope and direct fields are rejected;
- JSONL and all CLI failure branches were not exercised in the recorded run.

### M15-W003 — Loopback HTTP envelope route
Status: `LOCAL_HTTP_SMOKE_VERIFIED`

- `POST /tool-call` delegates to `KyvernexAIBridge.invoke_tool_call()`;
- `POST /invoke` remains available for direct canonical arguments;
- `kyvernex-ai-smoke` was executed by the operator and exercises both routes;
- the browser console independently verified the direct governed invocation path;
- the server remained bound to `127.0.0.1` and was forwarded privately by Codespaces.

## Verification boundary

This is a successful local smoke verification, not a full release qualification. Automated suite success, clean installations on separate Windows/macOS/Linux machines, portable launcher compatibility, JSONL coverage, every provider manifest, concurrency, load, security and recovery testing remain unverified. No tag or release was created.