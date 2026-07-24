# UPDATE 0001 — KYVERNEX come kernel-plugin unico

Versione: 0.1 Draft
Stato: consolidato come decisione architetturale
Data: 2026-07-25
Autore del progetto: Andrea Pernarcic

## 1. Decisione

KYVERNEX mantiene il proprio nome e assorbe integralmente le funzioni di integrazione esterna precedentemente ipotizzate come componente separato.

Non esiste un secondo prodotto o modulo denominato KYRNEXEN.

## 2. Ruolo definitivo

KYVERNEX è contemporaneamente:

- kernel cognitivo della Matrice ARGUS;
- motore operativo delle regole ARGUS;
- livello di integrazione caricabile, richiamabile o utilizzabile dalle principali AI;
- sistema di controllo continuo delle elaborazioni;
- sistema di validazione continua degli input, dei passaggi intermedi e degli output;
- coordinatore di AET, AIL, CORE, memoria, inferenza e restituzione;
- produttore della traccia di audit necessaria alla ricostruzione del processo.

## 3. Relazione con ARGUS

ARGUS definisce principi, assiomi, meta-regole, contratto cognitivo, linguaggio e vincoli.

KYVERNEX applica tali elementi durante l'interazione con un sistema AI ospite.

Schema concettuale:

AI ospite → KYVERNEX → regole e rappresentazioni ARGUS → validazione continua → output conforme o esito dichiarato

## 4. Vincoli

KYVERNEX deve:

- non sostituire silenziosamente il contenuto prodotto dall'AI ospite;
- tracciare ogni trasformazione applicata;
- distinguere dati, regole, inferenze e risultati;
- dichiarare errori, incompatibilità e risultati non verificabili;
- mantenere compatibilità con CCU e AIL;
- consentire integrazioni differenti senza alterare i principi fondamentali di ARGUS.

## 5. Impatto documentale

Sono interdipendenti e devono recepire questa decisione:

- repository/README.md;
- repository/spec/CORE_SPEC_v0.1_DRAFT.md;
- repository/spec/CCU_SPEC_v0.1_DRAFT.md;
- futura specifica di integrazione e plugin;
- futura specifica del protocollo di validazione continua;
- futura specifica delle API.

## 6. Parti ancora da definire

TODO:

- modalità di caricamento nei diversi sistemi AI;
- API e adattatori per ciascun ambiente;
- confini tra controllo preventivo, concomitante e successivo;
- comportamento in caso di mancata conformità;
- livelli di blocco, avviso e correzione;
- gestione delle capacità non disponibili nell'AI ospite;
- isolamento, sicurezza e autorizzazioni;
- test di conformità multipiattaforma.

## 7. Regola di continuità

Ogni nuova funzione, testo tecnico o modifica interdipendente deve generare un file di aggiornamento nella cartella `repository/updates` e deve aggiornare i documenti direttamente coinvolti.