# CORE METAMODEL ADDENDUM v0.1 DRAFT

## Scopo

Integrare `CORE_SPEC_v0.1_DRAFT.md` con le dipendenze introdotte da `METAMODEL_SPEC_v0.1_DRAFT.md`, senza riscrivere o sostituire la specifica CORE principale.

## Regola generale

Tutti i moduli CORE devono ricevere, produrre, trasformare, validare o conservare oggetti compatibili con il Meta-Modello Cognitivo ARGUS.

## Impatto sui moduli

### CORE-001

Deve preservare il contenuto originale e predisporre i riferimenti necessari alla futura classificazione dell'Entità Cognitiva.

### CORE-002

Deve produrre una rappresentazione AIL che dichiari la categoria cognitiva quando determinabile e mantenga l'incertezza quando non determinabile.

### CORE-003

Deve organizzare Entità Cognitive e Relazioni secondo categorie e vincoli registrati nel Meta-Modello.

### CORE-004

Deve mantenere distinti Dati, Fatti, Ipotesi, Deduzioni, Opinioni, Regole e Risultati durante l'elaborazione.

### CORE-005

Deve validare anche la coerenza tra oggetto, categoria dichiarata, origine, trasformazioni, stato ed esito.

### CORE-006

Deve conservare la categoria cognitiva, la provenienza, le trasformazioni e gli esiti di validazione associati all'oggetto.

### CORE-007

Deve impedire che un modulo introduca categorie cognitive non registrate come consolidate senza l'iter previsto dalla governance.

### CORE-008

Deve preservare o rendere esplicita, quando pertinente, la distinzione tra Fatto, Ipotesi, Deduzione e Opinione nella restituzione.

## Parti ancora da integrare nella specifica CORE principale

- schema formale degli input e output per categoria;
- invarianti applicabili a ogni modulo;
- errori di classificazione;
- regole di propagazione delle categorie;
- test di conformità al Meta-Modello.

## Stato

Il presente addendum è vincolante come dipendenza Draft fino all'integrazione nella prossima revisione completa di CORE_SPEC.
