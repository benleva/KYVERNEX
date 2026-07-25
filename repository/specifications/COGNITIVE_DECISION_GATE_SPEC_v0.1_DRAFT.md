# COGNITIVE DECISION GATE SPEC v0.1 DRAFT

## Purpose
Define the deterministic KYVERNEX gate that converts a cognitive decision dossier into an operational disposition.

## Inputs
- session id
- cognitive object id
- CognitiveDecisionDossier
- DecisionPolicy

## Dispositions
- APPROVATA
- APPROVATA_CON_RISERVA
- REVISIONE_UMANA_RICHIESTA
- BLOCCATA

## Policy parameters
- approval_threshold
- reservation_threshold
- require_verified_audit
- block_on_contradictions
- max_reservations_for_approval

## Mandatory behavior
1. Build the dossier through CognitiveDecisionExplainer.
2. Evaluate propagated confidence against deterministic thresholds.
3. Block when mandatory audit evidence is absent or invalid.
4. Optionally block when contradictions are present.
5. Preserve reasons and reservations.
6. Persist DECISIONE_GOVERNATA when an audit sink is configured.
7. Never generate or infer missing evidence.

## Audit requirement
Verified audit means both:
- the audit chain verifies successfully;
- at least one audit record exists for the governed object.

## Limitations
- Policy evaluation is process-local.
- The gate does not execute the approved action.
- Threshold selection remains a deployment responsibility.
- Test execution is not asserted by this specification.
