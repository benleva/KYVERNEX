# UPDATE 0004 — COGNITIVE METAMODEL

**Stato:** applicato  
**Ambito:** Matrice ARGUS / KYVERNEX  
**Tipo di modifica:** strutturale e documentale

## 1. Decisione

È introdotto il file `repository/spec/METAMODEL_SPEC_v0.1_DRAFT.md` come registro strutturale delle categorie cognitive già consolidate nel progetto.

Il Meta-Modello non aggiunge una nuova funzione eseguibile a KYVERNEX. Organizza in un vocabolario comune gli oggetti già presenti nella documentazione, affinché AET, AIL, CCU, CORE, memoria, validazione ed errori utilizzino le medesime categorie.

## 2. Categorie registrate

- Entità Cognitiva;
- Dato;
- Fatto;
- Ipotesi;
- Deduzione;
- Opinione;
- Regola;
- Assioma;
- Meta-Regola;
- Relazione;
- Trasformazione;
- Risultato;
- Fonte o Origine;
- Stato Cognitivo;
- Validazione;
- Errore.

Le categorie sono registrate in forma Draft. Gli schemi, le cardinalità e la serializzazione restano da definire.

## 3. Nuova regola di governance

Nessuna nuova categoria cognitiva potrà essere considerata consolidata senza:

1. registrazione nel Meta-Modello;
2. motivazione in un file UPDATE;
3. analisi delle interdipendenze;
4. aggiornamento dei documenti coinvolti;
5. versione e verifica di coerenza.

## 4. Interdipendenze aggiornate

- `repository/spec/AIL_SPEC_v0.1_DRAFT.md` → versione 0.2 Draft;
- `repository/spec/MEMORY_ARCHITECTURE_v0.1_DRAFT.md` → versione 0.2 Draft;
- `repository/spec/CORE_SPEC_v0.1_DRAFT.md` → versione 0.4 Draft;
- `repository/spec/CCU_SPEC_v0.1_DRAFT.md` → versione 0.3 Draft.

## 5. Vincoli

Il Meta-Modello non definisce ancora:

- schema eseguibile;
- grammatica AIL;
- criteri probatori definitivi;
- tassonomia completa degli errori;
- algoritmo di inferenza;
- API.

Tali elementi rimangono Draft o TODO e non devono essere trattati come implementati.
