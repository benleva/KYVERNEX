# UPDATE 0006 — AET SPECIFICATION

**Stato:** applicato  
**Ambito:** Matrice ARGUS / KYVERNEX  
**Tipo di modifica:** strutturale e documentale

## 1. Decisione

È introdotto il file `repository/spec/AET_SPEC_v0.1_DRAFT.md` come specifica preliminare dell'ARGUS Executive Translator.

AET è il livello che trasforma gli input acquisiti in una rappresentazione candidata ad AIL, preservando contenuto originale, origine, contesto, categorie cognitive, ambiguità e trasformazioni.

## 2. Vincoli consolidati

AET non può:

- inventare informazioni mancanti;
- trasformare ipotesi in fatti;
- eliminare origine o tracciabilità;
- dichiarare valida una traduzione incompleta o non verificabile;
- introdurre nuove categorie cognitive non registrate nel Meta-Modello.

## 3. Flusso aggiornato

`AI ospite o sorgente esterna → AI Adapter → CORE-001 → AET → AIL → CORE KYVERNEX`

## 4. Interdipendenze

Sono coinvolti:

- AI Adapter;
- AIL;
- Meta-Modello;
- CCU;
- CORE-001, CORE-002 e CORE-005;
- Protocollo di Validazione;
- Modello degli Errori.

## 5. Stato

La specifica resta Draft. Algoritmi, schema serializzabile, API, formati, confidenza e test sono ancora TODO.
