# UPDATE 0029 - COGNITIVE VERSIONING

## Stato
IMPLEMENTATO, NON ANCORA VERIFICATO DA ESECUZIONE TEST.

## File creati
- `src/kyvernex/versioning.py`
- `tests/test_versioning.py`
- `repository/specifications/VERSIONING_POLICY_SPEC_v0.1_DRAFT.md`

## File aggiornati
- `src/kyvernex/__init__.py`

## Funzionalità introdotte
- `CognitiveVersionManager`
- `VersionChangeType`
- `VersionTransition`
- `VersioningError`
- `VersionConflictError`
- revisione immutabile degli oggetti cognitivi
- relazione automatica `DERIVED_FROM`
- rollback della memoria se la relazione non può essere creata
- ricostruzione della storia dal più recente al più antico
- rilevazione di formato versione invalido, cicli, predecessori mancanti e storie ambigue

## Verifica
I test sono presenti ma non viene dichiarato alcun esito finché la suite non è eseguita e osservata tramite ambiente locale o CI.
