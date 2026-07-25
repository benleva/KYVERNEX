# UPDATE_0021 — Coordinated Transactional Deletion

## Stato
IMPLEMENTATO, NON ANCORA VERIFICATO DA CI.

## Obiettivo
Impedire che la rimozione di un oggetto cognitivo lasci relazioni orfane nel grafo KYVERNEX.

## Componenti aggiunti
- `src/kyvernex/deletion.py`
- `tests/test_coordinated_deletion.py`

## Componenti aggiornati
- `src/kyvernex/memory.py`
- `src/kyvernex/persistence.py`
- `src/kyvernex/graph.py`
- `src/kyvernex/graph_persistence.py`
- `src/kyvernex/__init__.py`

## Politiche
### RESTRICT
Blocca la cancellazione quando l'oggetto possiede relazioni cognitive entranti o uscenti.

Errore:
`OBJECT_HAS_COGNITIVE_RELATIONS`

### CASCADE
Rimuove prima tutte le relazioni collegate e successivamente l'oggetto dalla memoria.

## Rollback
Se la rimozione dell'oggetto fallisce dopo la rimozione delle relazioni, il coordinatore tenta di reinserire tutte le relazioni eliminate.

Questa è una garanzia transazionale a livello di processo. Non viene dichiarata atomicità assoluta in caso di arresto del sistema tra la scrittura del file del grafo e quella del file di memoria.

## Eventi audit
- `CANCELLAZIONE_PREPARATA`
- `RELAZIONI_COLLEGATE_RIMOSSE`
- `OGGETTO_COGNITIVO_RIMOSSO`
- `CANCELLAZIONE_COMPLETATA`

## Test previsti
- blocco RESTRICT su oggetto referenziato;
- cancellazione CASCADE di oggetto e relazioni;
- cancellazione RESTRICT di oggetto isolato;
- errore esplicito per oggetto inesistente.

## Limitazioni
- nessun lock distribuito tra processi;
- nessun journal transazionale su disco;
- nessuna atomicità multi-file resistente a crash;
- i test sono presenti nel repository ma non risultano ancora eseguiti con successo da una pipeline verificata.
