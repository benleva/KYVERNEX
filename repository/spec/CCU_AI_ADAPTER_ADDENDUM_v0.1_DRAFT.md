# CCU AI ADAPTER ADDENDUM

**Versione:** 0.1 Draft  
**Stato:** vincolante come integrazione documentale, non implementabile

## 1. Scopo

Integrare il Contratto Cognitivo Universale con le condizioni applicabili agli scambi tra AI ospite, AI Adapter e KYVERNEX.

## 2. Obblighi dell'AI Adapter

L'AI Adapter deve:

- identificare, quando possibile, sistema sorgente, sessione e versione;
- preservare il contenuto originale o il relativo riferimento;
- dichiarare capacità disponibili e capacità assenti;
- dichiarare passaggi non osservabili;
- non alterare silenziosamente il significato dell'input o dell'output;
- conservare il collegamento tra richiesta, trasformazioni, validazioni e risposta;
- trasmettere gli esiti di validazione senza aumentarne arbitrariamente il livello di affidabilità;
- segnalare errori, timeout, incompatibilità e perdita di contesto.

## 3. Scambio conforme

Uno scambio AI ospite ↔ KYVERNEX è conforme solo se:

1. la sorgente è identificata nei limiti tecnicamente disponibili;
2. il contenuto trasferito conserva il collegamento con l'origine;
3. capacità e limiti dell'adapter sono dichiarati;
4. gli esiti di validazione sono trasmessi senza alterazioni;
5. i passaggi non osservabili non vengono presentati come verificati;
6. ogni trasformazione rilevante è tracciata;
7. la versione dell'adapter è registrabile.

## 4. Violazioni specifiche

Costituiscono violazione del CCU:

- dichiarare disponibile una capacità assente;
- occultare un limite di osservabilità;
- presentare una validazione parziale come completa;
- perdere il collegamento con l'input originale;
- modificare il contenuto senza registrare la trasformazione;
- eliminare o alterare l'esito prodotto da CORE-005;
- fondere sessioni o contesti senza dichiararlo.

## 5. TODO

- schema formale dello scambio;
- codifica delle capacità;
- autenticazione e autorizzazione;
- isolamento delle sessioni;
- idempotenza;
- timeout e retry;
- test di conformità multipiattaforma.