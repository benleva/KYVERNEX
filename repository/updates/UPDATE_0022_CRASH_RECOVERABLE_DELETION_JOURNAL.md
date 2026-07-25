# UPDATE_0022 — Crash-Recoverable Deletion Journal

## Stato

Implementazione proposta per il Reference Prototype 0.1. Test presenti ma non ancora verificati tramite esecuzione locale o CI.

## Obiettivo

Ridurre il rischio di incoerenza tra memoria cognitiva e grafo persistente quando il processo si interrompe durante una cancellazione coordinata.

## Nuovi componenti

- `DurableDeletionCoordinator`
- `DeletionJournalState`
- `DeletionJournalError`
- `RecoveryResult`

## Strategia

Prima della cancellazione viene scritto atomicamente un journal JSON versionato contenente:

- identificatore transazione;
- sessione;
- oggetto da eliminare;
- politica di cancellazione;
- stato della transazione;
- relazioni coinvolte.

Il journal usa scrittura temporanea, `fsync` e sostituzione atomica.

## Recupero

Al riavvio:

1. se l'oggetto esiste ancora, KYVERNEX interpreta la transazione come non completata e ripristina le relazioni mancanti;
2. se l'oggetto non esiste più, KYVERNEX completa la cancellazione eliminando eventuali relazioni residue;
3. il journal viene rimosso solo dopo la riconciliazione.

## Pipeline

```text
PREPARE JOURNAL
→ DELETE GRAPH RELATIONS
→ DELETE MEMORY OBJECT
→ MARK MEMORY_APPLIED
→ REMOVE JOURNAL
```

## Garanzia

L'incremento introduce recuperabilità deterministica dopo crash per una singola cancellazione coordinata. Non costituisce una transazione ACID generale e non supporta più transazioni concorrenti nello stesso file journal.

## File

Creati:

- `src/kyvernex/durable_deletion.py`
- `tests/test_durable_deletion.py`
- `repository/updates/UPDATE_0022_CRASH_RECOVERABLE_DELETION_JOURNAL.md`

Aggiornato:

- `src/kyvernex/__init__.py`

## Verifica

I test coprono:

- cancellazione completata e rimozione del journal;
- recupero con rollback delle relazioni;
- recupero con completamento della cancellazione;
- rifiuto di journal corrotto.

Al momento della creazione di questo aggiornamento, l'esecuzione dei test non è stata confermata.
