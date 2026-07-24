# AET SPECIFICATION

**Titolo:** ARGUS Executive Translator (AET)  
**Versione:** 0.1 Draft  
**Stato:** incompleto, non implementabile  
**Progetto:** Matrice ARGUS / KYVERNEX  
**Autore del progetto:** Andrea Pernarcic

## 1. Scopo

AET è il traduttore esecutivo di ARGUS. Riceve contenuti esterni tramite l'AI Adapter o altri ingressi autorizzati e li prepara per la rappresentazione interna AIL, preservando significato, origine, contesto e tracciabilità.

## 2. Collocazione architetturale

Flusso consolidato:

`AI ospite o sorgente esterna → AI Adapter → CORE-001 → AET → AIL → CORE KYVERNEX`

AET opera tra acquisizione e rappresentazione interna. Non sostituisce l'AI Adapter, che gestisce l'integrazione con la piattaforma ospite, e non sostituisce AIL, che rappresenta il contenuto normalizzato.

## 3. Responsabilità consolidate

AET deve:

1. ricevere l'input acquisito da CORE-001;
2. preservare il contenuto originale;
3. registrare origine, contesto e formato dell'input;
4. identificare le categorie cognitive già registrate nel Meta-Modello quando tecnicamente possibile;
5. distinguere almeno dati, fatti, ipotesi, deduzioni, opinioni, regole e risultati quando tali distinzioni sono esplicite o ricostruibili senza invenzione;
6. segnalare ambiguità, incompletezza o incompatibilità;
7. produrre un output compatibile con AIL;
8. mantenere il collegamento tra input originale e rappresentazione prodotta;
9. rispettare il CCU;
10. rendere disponibili a CORE-005 gli elementi necessari alla validazione.

## 4. Vincoli

AET non deve:

- modificare silenziosamente il significato dell'input;
- trasformare un'ipotesi in fatto;
- fondere categorie cognitive differenti senza dichiararlo;
- eliminare la fonte o l'origine;
- inventare informazioni mancanti;
- produrre una rappresentazione AIL dichiarata valida quando la traduzione è incompleta o non verificabile.

## 5. Input minimo atteso

Ogni ingresso AET dovrà poter contenere almeno:

- identificatore dell'operazione;
- contenuto originale;
- sorgente o sistema di provenienza;
- formato dichiarato o rilevato;
- contesto disponibile;
- versione dell'AI Adapter o del modulo sorgente;
- eventuali limiti di osservabilità dichiarati.

La sintassi definitiva resta da definire.

## 6. Output minimo atteso

Ogni uscita AET dovrà poter contenere almeno:

- riferimento all'input originale;
- rappresentazione normalizzata candidata ad AIL;
- categorie cognitive identificate;
- elementi non classificati;
- ambiguità rilevate;
- trasformazioni applicate;
- livello di completezza;
- esito preliminare della traduzione;
- riferimenti necessari alla validazione.

La serializzazione definitiva resta da definire in AIL e CCU.

## 7. Esiti preliminari

AET deve poter distinguere almeno:

- TRADOTTO;
- TRADOTTO_CON_RISERVA;
- AMBIGUO;
- INCOMPLETO;
- INCOMPATIBILE;
- NON_VERIFICABILE;
- ERRORE.

La codifica normativa di tali esiti resta da consolidare.

## 8. Relazione con il Meta-Modello

AET usa il Meta-Modello come registro delle categorie cognitive ammesse. Nessuna categoria nuova può essere introdotta da AET come consolidata senza aggiornamento del `METAMODEL_SPEC` e relativo file UPDATE.

## 9. Relazione con la validazione continua

CORE-005 deve poter validare almeno:

- integrità dell'input originale;
- tracciabilità delle trasformazioni;
- correttezza della classificazione dichiarata;
- compatibilità dell'output con AIL;
- dichiarazione delle ambiguità;
- assenza di aggiunte non tracciate.

AET non può autorizzare il consolidamento di un contenuto.

## 10. Dipendenze

- `AI_ADAPTER_SPEC_v0.1_DRAFT.md`;
- `METAMODEL_SPEC_v0.1_DRAFT.md`;
- `AIL_SPEC_v0.1_DRAFT.md`;
- `CCU_SPEC_v0.1_DRAFT.md`;
- `CORE_SPEC_v0.1_DRAFT.md`;
- `VALIDATION_PROTOCOL_v0.1_DRAFT.md`;
- `ERROR_MODEL_v0.1_DRAFT.md`.

## 11. Parti non ancora definite

TODO:

- formati di input supportati;
- grammatica di riconoscimento;
- algoritmo di normalizzazione;
- criteri formali di classificazione;
- gestione multilingua e multimodale;
- punteggi di confidenza;
- struttura serializzabile di input e output;
- API;
- timeout e limiti;
- gestione dello streaming;
- comportamento sincrono e asincrono;
- codici di errore;
- test di conformità.

## 12. Requisiti per lo stato ALPHA

Il documento potrà passare da Draft ad Alpha quando saranno definiti e testabili:

1. schema di input;
2. schema di output;
3. regole di classificazione;
4. gestione delle ambiguità;
5. integrazione formale con AIL;
6. errori ed esiti;
7. almeno un esempio completo AI Adapter → AET → AIL;
8. test minimi di conformità.

## 13. Stato del documento

Questa specifica consolida il ruolo e i vincoli di AET senza definire ancora algoritmi eseguibili o una grammatica definitiva.
