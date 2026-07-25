# UPDATE_0019 — COGNITIVE RELATION GRAPH

## Stato
Implementato nel Reference Prototype 0.1. Test automatici aggiunti ma non ancora dichiarati superati finché non risulta disponibile un'esecuzione verificabile della pipeline CI.

## Obiettivo
Introdurre un grafo diretto e isolato per sessione capace di rappresentare relazioni esplicite tra oggetti cognitivi KYVERNEX.

## Componenti introdotti
- `src/kyvernex/graph.py`
- `tests/test_cognitive_graph.py`

## Componenti aggiornati
- `src/kyvernex/response_governance.py`
- `src/kyvernex/orchestrator.py`
- `src/kyvernex/__init__.py`

## Modello
`CognitiveRelation` collega due `CognitiveObject` mediante:
- `session_id`
- `source_object_id`
- `target_object_id`
- `relation_type`
- `relation_id`
- `metadata`

Tipi iniziali:
- `DERIVA_DA`
- `TRASFORMA`
- `DIPENDE_DA`
- `SUPPORTA`
- `CONTRADDICE`
- `RIFERISCE`

## Vincoli
- isolamento completo tra sessioni;
- estremi obbligatori;
- auto-relazioni rifiutate;
- duplicati identici rifiutati nella stessa sessione;
- query entranti, uscenti e bidirezionali;
- nessuna modifica retroattiva degli oggetti cognitivi.

## Integrazione con le risposte AI
Il `ResponseGovernor` registra automaticamente una relazione:

`RISPOSTA_AI --DERIVA_DA--> INPUT_ORIGINALE`

La relazione include adapter e modello nei metadati e produce l'evento Audit Trace:

`RELAZIONE_COGNITIVA_REGISTRATA`

## Limiti dichiarati
- grafo volatile e process-local;
- nessuna persistenza JSON delle relazioni;
- nessuna ricerca transitiva;
- nessun rilevamento automatico di contraddizioni;
- nessuna politica di cancellazione coordinata con la memoria;
- nessun controllo che gli identificatori puntino a oggetti già presenti in memoria.

## Passo successivo raccomandato
Aggiungere persistenza locale versionata del grafo e validazione referenziale contro la memoria della sessione.
