# UPDATE 0031 - COGNITIVE DECISION DOSSIER

## Added
- `src/kyvernex/explainability.py`
- `tests/test_explainability.py`
- `repository/specifications/COGNITIVE_DECISION_DOSSIER_SPEC_v0.1_DRAFT.md`

## Updated
- `src/kyvernex/__init__.py`

## Capability
KYVERNEX can now assemble a deterministic evidence dossier for a cognitive object by combining:
- object snapshot;
- version lineage;
- incoming and outgoing graph relations;
- confidence propagation;
- object-specific audit records;
- audit chain verification;
- explicit evidence reservations.

## Architectural impact
This update introduces a read-only explainability layer above memory, graph, versioning, confidence and audit trace. It does not alter stored cognitive objects and does not generate unsupported narrative explanations.

## Verification status
Tests were added but have not been observed running successfully in this update. CI status remains unconfirmed until a workflow execution is fetched and inspected.
