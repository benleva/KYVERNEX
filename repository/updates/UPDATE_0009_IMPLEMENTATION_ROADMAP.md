# UPDATE 0009 — IMPLEMENTATION ROADMAP

Stato: applicato
Ambito: Matrice ARGUS / KYVERNEX
Tipo di modifica: pianificazione tecnica e documentale

## 1. Decisione

È introdotto il file `repository/IMPLEMENTATION_ROADMAP_v0.1_DRAFT.md` come sequenza ufficiale preliminare per trasformare le specifiche in un primo prototipo verificabile di KYVERNEX.

## 2. Vincoli

La roadmap:

- non rende implementato ciò che è ancora Draft;
- non sceglie ancora linguaggio di programmazione o protocollo di rete;
- mantiene KYVERNEX come unico motore operativo e plugin integrabile;
- richiede tracciabilità, validazione continua e audit;
- impone che limiti e passaggi non osservabili dell'AI ospite siano dichiarati.

## 3. Sequenza introdotta

1. consolidamento delle specifiche;
2. modello dati minimo;
3. AET minimo;
4. validatore minimo;
5. Audit Trace minimo;
6. CORE minimo;
7. Plugin API e AI Adapter;
8. memoria minima;
9. scenario end-to-end;
10. test e criteri Alpha.

## 4. Interdipendenze

La roadmap dipende da:

- `repository/spec/DEPENDENCY_GRAPH_SPEC_v0.1_DRAFT.md`;
- Meta-Modello;
- AIL;
- AET;
- CCU;
- CORE;
- Validation Protocol;
- Error Model;
- Memory Architecture;
- AI Adapter;
- Plugin API;
- Audit Trace;
- futura Versioning Policy.

## 5. Parti non consolidate

Restano TODO:

- linguaggio di programmazione;
- framework;
- protocollo di trasporto;
- prima AI ospite supportata;
- infrastruttura di persistenza;
- criteri quantitativi di prestazione;
- calendario di sviluppo.

## 6. File aggiornati

- `repository/README.md` viene aggiornato per includere la roadmap come riferimento ufficiale.
