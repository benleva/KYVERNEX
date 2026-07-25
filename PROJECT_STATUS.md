# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7** through **M15**
- Runtime evidence: **LOCAL_APP_SMOKE_VERIFIED**
- Active milestone: **M16 — Local Verification Report**
- Active sprint: **S019 — Repeatable local verification**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-041`
- KGO cycle: `KGO-CYCLE-052`
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

Observed runtime facts remain recorded in `RUNTIME_SMOKE_EVIDENCE.md`.

## M16 product objective

Turn the one-time local smoke command into a reusable verification report covering the current local app contract without claiming full release qualification.

```text
kyvernex-ai-smoke --output verification.json
-> loopback server on an operating-system selected port
-> health check
-> canonical, OpenAI, Anthropic and Gemini manifest checks
-> OpenAPI route check
-> direct invocation
-> tool-call envelope invocation
-> explicit verification boundary
-> optional persistent JSON report
```

## M16 delivered code

### M16-W001 — Expanded local verification command
Status: `CODE_COMPLETE_UNVERIFIED`

- `kyvernex-ai-smoke` now accepts `--output PATH` and `--force`;
- the command verifies adapter health is `HEALTHY`;
- canonical, OpenAI, Anthropic and Gemini manifest shapes are inspected;
- the OpenAPI document must expose `/invoke` and `/tool-call`;
- direct and tool-call HTTP paths must return `SUCCEEDED`;
- the tool-call correlation id must be preserved;
- the JSON report identifies both verified checks and remaining unverified areas;
- an existing report is never replaced without `--force`.

## Active work

- M16-W002 operator execution of the expanded command and capture of a persistent report: `READY_FOR_OPERATOR_RUN`.

## Verification boundary

The earlier Codespaces smoke remains valid evidence for the local app path. The expanded M16 command has been written but has not yet been executed after this change. Full automated suite success, clean installations on separate operating systems, portable launcher compatibility, JSONL coverage, timeout and size-limit behavior, concurrency, load, recovery and release qualification remain unverified. No tag or release was created.
