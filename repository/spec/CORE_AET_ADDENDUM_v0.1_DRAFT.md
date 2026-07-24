# CORE / AET ADDENDUM v0.1 DRAFT

## Scopo

Formalizzare le interdipendenze tra AET e i moduli CORE.

## CORE coinvolti

### CORE-001

Acquisisce l'input dall'AI Adapter o da altra sorgente autorizzata e lo consegna ad AET preservando contenuto, origine, contesto e metadati disponibili.

### CORE-002

Riceve l'output di AET e coordina la sua trasformazione nella rappresentazione interna AIL. Non può rimuovere ambiguità, riserve o limiti dichiarati da AET senza una trasformazione tracciata e una nuova validazione.

### CORE-005

Valida integrità, tracciabilità, classificazione dichiarata, compatibilità con il Meta-Modello e compatibilità dell'output AET con AIL.

### CORE-007

Coordina il passaggio CORE-001 → AET → CORE-002 → AIL e gestisce eventuali richieste di integrazione, sospensione o nuova validazione.

## Stato

Draft. Interfacce, trigger, errori, retry e test restano TODO.
