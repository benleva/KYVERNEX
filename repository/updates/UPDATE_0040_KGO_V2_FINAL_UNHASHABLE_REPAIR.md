# UPDATE 0040 — KGO v2 final unhashable relation repair

## Status
IMPLEMENTED_NOT_VERIFIED

## Trigger evidence
A user-observed GitHub Actions run reported:
- 97 passed
- 3 failed
- 0 skipped
- 97.0% success
- one remaining KGO v2 root cause: `UNHASHABLE_DICT`

The three failures were concentrated in durable, multi-transaction and process-safe deletion paths.

## Root cause
`DurableDeletionCoordinator` and `MultiTransactionDeletionCoordinator` still deduplicated `CognitiveRelation` instances through `dict.fromkeys(...)`. `CognitiveRelation` contains mutable dictionary metadata and is therefore not hashable.

The base deletion coordinator had already been corrected, but these two journaling subclasses retained the obsolete pattern. The process-safe coordinator inherits the multi-transaction implementation and therefore inherited the same failure.

## Changes
- Updated `src/kyvernex/durable_deletion.py`.
- Updated `src/kyvernex/transaction_journal.py`.
- Replaced relation-object hashing with deterministic deduplication keyed by `relation_id`.
- Preserved relation order and full relation objects for journal encoding.
- No test expectations were weakened.

## Expected impact
The repair targets the three remaining failures:
- `tests/test_durable_deletion.py::test_successful_cascade_removes_journal`
- `tests/test_multi_transaction_deletion.py::test_completed_deletion_removes_its_transaction_journal`
- `tests/test_process_safe_deletion.py::test_process_safe_coordinator_completes_cascade_deletion`

Expected complete-suite result: 100 passed, 0 failed. This is a projection only until a fresh CI run verifies it.

## Governance
No release or milestone is declared complete from this commit alone. GitHub Actions must rerun the complete test suite and preserve KGO evidence before the repair can be marked verified.
