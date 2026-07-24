# ERROR_MODEL v0.2 DRAFT

Stato: DRAFT

## Scopo

Definire il modello preliminare degli errori della Matrice ARGUS e del kernel-plugin KYVERNEX, senza introdurre comportamenti non ancora consolidati.

## Principi consolidati applicabili

- Ogni elaborazione deve preservare integrità, tracciabilità e verificabilità.
- Dati, regole, inferenze e risultati devono restare distinti.
- Ogni risultato deve poter essere ricostruito.
- Le trasformazioni non possono alterare i dati originali senza tracciamento.
- Il kernel deve operare in modo coerente e riproducibile a parità di dati e condizioni.
- Ogni modulo deve rispettare il Contratto Cognitivo Universale (CCU).
- Ogni anomalia rilevata durante la validazione continua deve restare collegata al relativo record di validazione.

## Funzione del modello di errore

Il modello di errore deve consentire al sistema di:

- rilevare una condizione non conforme;
- identificare il punto della pipeline in cui si è verificata;
- preservare il dato originale;
- registrare il percorso logico precedente all'errore;
- impedire che un risultato non validato venga consolidato;
- produrre una segnalazione verificabile;
- ricevere e classificare anomalie provenienti da CORE-005;
- restituire a KYVERNEX informazioni utili alla decisione di prosecuzione, riserva, sospensione o blocco.

## Categorie preliminari

Le seguenti categorie derivano dalle lacune già individuate nella documentazione e restano da formalizzare:

- input incompleto;
- input ambiguo;
- rappresentazione AIL non valida;
- violazione del CCU;
- incompatibilità tra moduli;
- trasformazione non tracciabile;
- risultato non verificabile;
- incoerenza rispetto ad assiomi, regole o meta-regole;
- errore di memoria o persistenza;
- errore durante bootstrap, elaborazione, validazione o restituzione;
- passaggio dell'AI ospite non osservabile;
- validazione parziale o impossibile.

Queste categorie non costituiscono ancora una tassonomia definitiva.

## Stati correlati ancora mancanti

La documentazione consolidata definisce solo gli stati positivi:

- Acquisito;
- Normalizzato;
- Elaborato;
- Validato;
- Consolidato.

Restano da definire gli stati negativi o di eccezione, tra cui:

- Rifiutato;
- Ambiguo;
- Incompleto;
- Contraddittorio;
- Non verificabile;
- Errore;
- Sospeso;
- Obsoleto.

Tali stati sono elencati come necessità progettuali e non sono ancora normativi.

## Struttura minima di una segnalazione

Una futura segnalazione di errore dovrà poter contenere almeno:

- identificatore univoco;
- identificatore della validazione collegata;
- fase della pipeline;
- modulo coinvolto;
- dato o oggetto interessato;
- regola o vincolo violato;
- stato cognitivo precedente;
- esito della validazione;
- decisione operativa conseguente;
- riferimento alla traccia di elaborazione;
- versione del modulo o della specifica coinvolta.

La sintassi concreta resta da definire in AIL, CCU e AUDIT_TRACE_SPEC.

## Relazione con VALIDATION_PROTOCOL

Il protocollo di validazione continua:

1. rileva l'anomalia;
2. produce un esito esplicito;
3. trasmette l'anomalia al modello degli errori;
4. collega errore e record di validazione;
5. impedisce il consolidamento come valido finché non avviene una nuova validazione conforme.

Il modello degli errori non sostituisce il protocollo di validazione: ne riceve e organizza gli esiti negativi o incerti.

## Vincoli

Un errore non deve:

- cancellare o sovrascrivere il dato originale;
- essere trasformato in risultato valido senza una nuova validazione;
- interrompere la tracciabilità;
- nascondere la regola o il modulo che lo ha generato;
- essere consolidato come informazione verificata;
- essere omesso quando deriva da un passaggio non osservabile dell'AI ospite.

## Dipendenze

Il modello di errore dipende da:

- AIL_SPEC;
- CCU_SPEC;
- CORE_SPEC;
- MEMORY_ARCHITECTURE;
- VALIDATION_PROTOCOL;
- futura AUDIT_TRACE_SPEC;
- definizione degli Stati Cognitivi negativi.

## Parti non ancora definite

TODO:

- codici di errore;
- livelli di severità;
- differenza tra warning, errore bloccante e violazione costituzionale;
- comportamento di recupero;
- retry e rollback;
- propagazione tra moduli;
- formato AIL degli errori;
- relazione tra errore e stato cognitivo;
- politiche di logging e audit;
- test di conformità.

## Requisiti per lo stato ALPHA

Il documento potrà passare da DRAFT ad ALPHA quando saranno definiti:

- tassonomia normativa degli errori;
- stati negativi ed eccezioni;
- struttura serializzabile;
- regole di propagazione;
- livelli di severità;
- comportamento dei CORE coinvolti;
- integrazione eseguibile con VALIDATION_PROTOCOL;
- test minimi di validazione.

Aggiornamento di riferimento: `repository/updates/UPDATE_0002_VALIDATION_PROTOCOL.md`.