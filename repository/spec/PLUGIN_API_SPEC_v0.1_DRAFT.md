# PLUGIN API SPECIFICATION

Versione: 0.1 Draft
Stato: incompleto e aggiornabile
Progetto: Matrice ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Definire il contratto logico di integrazione attraverso cui KYVERNEX può essere caricato, richiamato o utilizzato da sistemi AI differenti come unico motore operativo per l'applicazione delle regole ARGUS, il controllo continuo e la validazione continua.

La presente specifica non impone ancora una tecnologia di trasporto concreta. REST, gRPC, MCP, SDK nativi, estensioni o altri protocolli restano da definire.

## 2. Principi consolidati

La Plugin API deve:

- mantenere separati il motore dell'AI ospite e KYVERNEX;
- usare l'AI Adapter come confine tecnico di integrazione;
- preservare origine, identità e tracciabilità delle informazioni;
- rispettare CCU, AET, AIL, Meta-Modello e moduli CORE;
- consentire il controllo e la validazione continua nei punti tecnicamente accessibili;
- dichiarare capacità mancanti, limiti e passaggi non osservabili;
- impedire che una validazione parziale venga presentata come completa;
- produrre esiti espliciti e registrabili.

## 3. Attori

### 3.1 AI ospite

Sistema esterno che produce o elabora contenuti e richiede l'intervento di KYVERNEX.

### 3.2 AI Adapter

Componente di confine che traduce le capacità della piattaforma ospite nel contratto logico della Plugin API.

### 3.3 KYVERNEX

Unico motore operativo del progetto. Coordina AET, AIL, CORE, memoria, validazione, errori e restituzione.

## 4. Ciclo logico minimo

1. L'AI ospite o il suo ambiente invia una richiesta all'AI Adapter.
2. L'AI Adapter dichiara identità della piattaforma, capacità disponibili e limiti.
3. CORE-001 acquisisce la richiesta.
4. AET normalizza l'input e prepara la rappresentazione per AIL.
5. KYVERNEX coordina i moduli CORE.
6. CORE-005 esegue i controlli previsti nei punti accessibili.
7. CORE-008 prepara il risultato e il relativo stato di validazione.
8. L'AI Adapter restituisce il risultato all'AI ospite.

## 5. Operazioni logiche minime

La futura API dovrà supportare almeno:

- inizializzazione della sessione di integrazione;
- dichiarazione delle capacità dell'AI ospite;
- invio di un input o di un evento;
- richiesta di validazione;
- restituzione di un esito;
- segnalazione di limiti o passaggi non osservabili;
- chiusura della sessione;
- recupero dei riferimenti di audit quando disponibili.

I nomi tecnici, i metodi, gli endpoint e i payload non sono ancora consolidati.

## 6. Informazioni minime di una richiesta

Ogni richiesta dovrà poter contenere almeno:

- identificatore dell'operazione;
- identificatore della sessione;
- sistema sorgente;
- versione dell'Adapter;
- contenuto originale o suo riferimento;
- contesto disponibile;
- capacità dichiarate;
- limiti dichiarati;
- punto del ciclo in cui avviene la richiesta;
- eventuali riferimenti a passaggi precedenti.

## 7. Informazioni minime di una risposta

Ogni risposta dovrà poter contenere almeno:

- identificatore dell'operazione;
- esito dell'elaborazione;
- esito della validazione;
- decisione operativa;
- contenuto restituito;
- limiti o riserve;
- errori rilevati;
- riferimento alla traccia di elaborazione o audit, quando disponibile;
- versioni dei componenti coinvolti.

## 8. Esiti preliminari

La Plugin API deve poter trasportare almeno gli esiti già consolidati:

- VALIDATO;
- VALIDATO_CON_RISERVA;
- NON_VERIFICABILE;
- INCOMPLETO;
- INCOMPATIBILE;
- RIFIUTATO;
- ERRORE.

La codifica definitiva resta dipendente da CCU, AIL, ERROR_MODEL e VALIDATION_PROTOCOL.

## 9. Gestione dei limiti dell'AI ospite

Quando una piattaforma non consente l'accesso a passaggi intermedi, strumenti, memoria o eventi necessari al controllo completo:

- l'AI Adapter deve dichiararlo;
- KYVERNEX deve limitare il perimetro della validazione;
- il risultato deve riportare la natura parziale del controllo;
- nessuna parte non osservata può essere trattata come verificata.

## 10. Sicurezza e isolamento

Restano da definire:

- autenticazione;
- autorizzazione;
- isolamento tra sessioni;
- protezione dei dati;
- gestione dei segreti;
- rate limit;
- timeout;
- retry;
- idempotenza;
- revoca dell'accesso.

## 11. Dipendenze

- `AI_ADAPTER_SPEC_v0.1_DRAFT.md`
- `AET_SPEC_v0.1_DRAFT.md`
- `AIL_SPEC_v0.1_DRAFT.md`
- `CCU_SPEC_v0.1_DRAFT.md`
- `CORE_SPEC_v0.1_DRAFT.md`
- `VALIDATION_PROTOCOL_v0.1_DRAFT.md`
- `ERROR_MODEL_v0.1_DRAFT.md`
- `MEMORY_ARCHITECTURE_v0.1_DRAFT.md`
- `METAMODEL_SPEC_v0.1_DRAFT.md`

## 12. Parti ancora da definire

TODO:

- tecnologia o tecnologie di trasporto;
- schema formale delle richieste e delle risposte;
- versionamento del contratto API;
- handshake e capability negotiation;
- modalità sincrone, asincrone e streaming;
- gestione degli eventi;
- firma e integrità dei messaggi;
- codici di errore;
- compatibilità tra Adapter;
- test di conformità multipiattaforma;
- SDK e implementazione di riferimento.

## 13. Criteri per lo stato Alpha

La specifica potrà passare ad Alpha quando saranno definiti:

- schema serializzabile di richiesta e risposta;
- handshake minimo;
- capability negotiation;
- regole di compatibilità;
- gestione degli errori;
- almeno un Adapter di riferimento;
- test end-to-end con una AI ospite;
- collegamento operativo con validazione e audit.
