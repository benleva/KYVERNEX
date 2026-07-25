# MULTI-TRANSACTION DELETION JOURNAL SPEC v0.1 DRAFT

## 1. Scopo

Definire il journal durevole per cancellazioni cognitive concorrenti nel Reference Prototype 0.1 di KYVERNEX.

## 2. Principio

Ogni cancellazione coordinata MUST possedere un file journal indipendente. Due transazioni attive MUST NOT condividere o sovrascrivere lo stesso record durevole.

## 3. Identità

Ogni transazione MUST avere un `transaction_id` univoco. Il file MUST essere denominato:

```text
deletion-<transaction_id>.json
```

Il valore interno `transaction_id` MUST corrispondere al nome del file.

## 4. Formato

Versione corrente:

```text
0.2
```

Campi obbligatori:

- `format_version`
- `transaction_id`
- `state`
- `session_id`
- `object_id`
- `policy`
- `relations`

## 5. Stati

- `PREPARED`
- `GRAPH_APPLIED`
- `MEMORY_APPLIED`

La versione di riferimento può omettere la persistenza intermedia di `GRAPH_APPLIED`, ma MUST interpretare correttamente ogni stato valido durante il recupero.

## 6. Recupero

Per ogni journal pendente:

- se l'oggetto esiste ancora, KYVERNEX MUST ripristinare le relazioni mancanti;
- se l'oggetto non esiste, KYVERNEX MUST eliminare le relazioni residue;
- dopo un recupero riuscito, il journal MUST essere eliminato;
- un journal non valido MUST produrre un errore esplicito e MUST NOT essere eliminato automaticamente.

## 7. Concorrenza

La reference implementation MUST serializzare le mutazioni nel singolo processo tramite lock rientrante.

Non sono dichiarate:

- esclusione distribuita tra processi;
- transazioni ACID generali;
- atomicità multi-file assoluta contro guasti del filesystem.

## 8. Scrittura durevole

La scrittura MUST usare:

```text
file temporaneo -> flush -> fsync -> os.replace
```

## 9. Ispezione

L'implementazione SHOULD esporre:

- elenco delle transazioni pendenti;
- recupero batch;
- modalità `continue_on_error` con elenco dei journal falliti.

## 10. Compatibilità

`DurableDeletionCoordinator` con journal singolo resta disponibile per compatibilità. Le nuove integrazioni SHOULD preferire `MultiTransactionDeletionCoordinator`.
