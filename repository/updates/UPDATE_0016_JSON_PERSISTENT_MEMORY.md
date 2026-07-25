# UPDATE 0016 — JSON PERSISTENT MEMORY

## Status
Implemented in Reference Prototype 0.1. This update does not promote the project to Alpha.

## Scope
KYVERNEX now provides an optional local JSON memory backend through `JsonSessionMemory`.

## Behaviour
- session isolation is preserved across process restarts;
- cognitive objects are stored with category, state, transformations, rules, limitations and metadata;
- writes use a temporary file followed by atomic replacement;
- the storage document declares `format_version`;
- malformed files and unsupported versions are rejected explicitly;
- reads and writes retain defensive-copy semantics;
- clearing a session is persisted immediately.

## Integration
`KyvernexEngine` already accepts a memory implementation through constructor injection. Passing `JsonSessionMemory(path)` activates persistence without changing the execution pipeline.

## Limitations
- local filesystem only;
- no encryption at rest;
- no file locking between multiple operating-system processes;
- no retention policy, expiry or capacity quota;
- JSON-compatible object content and metadata are required;
- migration between future storage versions is not yet implemented.

## Tests added
`tests/test_json_persistence.py` covers restart recovery, session isolation, persisted clearing, malformed JSON and unsupported format versions.

## Verification state
Tests are committed but must not be described as CI-verified until a GitHub Actions run is observable.
