# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Verified milestone: **M16 — Local Verification Report**
- Verified milestone: **M17 — ARGUS Matrix Runner**
- Active milestone: **M18 — ARGUS Executive Translator**
- Active sprint: **S021 — Human language to canonical ARGUS**
- KPM cycle: `KPM-CYCLE-045`
- KGO cycle: `KGO-CYCLE-056`
- Development package version: `1.2.0.dev0`

## M18 objective
Translate supported Italian statements into canonical ARGUS JSON without probabilistic inference, then optionally pass that request directly to the existing matrix evaluator.

```text
human Italian text
-> deterministic normalization
-> bounded lexical rules
-> canonical request JSON
-> optional ARGUS matrix evaluation
-> translation trace + decision trace
```

## M18 delivered code

### M18-W001 — Deterministic Italian translator
Status: `CODE_COMPLETE_UNVERIFIED`

- closed-world translation rejects unsupported text;
- conflicting values fail closed;
- output preserves source text, normalized text, canonical request and trace.

### M18-W002 — Installed translator command
Status: `CODE_COMPLETE_UNVERIFIED`

- `kyvernex-argus-translate` accepts direct text, file input or stdin;
- output may be persisted explicitly;
- replacement requires `--force`.

### M18-W003 — Direct matrix execution
Status: `CODE_COMPLETE_UNVERIFIED`

- `--matrix` sends the canonical request to the existing deterministic Matrix Runner;
- translator and evaluator traces remain separate in the response.

### M18-W004 — Controlled vocabulary expansion
Status: `CODE_COMPLETE_UNVERIFIED`

- normalization is case-insensitive, whitespace-stable and accent-folded for matching;
- consent and authorization are represented as separate boolean fields;
- risk remains limited to `low`, `medium`, `high`, and `critical`;
- minor/adult subject status is represented at `subject.minor`;
- bounded domains are `health`, `finance`, `legal`, and `education`;
- explicit synonyms and negations map to canonical values;
- every extracted field records lexical rule ids and matched fragments;
- translator contract version is `0.2`.

## Active work

M18-W005 will add the canonical symbolic projection and a reusable audit envelope. Tests remain deferred until all M18 implementation items are complete, as directed by the user.

## Boundary

M18 is a deterministic phrase translator, not general natural-language understanding. It does not use an LLM, infer unstated facts, encode the complete ARGUS Constitution, access external data, learn, or claim release readiness. No tests were run in this change. No tag or release was created.
