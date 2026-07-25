# UPDATE 0032 - COGNITIVE DECISION GATE

## Added
- `src/kyvernex/decision_gate.py`
- `tests/test_decision_gate.py`
- `repository/specifications/COGNITIVE_DECISION_GATE_SPEC_v0.1_DRAFT.md`

## Updated
- `src/kyvernex/__init__.py`

## Capability
KYVERNEX can now convert a cognitive dossier into a deterministic governed disposition using confidence thresholds, audit requirements, contradiction policy and explicit reservations.

## New public API
- CognitiveDecisionGate
- DecisionPolicy
- DecisionDisposition
- GovernedDecision
- DecisionGateError

## Audit event
- DECISIONE_GOVERNATA

## Verification status
Tests were added but no successful execution is claimed by this update.
