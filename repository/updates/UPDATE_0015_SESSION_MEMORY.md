# UPDATE 0015 — SESSION MEMORY

## Stato
IMPLEMENTATO_NEL_REFERENCE_PROTOTYPE

## Obiettivo
Introdurre una memoria minima process-local capace di conservare oggetti cognitivi senza contaminazione tra sessioni.

## File creati
- `src/kyvernex/memory.py`
- `tests/test_memory.py`

## File aggiornati
- `src/kyvernex/core.py`
- `src/kyvernex/__init__.py`
- `tests/test_reference_prototype.py`

## Funzioni introdotte
- archivio isolato per `session_id`;
- memorizzazione e recupero tramite `object_id`;
- copie difensive in scrittura e lettura;
- rifiuto dei duplicati nella stessa sessione;
- possibilità di usare lo stesso identificatore in sessioni differenti;
- conteggio, elenco e cancellazione selettiva della memoria di sessione;
- evento Audit Trace `MEMORY/OGGETTO_MEMORIZZATO`;
- accesso controllato alla memoria tramite `KyvernexEngine.memory`.

## Pipeline aggiornata
`CORE-001 -> AET -> RULE_ENGINE -> CORE-005 -> MEMORY -> CORE-008`

## Limitazioni dichiarate
- memoria volatile e limitata al processo;
- nessuna persistenza su disco o database;
- nessuna scadenza automatica;
- nessuna cifratura;
- nessuna politica di capacità o espulsione;
- nessuna conformità Alpha dichiarata;
- i nuovi test non sono dichiarati superati finché non esiste un'esecuzione CI verificabile.

## Dipendenze
La specifica definitiva della memoria dovrà essere allineata con Audit Trace, Versioning Policy, Conformance e futura gestione della persistenza.
