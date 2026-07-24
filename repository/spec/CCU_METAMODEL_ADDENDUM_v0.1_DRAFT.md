# CCU METAMODEL ADDENDUM v0.1 DRAFT

## Scopo

Integrare `CCU_SPEC_v0.1_DRAFT.md` con i vincoli introdotti da `METAMODEL_SPEC_v0.1_DRAFT.md`, senza sostituire la specifica CCU principale.

## Obblighi aggiuntivi

Ogni scambio cognitivo conforme al CCU deve, quando l'informazione è disponibile:

- identificare l'Entità Cognitiva trattata;
- dichiarare la categoria cognitiva;
- preservare la Fonte o Origine;
- mantenere il collegamento con Trasformazioni e Regole applicate;
- dichiarare lo Stato Cognitivo;
- collegare gli esiti di Validazione;
- mantenere distinti Fatto, Ipotesi, Deduzione e Opinione.

## Violazioni aggiuntive

Costituiscono violazioni del contratto:

- assegnazione silenziosa di una categoria cognitiva non giustificata;
- perdita della categoria durante uno scambio tra moduli;
- fusione non dichiarata tra categorie differenti;
- rimozione del collegamento con origine o trasformazioni;
- introduzione di una nuova categoria come consolidata senza aggiornamento del Meta-Modello e relativo file UPDATE.

## Dipendenza

Il CCU deve considerare `METAMODEL_SPEC_v0.1_DRAFT.md` come riferimento strutturale per gli oggetti scambiati.

## Parti da integrare nella prossima revisione CCU

- codifica della categoria nel messaggio CCU;
- schema degli identificatori;
- regole di compatibilità tra versioni del Meta-Modello;
- gestione delle categorie sconosciute o non determinabili;
- test di conformità.

## Stato

Il presente addendum è vincolante come dipendenza Draft fino all'integrazione nella prossima revisione completa di CCU_SPEC.
