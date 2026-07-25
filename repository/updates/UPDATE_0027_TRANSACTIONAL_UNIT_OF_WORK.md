# UPDATE 0027 - Transactional Unit of Work

## Summary

Introduced the first KYVERNEX Unit of Work for coordinated cognitive creation across session memory, the cognitive graph and persistent audit.

## Added

- `src/kyvernex/unit_of_work.py`
- `tests/test_unit_of_work.py`
- `repository/specifications/UNIT_OF_WORK_SPEC_v0.1_DRAFT.md`

## Updated

- `src/kyvernex/__init__.py`

## Public API

- `KyvernexUnitOfWork`
- `UnitOfWorkState`
- `UnitOfWorkResult`
- `UnitOfWorkError`
- `UnitOfWorkStateError`
- `UnitOfWorkCommitError`

## Implemented behavior

- explicit transaction lifecycle;
- staged cognitive objects;
- staged cognitive relations;
- staged audit events;
- referential-integrity validation before commit;
- ordered commit across memory, graph and audit;
- reverse-order rollback of applied memory and graph writes;
- context-manager support;
- explicit reporting of incomplete rollback.

## Tests added

The test module covers:

- successful coordinated commit;
- rollback after audit persistence failure;
- rejection of relations with missing endpoints;
- automatic commit through the context manager.

## Verification status

The code and tests have been committed to the repository. The test suite has not been executed in this update, therefore no passing-test claim is made.

## Known limitations

- process-local coordination only;
- no crash-safe Unit of Work journal;
- no distributed transactions;
- external audit sinks must make `append_many()` atomic to avoid a partially written audit batch;
- version 0.1 coordinates creation, while deletion continues to use the existing deletion transaction architecture.

## Next step

Execute the complete test suite and correct integration failures before extending the Unit of Work with durable recovery.
