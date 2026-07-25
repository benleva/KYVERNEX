# COGNITIVE CONFIDENCE PROPAGATION SPEC v0.1 DRAFT

## 1. Scopo

Definire un meccanismo deterministico e conservativo per stimare la confidenza di un oggetto cognitivo a partire dalla sua confidenza diretta e dalle relazioni presenti nel grafo KYVERNEX.

## 2. Input

Ogni oggetto può dichiarare `metadata.confidence` come numero compreso tra 0 e 1.

Quando il valore è assente viene applicata una confidenza predefinita configurabile. Il risultato deve riportare una riserva esplicita.

## 3. Relazioni considerate

- `SUPPORTS`: aumenta la confidenza del nodo destinazione.
- `DEPENDS_ON`: contribuisce come evidenza positiva.
- `CONTRADICTS`: riduce la confidenza del nodo destinazione.

Le altre relazioni non modificano il calcolo in questa versione.

## 4. Formula

La combinazione positiva usa il complemento del prodotto dei complementi:

`support = 1 - product(1 - score)`

La penalità delle contraddizioni usa:

`penalty = product(max(0, 1 - weight * contradiction_score))`

Il risultato finale è limitato all'intervallo `[0, 1]`:

`propagated = clamp(support * penalty)`

## 5. Proprietà obbligatorie

- determinismo;
- isolamento per sessione;
- rilevazione dei cicli;
- rifiuto dei valori non numerici;
- rifiuto dei valori fuori intervallo;
- tracciamento dei sostenitori e dei contraddittori;
- riserve esplicite per dati mancanti o contraddizioni.

## 6. Limitazioni

Il punteggio non dimostra la verità di un contenuto. Rappresenta soltanto una valutazione strutturale calcolata sulle informazioni e sulle relazioni disponibili.

La versione 0.1 non applica pesi diversi per fonte, categoria, età del dato o tipo di relazione positiva.
