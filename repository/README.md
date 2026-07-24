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

La Plugin API definisce il contratto logico con cui una piattaforma AI può inizializzare una sessione, dichiarare capacità e limiti, inviare richieste, ricevere esiti di validazione e recuperare i riferimenti di audit disponibili. La tecnologia di trasporto concreta resta da definire.

Flusso di riferimento:

`AI ospite o sorgente esterna → Plugin API → AI Adapter → CORE-001 → AET → AIL → CORE KYVERNEX → Validazione continua → Memoria / Audit / Error Model → CORE-008 → AI Adapter → Plugin API → AI ospite`

L'AI Adapter deve dichiarare capacità, limiti e passaggi non osservabili. Una validazione parziale non può essere presentata come completa.

AET preserva l'input originale, ne registra origine e contesto, identifica le categorie cognitive già ammesse dal Meta-Modello, dichiara ambiguità e produce una rappresentazione candidata ad AIL senza inventare informazioni mancanti.

Specifiche di riferimento:

- `repository/spec/PLUGIN_API_SPEC_v0.1_DRAFT.md`;
- `repository/spec/AI_ADAPTER_SPEC_v0.1_DRAFT.md`;
- `repository/spec/AET_SPEC_v0.1_DRAFT.md`;
- `repository/spec/DEPENDENCY_GRAPH_SPEC_v0.1_DRAFT.md`.

## Mappa delle dipendenze

La Dependency Graph è il riferimento ufficiale delle relazioni normative, strutturali, operative e di verifica tra i componenti del progetto.

Ogni nuova specifica o modifica interdipendente deve dichiarare il proprio impatto sulla mappa e aggiornarla quando introduce, elimina o modifica una relazione.

## Roadmap di implementazione

Il file `repository/IMPLEMENTATION_ROADMAP_v0.1_DRAFT.md` definisce l'ordine preliminare per trasformare le specifiche in un primo prototipo verificabile.

La roadmap non dichiara ancora scelte definitive di linguaggio, framework, protocollo o piattaforma AI. Stabilisce invece le fasi minime: consolidamento delle specifiche, modello dati, AET, validazione, audit, CORE, Plugin API, AI Adapter, memoria, scenario end-to-end e test.

Nessuna fase può essere presentata come completata senza codice, test, aggiornamento tecnico e collegamento alle specifiche applicate.

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
6. distinguere elementi consolidati, proposte progettuali e TODO;
7. aggiornare la Dependency Graph quando cambia una relazione tra componenti;
8. aggiornare la Roadmap quando cambia l'ordine o il criterio di implementazione.

Nessun nuovo oggetto cognitivo può essere trattato come consolidato senza registrazione nel `METAMODEL_SPEC`. Fino ad allora deve essere indicato come `PROPOSTO`.

Aggiornamenti di riferimento:

- `repository/updates/UPDATE_0003_REPOSITORY_GOVERNANCE.md`;
- `repository/updates/UPDATE_0005_AI_ADAPTER.md`;
- `repository/updates/UPDATE_0006_AET_SPECIFICATION.md`;
- `repository/updates/UPDATE_0007_PLUGIN_API.md`;
- `repository/updates/UPDATE_0008_DEPENDENCY_GRAPH.md`;
- `repository/updates/UPDATE_0009_IMPLEMENTATION_ROADMAP.md`.
