# KYVERNEX RUNTIME SMOKE EVIDENCE

## Evidence classification

Status: `LOCAL_APP_SMOKE_VERIFIED`

Environment: GitHub Codespaces, Python 3.12, repository default branch, development package `1.2.0.dev0`.

Evidence source: operator-executed commands and browser screenshots supplied during the interactive run on 26 July 2026.

## Commands executed by the operator

```text
python -m pip install -e .
kyvernex-ai-smoke
kyvernex-ai-project prova-kyvernex --principal andrea --no-browser
cd prova-kyvernex
python -m kyvernex.local_ai_app_cli --profile kyvernex.local.json
```

## Observed successful behavior

- editable installation completed and reported `Successfully installed kyvernex-1.2.0.dev0`;
- `kyvernex-ai-smoke` executed the local runtime and returned governed response data without a displayed traceback;
- the generated `prova-kyvernex` project was present in the Codespaces workspace;
- the local app reported `status: READY` with console address `http://127.0.0.1:8765/`;
- Codespaces forwarded port `8765` as a private port;
- the KYVERNEX Local AI browser console loaded successfully;
- the Status panel returned adapter status `HEALTHY` and capability `governed.execute`;
- network execution remained disabled, process execution remained disabled and repository authority remained `FORBIDDEN`;
- a browser-originated governed invocation completed with `status: SUCCEEDED`;
- the invocation preserved principal `andrea`;
- the generated handler returned `handled_by: local-project`;
- the handler received the input message `Prima prova reale di KYVERNEX`;
- the runtime reported `error: null`, a request id, execution timestamps and configured execution limits.

## Verified path

```text
editable install
-> generated local project
-> explicit local profile
-> loopback server
-> Codespaces private port forwarding
-> browser console
-> health/status retrieval
-> governed execute request
-> local project handler
-> successful governed response
```

The separate `kyvernex-ai-smoke` command also exercised the direct `/invoke` and canonical `/tool-call` routes and checked preservation of `tool_call_id` in its implementation. The operator ran this command successfully, but the complete formatted JSON report was not archived in the repository.

## Scope boundary

This evidence verifies one local Codespaces smoke path. It does not establish:

- full automated test-suite success;
- clean-install verification on Windows, macOS or Linux hosts outside Codespaces;
- portable launcher compatibility on all operating systems;
- JSONL CLI coverage;
- every provider-shaped manifest;
- concurrency, load, security or failure-recovery testing;
- release readiness;
- tag or package publication.

Stable release `v1.1.0` remains unchanged. Development version remains `1.2.0.dev0`.
