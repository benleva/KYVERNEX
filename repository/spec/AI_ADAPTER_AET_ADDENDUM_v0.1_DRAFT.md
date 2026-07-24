# AI ADAPTER / AET ADDENDUM v0.1 DRAFT

## Scopo

Formalizzare il confine tra AI Adapter e AET.

## Regola consolidata

L'AI Adapter gestisce la comunicazione con l'AI ospite o con la piattaforma esterna. AET riceve da CORE-001 il contenuto acquisito e lo prepara per AIL.

## Responsabilità dell'AI Adapter

- ricevere e restituire dati alla piattaforma ospite;
- dichiarare capacità e limiti di osservabilità;
- preservare metadati della sessione e della sorgente;
- inoltrare l'input a CORE-001 senza reinterpretarlo silenziosamente.

## Responsabilità di AET

- preservare il contenuto originale;
- normalizzare senza alterare il significato;
- classificare secondo il Meta-Modello quando possibile;
- dichiarare ambiguità e incompletezza;
- produrre una rappresentazione candidata ad AIL.

## Confine

L'AI Adapter non svolge classificazione cognitiva normativa. AET non gestisce direttamente protocolli specifici della piattaforma ospite.

## Stato

Draft. API, messaggi e serializzazione restano TODO.
