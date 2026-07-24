# UPDATE 0002 - VALIDATION PROTOCOL

Data: 2026-07-25
Stato: applicato
Progetto: Matrice ARGUS / KYVERNEX

## Decisione

È stata introdotta la specifica preliminare del protocollo di validazione continua di KYVERNEX.

## Nuovo file

- `repository/spec/VALIDATION_PROTOCOL_v0.1_DRAFT.md`

## Contenuto consolidato

Il protocollo stabilisce che KYVERNEX deve:

- validare input, trasformazioni, passaggi intermedi accessibili e risultati;
- applicare controlli ripetuti lungo la pipeline;
- usare CORE-005 come modulo di validazione continua;
- usare CORE-007 per coordinare i richiami di validazione;
- produrre un record di validazione tracciabile;
- dichiarare esplicitamente i passaggi non osservabili;
- impedire il consolidamento di risultati non validati;
- collegare anomalie ed errori alla traccia di audit.

## Interdipendenze aggiornate

- `repository/spec/CORE_SPEC_v0.1_DRAFT.md`
- `repository/spec/ERROR_MODEL_v0.1_DRAFT.md`

## Interdipendenze future

- `repository/spec/AUDIT_TRACE_SPEC_v0.1_DRAFT.md`
- `repository/spec/AI_ADAPTER_SPEC_v0.1_DRAFT.md`
- schema AIL dei record di validazione;
- schema CCU degli esiti.

## Regola di continuità

Ogni futura modifica al protocollo deve aggiornare anche i file interdipendenti e generare un nuovo documento nella cartella `repository/updates/`.