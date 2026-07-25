# KGO v2 Technical Specification v0.1 DRAFT

## Purpose
KGO v2 extends CI evidence classification into deterministic governance planning. It does not claim to repair code autonomously. It groups failures by probable shared cause, estimates impact, confidence and effort, and emits controlled patch plans.

## Inputs
- Complete pytest textual output.
- Existing KGO v1 parsed analysis.

## Outputs
- `KGO_V2_REPORT.json`
- `KGO_ROOT_CAUSES.json`
- `KGO_PATCH_PLAN.json`
- `KGO_V2_SUMMARY.md`

## Components
1. Root Cause Grouper: converts repeated failure signatures into shared causes.
2. Dependency/Impact Projection: counts affected tests and projects the success percentage after one cause is removed.
3. Confidence Engine: deterministic signature-based confidence scoring.
4. Cost Engine: coarse effort classification (`SMALL`, `MEDIUM`, `UNKNOWN`).
5. Patch Planner: lists probable files, validation tests and the exact targeted pytest command.
6. Governance Gate: permits only an isolated patch proposal when confidence and effort thresholds are met. Passing tests are still required; automatic merge is forbidden.

## Safety rules
- Never fabricate a source line or confirmed root cause.
- `probable_files` are hypotheses, not verified fault locations.
- Contract mismatches require specification, implementation and test review.
- Autonomous patch eligibility is not authorization to merge.
- A failing complete suite keeps the workflow `BLOCKED`.

## Current deterministic signatures
- `UNHASHABLE_DICT`
- `KEX_TIMEOUT_POLICY`
- `ERROR_CONTRACT_REGEX`
- assertion contracts grouped per test module
- fallback category/reason signature

## Definition of Done
- Specification committed.
- Implementation committed.
- Unit tests committed.
- GitHub Actions integration committed.
- Complete CI run verified separately.
- Documentation and project status synchronized.
