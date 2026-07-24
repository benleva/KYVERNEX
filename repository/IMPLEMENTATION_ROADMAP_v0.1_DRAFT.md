# KYVERNEX IMPLEMENTATION ROADMAP

Versione: 0.2 Draft
Stato: incompleto e aggiornabile
Progetto: Matrice ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Questo documento definisce l'ordine preliminare con cui trasformare le specifiche del repository in un primo prototipo verificabile di KYVERNEX.

La roadmap non introduce nuove funzioni normative. Organizza esclusivamente le dipendenze già consolidate e marca come TODO le decisioni tecniche non ancora approvate.

## 2. Principi vincolanti

L'implementazione deve:

- rispettare ARGUS, CCU, Meta-Regole e Governance;
- mantenere distinti dati, regole, inferenze e risultati;
- preservare origine e tracciabilità;
- non presentare come implementato ciò che è ancora Draft o TODO;
- mantenere KYVERNEX come unico motore operativo e plugin integrabile;
- dichiarare i limiti dell'AI ospite e i passaggi non osservabili;
- produrre esiti di validazione e riferimenti di audit;
- produrre evidenze sufficienti per la valutazione di conformità.

## 3. Fase 0 — Consolidamento delle specifiche

Prima del codice eseguibile devono essere rese coerenti almeno le seguenti specifiche:

1. Meta-Modello;
2. AIL;
3. AET;
4. CCU;
5. CORE;
6. Validation Protocol;
7. Error Model;
8. Memory Architecture;
9. AI Adapter;
10. Plugin API;
11. Audit Trace;
12. Dependency Graph;
13. Versioning Policy;
14. Conformance Specification.

Criterio di uscita:

- dipendenze dichiarate;
- nessuna contraddizione nota non registrata;
- tutti i campi mancanti indicati come TODO;
- almeno un flusso end-to-end descritto;
- verifica Level 0 eseguita con esito e limitazioni registrati.

## 4. Fase 1 — Modello dati minimo

Obiettivo:

creare una rappresentazione minima e serializzabile degli oggetti cognitivi già registrati nel Meta-Modello.

Componenti:

- identificatore;
- categoria cognitiva;
- contenuto originale;
- origine;
- stato cognitivo;
- trasformazioni;
- regole applicate;
- esito di validazione;
- collegamento alla traccia di audit.

TODO:

- formato definitivo;
- tipi;
- schema;
- validatore;
- compatibilità tra versioni.

Criterio di conformità previsto: Level 1 Draft.

## 5. Fase 2 — AET minimo

Obiettivo:

trasformare un input esterno in una rappresentazione candidata AIL senza aggiungere informazioni non presenti.

Funzioni minime:

- acquisizione dell'input;
- preservazione dell'originale;
- registrazione dell'origine;
- classificazione preliminare;
- dichiarazione di ambiguità o incompletezza;
- produzione dell'oggetto candidato AIL.

Criterio di uscita:

- input e output formalizzati;
- test su input valido, ambiguo e incompleto;
- nessuna perdita silenziosa dell'origine.

## 6. Fase 3 — Validatore minimo

Obiettivo:

implementare il primo ciclo di controllo continuo di KYVERNEX.

Controlli minimi:

- presenza dei campi obbligatori;
- integrità dell'origine;
- tracciabilità delle trasformazioni;
- compatibilità con il Meta-Modello;
- coerenza dello stato cognitivo;
- presenza di limiti dichiarati.

Esiti minimi:

- VALIDATO;
- VALIDATO_CON_RISERVA;
- NON_VERIFICABILE;
- INCOMPLETO;
- INCOMPATIBILE;
- RIFIUTATO;
- ERRORE.

Criterio di conformità previsto: Level 3 Draft.

## 7. Fase 4 — Audit Trace minimo

Obiettivo:

registrare le operazioni osservabili svolte da KYVERNEX.

Record minimo:

- identificatore della sessione;
- identificatore dell'operazione;
- timestamp;
- componente coinvolto;
- input e output referenziati;
- regola applicata;
- esito della validazione;
- limite o passaggio non osservabile;
- versione delle specifiche coinvolte.

La traccia non deve dichiarare di rappresentare il ragionamento interno non accessibile dell'AI ospite.

Criterio di conformità previsto: Level 4 Draft.

## 8. Fase 5 — CORE minimo

Ordine preliminare di implementazione:

1. CORE-001 Acquisizione;
2. CORE-002 Traduzione;
3. CORE-005 Validazione continua;
4. CORE-007 Coordinamento;
5. CORE-008 Restituzione;
6. CORE-006 Memoria;
7. CORE-003 Relazioni;
8. CORE-004 Elaborazione.

L'ordine privilegia un primo percorso verificabile prima dell'introduzione di elaborazioni complesse.

## 9. Fase 6 — Plugin API e AI Adapter

Obiettivo:

consentire a una AI ospite o a un simulatore di inviare richieste a KYVERNEX e ricevere:

- risultato;
- esito di validazione;
- limiti dichiarati;
- riferimento alla traccia di audit.

TODO:

- tecnologia di trasporto;
- autenticazione;
- autorizzazioni;
- streaming;
- timeout;
- retry;
- isolamento delle sessioni;
- adattatore della prima piattaforma.

Criterio di conformità previsto: Level 5 Draft.

## 10. Fase 7 — Memoria minima

Obiettivo:

persistenza e recupero di oggetti cognitivi con origine, stato, versione e validazione.

Vincolo:

nessun contenuto può essere consolidato come valido senza un esito conforme di CORE-005.

## 11. Primo scenario end-to-end

Scenario minimo richiesto:

1. una AI ospite o un simulatore invia un input;
2. Plugin API e AI Adapter registrano capacità e limiti;
3. CORE-001 acquisisce l'input;
4. AET preserva e normalizza;
5. AIL rappresenta l'oggetto;
6. CORE-005 valida nei punti disponibili;
7. Audit Trace registra le operazioni KYVERNEX;
8. CORE-008 restituisce risultato, esito e limiti;
9. la risposta torna all'AI ospite;
10. viene prodotto un rapporto di conformità Draft del flusso.

## 12. Test minimi

Il prototipo dovrà includere almeno:

- test di preservazione dell'input;
- test di origine mancante;
- test di ambiguità;
- test di campo AIL obbligatorio assente;
- test di trasformazione non tracciata;
- test di passaggio non osservabile;
- test di risultato non verificabile;
- test di audit ricostruibile;
- test di isolamento tra due sessioni;
- test di attribuzione corretta degli esiti di conformità.

## 13. Criteri per il prototipo Alpha

Il prototipo potrà essere indicato come Alpha solo quando:

- esiste un flusso end-to-end eseguibile;
- ogni passaggio osservabile genera una traccia;
- i limiti della piattaforma ospite sono dichiarati;
- gli esiti negativi non vengono presentati come validi;
- i test minimi sono ripetibili;
- versione del codice e versioni delle specifiche sono collegate;
- README e Dependency Graph riflettono l'implementazione reale;
- è disponibile una valutazione di conformità Draft almeno fino al Level 4;
- le limitazioni residue sono dichiarate.

## 14. Fuori ambito della presente versione

Restano fuori ambito:

- scelta definitiva del linguaggio di programmazione;
- scelta definitiva del protocollo di rete;
- supporto simultaneo a tutte le principali AI;
- motore di inferenza completo;
- knowledge graph definitivo;
- certificazione crittografica;
- prestazioni di produzione;
- conformità normativa esterna;
- certificazione commerciale o legale.

## 15. Regola di avanzamento

Ogni fase può iniziare solo quando le dipendenze necessarie sono sufficientemente definite oppure quando le parti mancanti sono esplicitamente isolate come TODO e non alterano il comportamento previsto.

Ogni implementazione deve generare:

1. codice versionato;
2. test;
3. aggiornamento tecnico;
4. aggiornamento delle dipendenze;
5. riferimento alle specifiche applicate;
6. evidenze per la valutazione di conformità.

## 16. Registro modifiche

| Versione | Stato | Modifica |
|---|---|---|
| 0.1 | Draft | Prima roadmap di implementazione. |
| 0.2 | Draft | Inseriti i gate e le evidenze della Conformance Specification. |
