# UPDATE 0025 — PERSISTENT HASH-CHAINED AUDIT TRACE

## Stato

Implementato nel repository. Test presenti ma non dichiarati superati finché non eseguiti localmente o da CI.

## Obiettivo

Colmare l'assenza della specifica Audit Trace e introdurre un ledger durevole e verificabile per gli eventi `AuditEvent` prodotti da KYVERNEX.

## Modifiche

Creati:

- `src/kyvernex/audit_trace.py`
- `tests/test_audit_trace.py`
- `repository/specifications/AUDIT_TRACE_SPEC_v0.1_DRAFT.md`
- `repository/updates/UPDATE_0025_PERSISTENT_HASH_CHAINED_AUDIT_TRACE.md`

Aggiornato:

- `src/kyvernex/__init__.py`

## API

- `JsonAuditTrace`
- `AuditTraceRecord`
- `AuditTraceError`

## Garanzie

- persistenza JSON versionata `0.1`;
- append singolo e multiplo;
- sequenza globale monotona;
- catena SHA-256;
- verifica automatica al caricamento;
- filtraggio per sessione;
- scrittura atomica con `fsync` e `os.replace`.

## Limiti

Non sono introdotte firme digitali, ancoraggio esterno, storage WORM o coordinamento inter-processo specifico del ledger. La catena è tamper-evident, non tamper-proof.

## Dipendenze

- `models.AuditEvent`
- filesystem locale
- standard library Python
