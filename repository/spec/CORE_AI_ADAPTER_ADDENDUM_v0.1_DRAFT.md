# CORE AI ADAPTER ADDENDUM

**Versione:** 0.1 Draft  
**Stato:** vincolante come integrazione documentale, non implementabile

## 1. Scopo

Integrare `CORE_SPEC_v0.1_DRAFT.md` con le dipendenze introdotte da `AI_ADAPTER_SPEC_v0.1_DRAFT.md`.

## 2. CORE coinvolti

### CORE-001

- riceve dall'AI Adapter input, contesto disponibile, identificatori e capacità dichiarate;
- non presume capacità non dichiarate;
- registra il sistema AI sorgente e i limiti dell'adapter.

### CORE-002

- riceve da CORE-001 il contenuto preservando il collegamento con l'input dell'AI ospite;
- prepara il trasferimento verso AET e AIL senza alterazioni semantiche silenziose.

### CORE-005

- valida esclusivamente i passaggi osservabili;
- distingue validazione completa, parziale e non verificabile;
- registra quando un limite deriva dall'AI Adapter o dalla piattaforma ospite.

### CORE-007

- coordina il ciclo AI Adapter ↔ moduli CORE;
- gestisce i richiami di validazione nei punti accessibili;
- mantiene la dichiarazione delle capacità e dei limiti durante l'intero ciclo.

### CORE-008

- restituisce all'AI Adapter il risultato e il relativo stato di validazione;
- dichiara esiti parziali, riserve e limiti di osservabilità;
- non presenta come validato ciò che non è stato verificato.

## 3. Vincoli

- L'AI Adapter non è un modulo CORE.
- I CORE rimangono interni a KYVERNEX.
- L'adapter non può sostituire CORE-005.
- Nessun limite della piattaforma può essere occultato.
- Ogni passaggio deve rispettare CCU, Meta-Modello e Validation Protocol.

## 4. TODO

- interfacce formali tra adapter e CORE-001/CORE-008;
- eventi di coordinamento di CORE-007;
- schema delle capacità;
- gestione di timeout, retry e streaming;
- test di conformità.