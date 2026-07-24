# VALIDATION PROTOCOL v0.1 DRAFT

Stato: DRAFT
Progetto: Matrice ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Definire il protocollo preliminare con cui KYVERNEX controlla e valida in modo continuo input, trasformazioni, passaggi intermedi e risultati prodotti durante l'attività dell'AI ospite.

Il documento consolida esclusivamente principi e responsabilità già presenti nel repository. Le parti non ancora definite sono indicate come TODO.

## 2. Principi vincolanti

Ogni validazione deve rispettare:

- coerenza con Principi Fondamentali, Assiomi, Regole del Kernel e Meta-Regole;
- integrità dei dati originali;
- tracciabilità delle trasformazioni;
- separazione tra dati, regole, inferenze e risultati;
- verificabilità e auditabilità;
- riproducibilità a parità di dati e condizioni;
- compatibilità con CCU e AIL;
- continuità del controllo durante l'intero ciclo operativo dell'AI ospite.

## 3. Ambito della validazione continua

KYVERNEX deve poter validare almeno:

1. input acquisiti;
2. normalizzazione e traduzione AET;
3. rappresentazioni AIL;
4. relazioni tra entità;
5. applicazione delle regole;
6. inferenze e trasformazioni;
7. accessi e scritture in memoria;
8. passaggi intermedi prodotti dall'AI ospite quando accessibili;
9. risultato finale;
10. restituzione verso AI ospite o utente finale.

L'accessibilità concreta dei passaggi intermedi dipende dalle capacità offerte dalla piattaforma AI ospite ed è ancora da formalizzare.

## 4. Responsabilità

### CORE-005

CORE-005 è il modulo responsabile della validazione continua.

Deve:

- ricevere l'oggetto o il passaggio da validare;
- identificare regole e vincoli applicabili;
- verificare coerenza, integrità e tracciabilità;
- produrre un esito esplicito;
- collegare l'esito alla traccia di elaborazione;
- segnalare violazioni al modello degli errori;
- impedire il consolidamento di risultati non validati.

### CORE-007

CORE-007 coordina i richiami a CORE-005 lungo la pipeline e nell'interazione con l'AI ospite.

### Operatore V

L'operatore V rappresenta la funzione formale di validazione. Firma, sintassi e comportamento eseguibile restano definiti in `OPERATORS_SPEC` come TODO.

## 5. Punti minimi di controllo

La validazione deve essere invocabile almeno:

- dopo l'acquisizione;
- dopo la normalizzazione;
- prima e dopo una trasformazione rilevante;
- dopo un'inferenza;
- prima del consolidamento in memoria;
- prima della restituzione del risultato.

KYVERNEX può richiamare CORE-005 più volte sullo stesso ciclo. Frequenza, trigger e condizioni di campionamento restano da definire.

## 6. Sequenza minima

1. Ricezione dell'oggetto da validare.
2. Identificazione di origine, stato, modulo e versione.
3. Recupero delle regole applicabili.
4. Verifica di integrità.
5. Verifica di tracciabilità.
6. Verifica di coerenza.
7. Verifica di completezza e compatibilità.
8. Produzione dell'esito.
9. Registrazione nella traccia di audit.
10. Decisione di prosecuzione, riserva, sospensione o blocco.

## 7. Esiti preliminari

Il protocollo utilizza le categorie già presenti nel CCU:

- completato;
- completato con riserva;
- non verificabile;
- incompleto;
- incompatibile;
- rifiutato;
- errore.

Per la validazione continua tali categorie corrispondono, in forma preliminare, a:

- VALIDATO;
- VALIDATO_CON_RISERVA;
- NON_VERIFICABILE;
- INCOMPLETO;
- INCOMPATIBILE;
- RIFIUTATO;
- ERRORE.

La codifica definitiva non è ancora normativa.

## 8. Decisioni operative preliminari

In base all'esito, KYVERNEX deve poter rappresentare almeno una delle seguenti decisioni:

- prosecuzione;
- prosecuzione con riserva;
- richiesta di integrazione;
- nuova validazione;
- sospensione;
- blocco.

Le condizioni precise per correzione automatica, rollback o retry non sono ancora consolidate e restano affidate a ERROR_MODEL e alle future regole di recupero.

## 9. Struttura minima del record di validazione

Ogni record di validazione dovrà poter contenere almeno:

- identificatore della validazione;
- identificatore dell'operazione;
- oggetto validato;
- modulo sorgente;
- punto della pipeline;
- stato cognitivo precedente;
- regole applicate;
- controlli eseguiti;
- esito;
- decisione operativa;
- anomalie rilevate;
- riferimento alla traccia precedente;
- versione di KYVERNEX e delle specifiche applicate.

La forma serializzabile definitiva resta da definire in AIL, CCU e AUDIT_TRACE_SPEC.

## 10. Validazione nell'AI ospite

Quando integrato come plugin, KYVERNEX deve applicare il protocollo in modo indipendente dal modello AI ospite, entro i limiti delle interfacce disponibili.

Il protocollo deve distinguere:

- contenuto ricevuto dall'AI ospite;
- trasformazioni eseguite da KYVERNEX;
- contenuto restituito all'AI ospite;
- passaggi non osservabili o non disponibili.

L'assenza di accesso a un passaggio non può essere nascosta: deve produrre una dichiarazione di non verificabilità o validazione parziale.

## 11. Relazione con il modello degli errori

Ogni violazione o anomalia rilevata deve:

- essere classificata secondo ERROR_MODEL;
- preservare il dato originale;
- indicare regola, modulo e fase coinvolti;
- impedire che un risultato non validato venga consolidato come valido;
- restare collegata al record di validazione.

## 12. Dipendenze

Il protocollo dipende da:

- Principi Fondamentali;
- Assiomi della Matrice;
- Regole Fondamentali del Kernel;
- Meta-Regole;
- CCU_SPEC;
- AIL_SPEC;
- CORE_SPEC;
- OPERATORS_SPEC;
- ERROR_MODEL;
- MEMORY_ARCHITECTURE;
- futura AUDIT_TRACE_SPEC;
- futura AI_ADAPTER_SPEC.

## 13. TODO

Restano da formalizzare:

- algoritmo completo di validazione;
- priorità tra regole;
- metriche e soglie;
- livelli di severità;
- trigger e frequenza dei controlli;
- condizioni precise di blocco o prosecuzione;
- firma e serializzazione dei record;
- comportamento in modalità sincrona e asincrona;
- validazione concorrente;
- idempotenza;
- timeout;
- retry, rollback e recupero;
- test di conformità;
- capacità minime richieste all'AI ospite.

## 14. Requisiti per lo stato ALPHA

Il documento potrà passare da DRAFT ad ALPHA quando saranno definiti:

1. schema serializzabile del record di validazione;
2. algoritmo minimo eseguibile;
3. tassonomia degli esiti e delle severità;
4. regole di blocco, riserva e prosecuzione;
5. integrazione con ERROR_MODEL;
6. almeno un adattatore AI dimostrativo;
7. casi di test per ogni punto minimo di controllo;
8. formato della traccia di audit.

## 15. Stato del documento

Questo file costituisce la specifica preliminare ufficiale del protocollo di validazione continua di KYVERNEX. Non è ancora una specifica implementabile completa.