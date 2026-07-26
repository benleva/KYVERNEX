# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Verified milestone: **M16 — Local Verification Report**
- Verified milestone: **M17 — ARGUS Matrix Runner**
- Active milestone: **M18 — ARGUS Executive Translator**
- Active sprint: **S021 — Human language to canonical ARGUS**
- KPM cycle: `KPM-CYCLE-046`
- KGO cycle: `KGO-CYCLE-057`
- Development package version: `1.2.0.dev0`

## M18 objective
Translate supported Italian statements into canonical ARGUS JSON without probabilistic inference, optionally evaluate the request, and preserve a reversible symbolic and audit representation.

```text
human Italian text
-> deterministic normalization
-> bounded lexical rules
-> canonical request JSON
-> reversible ARGUS symbols
-> optional matrix evaluation
-> audit envelope
```

## M18 delivered code

### M18-W001 — Deterministic Italian translator
Status: `CODE_COMPLETE_UNVERIFIED`

### M18-W002 — Installed translator command
Status: `CODE_COMPLETE_UNVERIFIED`

### M18-W003 — Direct matrix execution
Status: `CODE_COMPLETE_UNVERIFIED`

### M18-W004 — Controlled vocabulary expansion
Status: `CODE_COMPLETE_UNVERIFIED`

- consent and authorization are separate boolean fields;
- risk is limited to `low`, `medium`, `high`, and `critical`;
- subject minority is represented at `subject.minor`;
- bounded domains are `health`, `finance`, `legal`, and `education`;
- contradictions fail closed and every match remains traceable.

### M18-W005 — Reversible symbolic projection
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/argus_symbols.py` maps every currently supported canonical fact to one ARGUS token;
- encoding fails if a fact cannot be represented without information loss;
- decoding rejects malformed, unknown, duplicate, or conflicting symbols;
- canonical facts are ordered before projection, producing stable sequences.

### M18-W006 — Audit envelope
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/argus_audit.py` records input, normalization, lexical translation, canonical request, symbols, and optional matrix evaluation;
- `kyvernex-argus-translate --audit-envelope` emits the envelope directly;
- normal output now also includes the symbolic projection.

## Active work
M18-W007 will define the complete end-of-milestone verification manifest and operator runbook. Execution of that verification remains deferred until the implementation boundary is closed, as directed by the user.

## Boundary
M18 remains deterministic and closed-world. It does not use an LLM, infer unstated facts, encode the complete ARGUS Constitution, access external data, learn, or claim release readiness. No tests were run in this change. No tag or release was created.
