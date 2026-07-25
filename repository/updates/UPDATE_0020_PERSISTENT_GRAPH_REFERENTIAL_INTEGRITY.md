# UPDATE_0020 — Persistent Graph and Referential Integrity

## Stato
DRAFT IMPLEMENTED — execution verification pending.

## Obiettivo
Rendere persistente il grafo delle relazioni cognitive e impedire la creazione o il caricamento di relazioni che puntano a oggetti non presenti nella memoria della stessa sessione.

## Componenti introdotti

- `JsonCognitiveGraph`
- `GraphPersistenceFormatError`
- `ReferentialIntegrityError`

## Formato

Il grafo usa un documento JSON versionato:

```json
{
  "format_version": "0.1",
  "sessions": {}
}
```

Ogni relazione conserva:

- `relation_id`
- `source_object_id`
- `target_object_id`
- `relation_type`
- `metadata`

## Regole di integrità

Prima di registrare una relazione, entrambi gli estremi devono esistere nella `SessionMemory` associata e nella stessa sessione.

Errori espliciti:

- `SOURCE_OBJECT_NOT_FOUND`
- `TARGET_OBJECT_NOT_FOUND`
- `GRAPH_JSON_NON_VALIDO`
- `GRAPH_FORMAT_VERSION_NON_SUPPORTATA`
- `GRAPH_RELATION_DATA_NON_VALIDI`

Il caricamento rifiuta anche relazioni persistite divenute orfane.

## Persistenza

La scrittura usa un file temporaneo nella stessa directory, flush, `fsync` e sostituzione atomica tramite `os.replace`.

La cancellazione di una sessione viene resa persistente.

## Integrazione

`JsonCognitiveGraph` è compatibile con il parametro `graph` di `KyvernexOrchestrator`:

```python
memory = JsonSessionMemory("data/memory.json")
engine = KyvernexEngine(memory=memory)
graph = JsonCognitiveGraph("data/graph.json", memory=memory)
orchestrator = KyvernexOrchestrator(EchoAdapter(), engine=engine, graph=graph)
```

## Test aggiunti

- riapertura e recupero delle relazioni;
- rifiuto di estremi inesistenti;
- cancellazione persistente;
- rifiuto di JSON corrotto;
- rifiuto di versione incompatibile;
- rifiuto di relazioni orfane durante il caricamento.

## Limitazioni

- nessun lock tra processi differenti;
- nessuna migrazione automatica del formato;
- nessuna cancellazione coordinata oggetto-relazioni;
- test presenti ma non dichiarati superati finché non eseguiti indipendentemente o tramite CI osservabile.
