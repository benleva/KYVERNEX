# ERROR_MODEL v0.1 DRAFT

Stato: DRAFT

## Scopo

Definire il modello preliminare degli errori della Matrice ARGUS e del kernel KYVERNEX, senza introdurre comportamenti non ancora consolidati.

## Principi consolidati applicabili

- Ogni elaborazione deve preservare integrità, tracciabilità e verificabilità.
- Dati, regole, inferenze e risultati devono restare distinti.
- Ogni risultato deve poter essere ricostruito.
- Le trasformazioni non possono alterare i dati originali senza tracciamento.
- Il kernel deve operare in modo coerente e riproducibile a parità di dati e condizioni.
- Ogni modulo deve rispettare il Contratto Cognitivo Universale (CCU).

## Funzione del modello di errore

Il modello di errore deve consentire al sistema di:

- rilevare una condizione non conforme;
- identificare il punto della pipeline in cui si è verificata;
- preservare il dato originale;
- registrare il percorso logico precedente all'errore;
- impedire che un risultato non validato venga consolidato;
- produrre una segnalazione verificabile.

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
- errore durante bootstrap, elaborazione, validazione o restituzione.

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
- fase della pipeline;
- modulo coinvolto;
- dato o oggetto interessato;
- regola o vincolo violato;
- stato cognitivo precedente;
- esito della validazione;
- riferimento alla traccia di elaborazione;
- versione del modulo o della specifica coinvolta.

La sintassi concreta resta da definire in AIL e nel CCU.

## Vincoli

Un errore non deve:

- cancellare o sovrascrivere il dato originale;
- essere trasformato in risultato valido senza una nuova validazione;
- interrompere la tracciabilità;
- nascondere la regola o il modulo che lo ha generato;
- essere consolidato come informazione verificata.

## Dipendenze

Il modello di errore dipende da:

- AIL_SPEC;
- CCU_SPEC;
- CORE_SPEC;
- MEMORY_ARCHITECTURE;
- VALIDATION_PROTOCOL;
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
- test minimi di validazione.
