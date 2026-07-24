# UPDATE 0003 — REPOSITORY GOVERNANCE

Data: 2026-07-25
Stato: applicato
Ambito: governo del repository MATRICE ARGUS / KYVERNEX

## Decisione

È istituita una governance ufficiale del repository.

Ogni nuova funzione, specifica, concetto tecnico o modifica interdipendente deve:

- generare o aggiornare il relativo file tecnico;
- generare un file `UPDATE_xxxx`;
- dichiarare le dipendenze;
- aggiornare i file direttamente coinvolti;
- indicare versione e stato;
- mantenere separati elementi consolidati, proposte e TODO.

## Regola sul Meta-Modello

Nessun nuovo oggetto cognitivo può essere introdotto come requisito consolidato senza registrazione nel futuro `METAMODEL_SPEC`.

Fino alla sua creazione, i nuovi concetti devono essere marcati come `PROPOSTO`.

## File creato

- `repository/GOVERNANCE.md`

## File interdipendenti

- `repository/README.md`

## Compatibilità

La modifica non altera gli assiomi, il CCU o l'architettura KYVERNEX. Formalizza il metodo già adottato per aggiornamenti e dipendenze.

## Parti ancora mancanti

- schema automatico delle dipendenze;
- workflow di revisione;
- politica dei tag;
- procedura di rollback;
- criteri formali di approvazione.