# CORE SPECIFICATION

Versione: 0.2 Draft
Stato: incompleto e aggiornabile
Progetto: Matrice ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Questo documento organizza la specifica preliminare dei moduli CORE della Matrice ARGUS. Riporta esclusivamente le responsabilità già consolidate e separa chiaramente le parti ancora da definire.

KYVERNEX è l'unico motore operativo del progetto: kernel cognitivo e plugin integrabile nelle principali AI per l'applicazione delle regole ARGUS, il controllo continuo e la validazione continua.

## 2. Principi vincolanti

Ogni modulo CORE deve rispettare:

- integrità delle informazioni;
- tracciabilità delle trasformazioni;
- separazione tra dati, regole, inferenze e risultati;
- modularità;
- compatibilità con AIL e CCU;
- verificabilità;
- evoluzione controllata e versionata;
- continuità del controllo durante l'intero ciclo di elaborazione dell'AI ospite.

## 3. Moduli consolidati

### CORE-001 — Acquisizione

Responsabilità consolidata:

Gestione dell'acquisizione delle informazioni, comprese quelle provenienti dall'AI ospite o dal suo ambiente di integrazione.

Da definire:

- formati di input ammessi;
- interfaccia di ingresso;
- adattatori per le diverse AI;
- controlli iniziali;
- gestione degli input incompleti o corrotti;
- output verso CORE-002.

### CORE-002 — Traduzione

Responsabilità consolidata:

Traduzione nella rappresentazione cognitiva comune.

Da definire:

- interfaccia con AET;
- formato AIL prodotto;
- gestione delle ambiguità;
- conservazione del contenuto originale;
- condizioni di errore.

### CORE-003 — Relazioni

Responsabilità consolidata:

Organizzazione e gestione delle relazioni tra le informazioni.

Da definire:

- struttura delle entità;
- struttura delle relazioni;
- identificatori;
- gestione dei conflitti;
- dipendenze dall'operatore Λ.

### CORE-004 — Elaborazione

Responsabilità consolidata:

Applicazione delle regole di elaborazione del kernel e dei vincoli ARGUS durante l'attività dell'AI ospite.

Da definire:

- ordine di applicazione delle regole;
- gestione delle dipendenze;
- uso degli operatori formali;
- condizioni di arresto;
- registrazione della traccia logica;
- punti di intercettazione dell'elaborazione dell'AI ospite.

### CORE-005 — Validazione continua

Responsabilità consolidata:

Verifica continua della coerenza e della validità di input, trasformazioni, passaggi intermedi e risultati.

Da definire:

- criteri di validazione;
- frequenza e punti di controllo;
- livelli di esito;
- differenza tra errore e avviso;
- condizioni di blocco, correzione o prosecuzione;
- report di validazione;
- dipendenze dall'operatore V.

### CORE-006 — Memoria

Responsabilità consolidata:

Gestione della memoria e della persistenza delle informazioni.

Da definire:

- tipi di memoria;
- durata;
- consolidamento;
- recupero;
- cancellazione;
- provenienza;
- conflitti;
- dipendenze dall'operatore μ.

### CORE-007 — Coordinamento

Responsabilità consolidata:

Coordinamento dei processi cognitivi, delle inferenze, dei moduli interni e dell'interazione con l'AI ospite.

Da definire:

- pianificazione dei passaggi;
- orchestrazione dei moduli;
- concorrenza;
- priorità;
- gestione dei blocchi;
- criterio di completamento;
- ciclo di controllo continuo.

### CORE-008 — Restituzione

Responsabilità consolidata:

Restituzione dei risultati nel formato richiesto mantenendo tracciabilità e integrità, insieme all'esito della validazione quando previsto.

Da definire:

- formati di output;
- interfaccia di restituzione;
- ricostruzione linguistica;
- allegati di tracciabilità;
- gestione degli esiti parziali o non validati;
- modalità di restituzione verso l'AI ospite o l'utente finale.

## 4. Sequenza operativa consolidata

CORE-001 → CORE-002 → CORE-003 → CORE-004 → CORE-005 → CORE-006 / CORE-007 → CORE-008

La sequenza rappresenta il flusso minimo ricavato dalla Pipeline del Kernel. CORE-005 può essere richiamato ripetutamente durante il ciclo, poiché la validazione è continua. Le condizioni di salto, ripetizione o ritorno non sono ancora formalizzate.

## 5. Contratto minimo di ogni modulo

Ogni modulo CORE dovrà in futuro dichiarare almeno:

- identificatore;
- versione;
- responsabilità;
- input;
- output;
- dipendenze;
- invarianti;
- errori;
- eventi tracciati;
- test di accettazione;
- punti di integrazione con l'AI ospite, quando applicabili.

Questi campi sono richiesti ma non ancora compilati in modo definitivo.

## 6. Conformità

Un modulo CORE è conforme solo se:

- non altera dati senza traccia;
- usa rappresentazioni compatibili con AIL;
- rispetta il CCU;
- espone responsabilità chiare e non sovrapposte;
- produce risultati verificabili;
- registra versione e modifiche;
- non elude il controllo continuo previsto da KYVERNEX.

## 7. Integrazione plugin

KYVERNEX deve poter essere caricato, richiamato o utilizzato come livello di integrazione da sistemi AI differenti. I moduli CORE restano interni a KYVERNEX e non costituiscono plugin separati.

Restano da definire:

- API comuni;
- adattatori specifici per piattaforma;
- capacità minime richieste all'AI ospite;
- modalità sincrone e asincrone;
- autorizzazioni e isolamento;
- comportamento in caso di indisponibilità di una funzione dell'AI ospite.

## 8. Parti mancanti

Prima del passaggio da Draft ad Alpha occorre definire:

1. interfacce di ogni modulo;
2. input e output formali;
3. dipendenze;
4. errori;
5. invarianti;
6. test di accettazione;
7. ordine operativo completo;
8. regole di recupero;
9. compatibilità tra versioni;
10. protocollo di integrazione con le AI;
11. protocollo di validazione continua.

## 9. Stato del documento

Questo file non costituisce ancora una specifica implementabile. Costituisce la mappa ufficiale delle responsabilità CORE già consolidate e delle parti mancanti da sviluppare progressivamente.

Aggiornamento architetturale di riferimento: `repository/updates/UPDATE_0001_KYVERNEX_PLUGIN_ARCHITECTURE.md`.