# UPDATE_0023 — MULTI-TRANSACTION DELETION JOURNAL

## Stato

IMPLEMENTATO NEL REPOSITORY, NON ANCORA VERIFICATO DA ESECUZIONE TEST O CI.

## Obiettivo

Rimuovere il limite del journal singolo introdotto da UPDATE_0022 e consentire la presenza simultanea di più cancellazioni recuperabili.

## File creati

- `src/kyvernex/transaction_journal.py`
- `tests/test_multi_transaction_deletion.py`
- `repository/specifications/MULTI_TRANSACTION_DELETION_JOURNAL_SPEC_v0.1_DRAFT.md`
- `repository/updates/UPDATE_0023_MULTI_TRANSACTION_DELETION_JOURNAL.md`

## File aggiornati

- `src/kyvernex/__init__.py`

## Componenti

- `MultiTransactionDeletionCoordinator`
- `RecoveryBatch`

## Modello operativo

```text
DELETE REQUEST
→ PROCESS-LOCAL TRANSACTION LOCK
→ UNIQUE TRANSACTION ID
→ DEDICATED JOURNAL FILE
→ COORDINATED GRAPH/MEMORY DELETION
→ JOURNAL REMOVAL
```

## Recupero batch

```text
JOURNAL DIRECTORY
→ ORDERED SCAN
→ VALIDATION
→ ROLLBACK OR COMMIT COMPLETION
→ PER-JOURNAL REMOVAL
```

La modalità `continue_on_error=True` conserva i journal non validi e continua il recupero di quelli validi.

## Garanzie

- una transazione non sovrascrive il journal di un'altra;
- corrispondenza obbligatoria tra nome file e `transaction_id`;
- scrittura atomica del singolo journal;
- recupero deterministico basato sullo stato visibile della memoria;
- serializzazione delle cancellazioni concorrenti nel singolo processo;
- ispezione delle transazioni pendenti.

## Limitazioni dichiarate

- nessun lock distribuito tra processi;
- nessuna transazione ACID generale;
- nessuna atomicità assoluta tra memoria, grafo e directory journal;
- i test aggiunti non risultano eseguiti in questa sessione;
- lo stato CI deve essere verificato separatamente.

## Compatibilità

`DurableDeletionCoordinator` resta disponibile. Le nuove integrazioni dovrebbero usare `MultiTransactionDeletionCoordinator`.
