# AI ADAPTER SPECIFICATION

**Versione:** 0.1 Draft  
**Stato:** incompleto e aggiornabile  
**Progetto:** Matrice ARGUS / KYVERNEX  
**Autore del progetto:** Andrea Pernarcic

## 1. Scopo

Definire il livello di integrazione tra KYVERNEX e un sistema AI ospite, mantenendo separati il motore di inferenza dell'AI e il sistema di governo, controllo e validazione continua basato sulle regole ARGUS.

## 2. Principi consolidati

- KYVERNEX è l'unico motore operativo del progetto.
- KYVERNEX deve poter essere caricato, richiamato o utilizzato come plugin o livello di integrazione da sistemi AI differenti.
- L'AI ospite mantiene il proprio motore di inferenza.
- KYVERNEX applica i principi, gli assiomi, le meta-regole, il CCU e le regole ARGUS.
- KYVERNEX esegue controllo e validazione continua sui passaggi tecnicamente osservabili.
- KYVERNEX deve dichiarare quando una parte del processo dell'AI ospite non è osservabile.
- Ogni scambio deve preservare origine, integrità, tracciabilità e stato di validazione.
- L'integrazione deve rispettare il CCU e il Meta-Modello.

## 3. Ruolo dell'AI Adapter

L'AI Adapter costituisce il confine tecnico tra KYVERNEX e l'AI ospite. Non sostituisce AET, AIL o i moduli CORE e non costituisce un secondo kernel.

Deve poter:

- ricevere richieste, messaggi o eventi dall'AI ospite;
- identificare il sistema sorgente e il contesto disponibile;
- trasferire l'input verso CORE-001 e AET;
- ricevere esiti intermedi e finali da KYVERNEX;
- restituire all'AI ospite il risultato nel formato compatibile;
- allegare o rendere disponibile lo stato di validazione quando previsto;
- dichiarare capacità mancanti, passaggi non osservabili e limiti della piattaforma;
- preservare il collegamento tra input originale, trasformazioni, esiti e output.

## 4. Confini di responsabilità

### AI ospite

- genera o elabora contenuti attraverso il proprio motore;
- espone a KYVERNEX solo le informazioni consentite dalla piattaforma;
- non è considerata conforme per il solo fatto di essere collegata a KYVERNEX.

### AI Adapter

- traduce il protocollo della piattaforma in uno scambio interpretabile da KYVERNEX;
- non modifica silenziosamente il contenuto semantico;
- non dichiara osservabili passaggi che la piattaforma non espone;
- non sostituisce la validazione di CORE-005.

### KYVERNEX

- applica le regole ARGUS;
- coordina i moduli CORE;
- valida i passaggi accessibili;
- registra gli esiti e le limitazioni;
- restituisce una decisione o un risultato tracciabile.

## 5. Flusso minimo consolidato

`AI ospite → AI Adapter → CORE-001 → AET → AIL → CORE → Validazione continua → CORE-008 → AI Adapter → AI ospite`

Il flusso può contenere richiami ripetuti a CORE-005. Le condizioni precise di ritorno, retry, streaming e asincronia non sono ancora definite.

## 6. Scambio minimo

Ogni scambio tra AI Adapter e KYVERNEX deve poter contenere almeno:

- identificatore dell'operazione;
- identificatore della sessione o del contesto, quando disponibile;
- sistema AI sorgente;
- capacità dichiarate dall'adapter;
- contenuto originale o relativo riferimento;
- formato dell'input;
- stato cognitivo corrente;
- passaggio della pipeline;
- esito di validazione disponibile;
- limiti di osservabilità;
- collegamento con i passaggi precedenti;
- versione dell'adapter e delle specifiche applicate.

La sintassi e la serializzazione definitive restano da definire.

## 7. Capacità dell'adapter

Ogni adapter dovrà dichiarare esplicitamente se supporta:

- input testuale;
- output testuale;
- allegati o file;
- strumenti esterni;
- streaming;
- chiamate sincrone;
- chiamate asincrone;
- accesso ai passaggi intermedi;
- ricezione di eventi;
- blocco preventivo dell'output;
- correzione o richiesta di nuova elaborazione;
- restituzione della traccia di audit.

Le capacità non dichiarate non devono essere presunte.

## 8. Validazione e osservabilità

- KYVERNEX valida solo gli elementi effettivamente ricevuti o osservabili.
- Un passaggio non osservabile deve essere registrato come tale.
- La mancanza di osservabilità può produrre un esito di validazione parziale o non verificabile.
- L'adapter non può trasformare un esito parziale in validazione completa.
- Il risultato finale deve dichiarare le limitazioni rilevanti quando incidono sull'affidabilità dell'esito.

## 9. Errori preliminari

L'adapter deve poter segnalare almeno:

- piattaforma non supportata;
- capacità richiesta non disponibile;
- input non trasferibile;
- formato incompatibile;
- sessione o contesto non identificabile;
- timeout;
- perdita della connessione;
- risposta incompleta;
- passaggio non osservabile;
- violazione del CCU;
- errore restituito da KYVERNEX o dall'AI ospite.

La codifica degli errori dipende da `ERROR_MODEL` e non è ancora normativa.

## 10. Sicurezza e isolamento

Restano requisiti vincolanti, ma non ancora formalizzati:

- separazione tra sessioni;
- controllo delle autorizzazioni;
- minimizzazione dei dati trasferiti;
- protezione delle credenziali;
- tracciamento delle operazioni;
- gestione della revoca;
- comportamento in caso di adapter compromesso o non conforme.

## 11. Dipendenze

- `METAMODEL_SPEC_v0.1_DRAFT.md`;
- `CCU_SPEC_v0.1_DRAFT.md` e relativi addendum;
- `CORE_SPEC_v0.1_DRAFT.md` e relativi addendum;
- `VALIDATION_PROTOCOL_v0.1_DRAFT.md`;
- `ERROR_MODEL_v0.1_DRAFT.md`;
- `AIL_SPEC_v0.1_DRAFT.md`;
- futura `AET_SPEC`;
- futura `AUDIT_TRACE_SPEC`;
- futura `PLUGIN_API_SPEC`.

## 12. TODO

- protocollo comune di comunicazione;
- schema serializzabile degli scambi;
- API sincrone e asincrone;
- gestione dello streaming;
- gestione di timeout, retry e idempotenza;
- autenticazione e autorizzazione;
- isolamento dei contesti;
- adapter specifici per piattaforma;
- modello delle capacità;
- prestazioni e limiti;
- test multipiattaforma;
- comportamento di fallback;
- compatibilità tra versioni.

## 13. Criteri per lo stato ALPHA

Il documento potrà passare ad ALPHA quando saranno definiti e testabili:

1. contratto comune dell'adapter;
2. schema degli input e degli output;
3. modello delle capacità;
4. gestione degli errori;
5. protocollo di validazione parziale;
6. requisiti minimi di sicurezza;
7. almeno un adapter di riferimento;
8. test di conformità;
9. esempio completo AI ospite → KYVERNEX → AI ospite.

## 14. Stato del documento

Questa specifica definisce esclusivamente il perimetro e i requisiti già consolidati o necessari alla loro applicazione. Non costituisce ancora un'API implementabile.