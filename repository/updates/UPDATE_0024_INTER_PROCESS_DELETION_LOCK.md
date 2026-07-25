# UPDATE_0024 — INTER-PROCESS DELETION LOCK

## Stato

IMPLEMENTATO, NON ANCORA VERIFICATO DA ESECUZIONE TEST/CI.

## Obiettivo

Superare il limite del solo lock locale introdotto in UPDATE_0023, coordinando più processi KYVERNEX che condividono la stessa directory dei journal.

## File creati

- `src/kyvernex/process_lock.py`
- `src/kyvernex/process_safe_journal.py`
- `tests/test_process_safe_deletion.py`
- `repository/specifications/INTER_PROCESS_DELETION_LOCK_SPEC_v0.1_DRAFT.md`

## File aggiornati

- `src/kyvernex/__init__.py`

## Componenti

- `InterProcessFileLock`
- `ProcessLockError`
- `ProcessSafeMultiTransactionDeletionCoordinator`

## Flusso

```text
PROCESSO A / PROCESSO B
        ↓
LOCK FILE CONDIVISO
        ↓
SEZIONE CRITICA ESCLUSIVA
        ↓
JOURNAL + GRAFO + MEMORIA
        ↓
RILASCIO LOCK
```

## Operazioni protette

- `delete`
- `recover_all`
- `pending_transactions`

## Compatibilità

- POSIX: `fcntl.flock`
- Windows: `msvcrt.locking`

## Garanzie dichiarate

Il coordinamento vale esclusivamente tra processi cooperanti sullo stesso host e filesystem, configurati con la stessa directory di journal.

## Limiti residui

- nessun lock distribuito;
- nessuna protezione contro processi non cooperanti;
- test presenti ma non dichiarati superati;
- CI non confermata.
