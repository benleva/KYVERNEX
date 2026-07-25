# COGNITIVE DECISION DOSSIER SPEC v0.1 DRAFT

## Status
Draft implementation specification.

## Purpose
Define the minimum evidence package required to inspect one KYVERNEX cognitive object without generating unsupported natural-language explanations.

## Required inputs
- session identifier;
- cognitive object identifier;
- session memory;
- cognitive graph;
- confidence engine;
- optional audit trace reader.

## Required output
A `CognitiveDecisionDossier` containing:
- immutable snapshot of the selected cognitive object;
- complete predecessor version history available in memory and graph;
- incoming relations;
- outgoing relations;
- direct and propagated confidence assessment;
- object-specific audit records;
- audit integrity verification state;
- explicit reservations for missing evidence.

## Normative rules
1. The object MUST exist in the requested session.
2. The dossier MUST NOT infer evidence absent from memory, graph or audit trace.
3. Version history MUST follow `DERIVED_FROM` relations.
4. Confidence MUST be produced by `CognitiveConfidenceEngine`.
5. When an audit trace is configured, its integrity MUST be verified before records are exposed.
6. Audit records MUST be filtered by both session and object identifier.
7. Missing optional evidence MUST be represented as reservations, not silently ignored.
8. Duplicate reservations MUST be removed while preserving their first occurrence order.

## Reservations
Current standard reservations include:
- `AUDIT_TRACE_NON_CONFIGURATO`;
- `AUDIT_OGGETTO_ASSENTE`;
- `NESSUNA_REVISIONE_PRECEDENTE`;
- `OGGETTO_ISOLATO_NEL_GRAFO`;
- reservations returned by the confidence engine.

## Limitations
- The dossier is evidence assembly, not causal proof.
- It does not generate prose justifications.
- It does not sign or externally certify the exported dossier.
- It reflects the current state of configured stores at read time.
