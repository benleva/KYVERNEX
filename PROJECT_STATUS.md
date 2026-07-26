# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Verified milestone: **M16 — Local Verification Report**
- Verified milestone: **M17 — ARGUS Matrix Runner**
- Active milestone: **M18 — ARGUS Executive Translator**
- Active sprint: **S021 — Human language to canonical ARGUS**
- KPM cycle: `KPM-CYCLE-044`
- KGO cycle: `KGO-CYCLE-055`
- Development package version: `1.2.0.dev0`

## Verified ARGUS matrix path
The operator executed `kyvernex-argus` in GitHub Codespaces. The saved request produced `status: DECIDED`, decision `ALLOW`, selected rule `allow-low-risk`, the expected reason, and an ordered rule trace. M17 is therefore `ARGUS_MATRIX_SMOKE_VERIFIED`, not fully tested.

## M18 objective
Translate supported Italian statements into canonical ARGUS JSON without probabilistic inference, then optionally pass that request directly to the existing matrix evaluator.

```text
human Italian text
-> deterministic executive translator
-> canonical request JSON
-> optional ARGUS matrix evaluation
-> translation trace + decision trace
```

## M18 delivered code
### M18-W001 — Deterministic Italian translator
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/argus_translator.py` recognizes explicit consent and risk statements;
- consent values are boolean and risk values are `low`, `medium`, `high`, or `critical`;
- conflicting statements fail closed instead of being guessed;
- unsupported text fails with an explicit translation error;
- output contains normalized source text, canonical request, extraction trace, and unresolved fields.

### M18-W002 — Installed translator and direct matrix path
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/argus_translator_cli.py` provides `kyvernex-argus-translate`;
- text may be supplied with `--text`, from a file, or through stdin;
- `--matrix` immediately evaluates the translated request with the existing Matrix Runner;
- optional output replacement requires `--force`;
- `pyproject.toml` installs the command.

## Boundary
M18 is a deterministic phrase translator, not general natural-language understanding. It does not use an LLM, infer unstated facts, encode the complete ARGUS Constitution, access external data, learn, or claim release readiness. Tests are deferred until the milestone is complete, as directed by the user. No tag or release was created.
