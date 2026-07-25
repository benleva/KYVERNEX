# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestone: **M7 — Plugin Product Interface**
- Code-complete milestone: **M8 — Universal AI Plugin Bridge**
- Sprint: **S011 — Provider-neutral AI invocation**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-025`
- KGO cycle: `KGO-CYCLE-036`
- Development package version: `1.2.0.dev0`

## Product path

```text
AI host
-> canonical or provider-shaped tool manifest
-> kyvernex-ai-plugin / KyvernexAIBridge
-> KyvernexPlugin
-> governed runtime
-> bounded host callable
-> structured response
```

## M8 code delivered

### M8-W001 — Provider-neutral AI bridge
Status: `CODE_COMPLETE_UNVERIFIED`

`src/kyvernex/ai_bridge.py` provides one canonical tool named `kyvernex_execute`, strict arguments and governed invocation.

### M8-W002 — Installed AI bridge command
Status: `CODE_COMPLETE_UNVERIFIED`

`kyvernex-ai-plugin` accepts an explicit `module:attribute` handler, prints manifests and processes JSON requests.

### M8-W003 — Persistent multi-request process
Status: `CODE_COMPLETE_UNVERIFIED`

`--stream` keeps one bridge alive and processes JSON Lines with per-line error isolation.

### M8-W004 — Provider manifest exporters
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/ai_formats.py` translates the canonical manifest;
- supported shapes: `canonical`, `openai`, `anthropic`, `gemini`;
- `KyvernexAIBridge.manifest_for(provider)` exposes the translation in Python;
- `kyvernex-ai-plugin --manifest --manifest-format FORMAT` exposes it from the installed command;
- exporters change only field layout and never duplicate runtime or governance logic.

## Manifest examples

```text
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest --manifest-format canonical
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest --manifest-format openai
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest --manifest-format anthropic
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest --manifest-format gemini
```

## Boundary
M8 is code-complete but unverified. No separate provider runtime, remote transport, account system, dashboard, publication or release claim has been added.
