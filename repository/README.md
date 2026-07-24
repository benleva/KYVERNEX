# MATRICE ARGUS — Repository incompleto

Archivio di continuità del progetto MATRICE ARGUS / KYVERNEX.

Versione: 1.0 Alpha
Stato: incompleto e aggiornabile
Autore del progetto: Andrea Pernarcic

## Architettura consolidata

ARGUS definisce la Costituzione Cognitiva Universale: principi, assiomi, meta-regole, CCU, linguaggio e vincoli.

KYVERNEX è l'unico motore operativo del progetto. Svolge contemporaneamente il ruolo di kernel cognitivo, plugin integrabile nelle principali AI, livello di applicazione delle regole ARGUS e sistema di controllo e validazione continua.

Non esiste un componente separato denominato KYRNEXEN.

## Livello di integrazione AI

L'AI Adapter è il confine tecnico tra KYVERNEX e ciascuna AI ospite. Non è un secondo kernel e non sostituisce AET, AIL o i moduli CORE.

Flusso di riferimento:

`AI ospite → AI Adapter → CORE-001 → AET → AIL → CORE → Validazione continua → CORE-008 → AI Adapter → AI ospite`

L'AI Adapter deve dichiarare capacità, limiti e passaggi non osservabili. Una validazione parziale non può essere presentata come completa.

Specifica di riferimento: `repository/spec/AI_ADAPTER_SPEC_v0.1_DRAFT.md`.

## Documentazione

La documentazione consolidata dei 22 PDF è archiviata in tre parti Markdown. La cartella `spec` contiene le specifiche progressive e la cartella `updates` registra ogni decisione o modifica con impatto architetturale o documentale.

## Governance

Il file `repository/GOVERNANCE.md` contiene le regole vincolanti per l'evoluzione del progetto.

Ogni nuova funzione, testo tecnico o modifica interdipendente deve:

1. generare o aggiornare il relativo file tecnico;
2. generare un file di aggiornamento in `repository/updates`;
3. dichiarare le dipendenze coinvolte;
4. aggiornare tutti i documenti direttamente coinvolti;
5. mantenere tracciabilità, motivazione, versione e stato;
6. distinguere elementi consolidati, proposte progettuali e TODO.

Nessun nuovo oggetto cognitivo può essere trattato come consolidato senza registrazione nel `METAMODEL_SPEC`. Fino ad allora deve essere indicato come `PROPOSTO`.

Aggiornamenti di riferimento:

- `repository/updates/UPDATE_0003_REPOSITORY_GOVERNANCE.md`;
- `repository/updates/UPDATE_0005_AI_ADAPTER.md`.