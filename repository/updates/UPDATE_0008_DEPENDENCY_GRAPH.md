# UPDATE 0008 — DEPENDENCY GRAPH

**Stato:** applicato  
**Ambito:** Matrice ARGUS / KYVERNEX  
**Tipo di modifica:** strutturale e documentale

## 1. Decisione

È introdotto il file `repository/spec/DEPENDENCY_GRAPH_SPEC_v0.1_DRAFT.md` come mappa ufficiale delle dipendenze del progetto.

## 2. Effetto

La nuova specifica:

- raccoglie le relazioni già consolidate;
- distingue dipendenze normative, strutturali, operative e di verifica;
- definisce il flusso complessivo tra AI ospite, Plugin API, AI Adapter, AET, AIL, CORE, validazione, memoria, audit ed errori;
- obbliga le future specifiche a dichiarare le proprie dipendenze;
- non introduce nuove funzioni eseguibili.

## 3. Interdipendenze

Sono direttamente coinvolti:

- `repository/README.md`;
- `repository/GOVERNANCE.md`;
- `repository/spec/PLUGIN_API_SPEC_v0.1_DRAFT.md`;
- `repository/spec/AI_ADAPTER_SPEC_v0.1_DRAFT.md`;
- `repository/spec/AET_SPEC_v0.1_DRAFT.md`;
- `repository/spec/AIL_SPEC_v0.1_DRAFT.md`;
- `repository/spec/CORE_SPEC_v0.1_DRAFT.md`;
- `repository/spec/VALIDATION_PROTOCOL_v0.1_DRAFT.md`;
- `repository/spec/ERROR_MODEL_v0.1_DRAFT.md`;
- `repository/spec/MEMORY_ARCHITECTURE_v0.1_DRAFT.md`;
- `repository/spec/METAMODEL_SPEC_v0.1_DRAFT.md`.

## 4. Regola applicata

Ogni nuova relazione o modifica di dipendenza dovrà:

1. essere motivata in un file UPDATE;
2. aggiornare la Dependency Graph;
3. indicare i file coinvolti;
4. evitare cicli non dichiarati;
5. mantenere versione, stato e tracciabilità.

## 5. Limiti

La mappa è ancora Draft. Non contiene ancora un formato machine-readable, controlli automatici o integrazione CI/CD.
