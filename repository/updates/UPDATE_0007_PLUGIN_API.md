# UPDATE 0007 — PLUGIN API

Stato: applicato
Ambito: Matrice ARGUS / KYVERNEX
Tipo di modifica: strutturale e documentale

## 1. Decisione

È introdotto il file `repository/spec/PLUGIN_API_SPEC_v0.1_DRAFT.md` come contratto logico preliminare per l'integrazione di KYVERNEX con sistemi AI differenti.

## 2. Vincoli consolidati

- KYVERNEX resta l'unico motore operativo.
- L'AI Adapter resta il confine tecnico verso la piattaforma ospite.
- La Plugin API non sostituisce AET, AIL o CORE.
- La tecnologia di trasporto non è ancora consolidata.
- Ogni limite o passaggio non osservabile deve essere dichiarato.
- Una validazione parziale non può essere presentata come completa.

## 3. Dipendenze coinvolte

- AI Adapter
- AET
- AIL
- CCU
- CORE
- Validation Protocol
- Error Model
- Memory Architecture
- Meta-Modello

## 4. Parti non implementate

Restano Draft o TODO:

- schema serializzabile;
- endpoint e metodi;
- autenticazione e autorizzazione;
- capability negotiation;
- streaming;
- codici di errore;
- Adapter di riferimento;
- test end-to-end.

## 5. Regola di avanzamento

Ogni futura implementazione della Plugin API dovrà aggiornare questa specifica, creare un nuovo file UPDATE e revisionare tutte le dipendenze direttamente coinvolte.
