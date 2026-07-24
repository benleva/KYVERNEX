# UPDATE 0005 — AI ADAPTER

**Stato:** applicato  
**Ambito:** Matrice ARGUS / KYVERNEX  
**Tipo di modifica:** architetturale e documentale

## 1. Decisione

È introdotto il file `repository/spec/AI_ADAPTER_SPEC_v0.1_DRAFT.md` come specifica preliminare del livello di integrazione tra KYVERNEX e i sistemi AI ospiti.

L'AI Adapter non costituisce un nuovo kernel e non sostituisce AET, AIL o i moduli CORE. È il confine tecnico che consente a KYVERNEX di ricevere input, dichiarare capacità e limiti della piattaforma, applicare controllo e validazione continua sui passaggi osservabili e restituire esiti tracciabili.

## 2. Elementi consolidati

- KYVERNEX rimane l'unico motore operativo.
- L'AI ospite mantiene il proprio motore di inferenza.
- L'integrazione deve rispettare ARGUS, CCU e Meta-Modello.
- Le capacità non dichiarate non possono essere presunte.
- I passaggi non osservabili devono essere dichiarati.
- La validazione parziale non può essere presentata come completa.
- Ogni scambio deve preservare origine, integrità, tracciabilità e versione.

## 3. Flusso registrato

`AI ospite → AI Adapter → CORE-001 → AET → AIL → CORE → Validazione continua → CORE-008 → AI Adapter → AI ospite`

## 4. Interdipendenze

Sono coinvolti:

- `repository/README.md`;
- `repository/spec/CORE_SPEC_v0.1_DRAFT.md`;
- `repository/spec/CCU_SPEC_v0.1_DRAFT.md`;
- futura `AET_SPEC`;
- `VALIDATION_PROTOCOL_v0.1_DRAFT.md`;
- `ERROR_MODEL_v0.1_DRAFT.md`;
- futura `AUDIT_TRACE_SPEC`;
- futura `PLUGIN_API_SPEC`.

Per evitare modifiche invasive ai documenti principali ancora in evoluzione, le nuove dipendenze operative verso CORE e CCU sono registrate anche tramite addendum dedicati.

## 5. File creati o aggiornati

- creato `repository/spec/AI_ADAPTER_SPEC_v0.1_DRAFT.md`;
- creato `repository/spec/CORE_AI_ADAPTER_ADDENDUM_v0.1_DRAFT.md`;
- creato `repository/spec/CCU_AI_ADAPTER_ADDENDUM_v0.1_DRAFT.md`;
- aggiornato `repository/README.md`.

## 6. Limiti

Non sono ancora definiti:

- API;
- schema serializzabile;
- adapter specifici per singola piattaforma;
- autenticazione e autorizzazione;
- streaming;
- timeout e retry;
- requisiti prestazionali;
- test multipiattaforma.

Tali elementi restano Draft o TODO e non devono essere trattati come implementati.