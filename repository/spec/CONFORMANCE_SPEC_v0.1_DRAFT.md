# CONFORMANCE SPECIFICATION

Versione: 0.1 Draft
Stato: incompleto e aggiornabile
Progetto: Matrice ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Definire i criteri con cui una documentazione, un modulo, una pipeline o una futura implementazione di KYVERNEX può essere valutata rispetto ai principi ARGUS e alle specifiche del repository.

La presente versione non istituisce ancora una certificazione commerciale o legale. Definisce un protocollo tecnico preliminare di conformità.

## 2. Principi vincolanti

Una valutazione di conformità deve:

- utilizzare requisiti espliciti e versionati;
- distinguere elementi verificati, parzialmente verificati, non conformi e non verificabili;
- preservare le evidenze utilizzate;
- dichiarare limiti, eccezioni e dipendenze mancanti;
- non attribuire conformità a funzioni non implementate;
- collegare ogni esito alle specifiche applicate;
- produrre una traccia ricostruibile della verifica.

## 3. Oggetto della conformità

La conformità può essere valutata su:

1. repository documentale;
2. schema dati;
3. singolo modulo CORE;
4. pipeline KYVERNEX;
5. validazione continua;
6. Audit Trace;
7. Plugin API e AI Adapter;
8. implementazione completa.

Ogni valutazione deve dichiarare con precisione il proprio oggetto e il relativo perimetro.

## 4. Livelli preliminari

### Level 0 — Repository

Verifica presenza, versionamento, stato, dipendenze, UPDATE e coerenza documentale minima.

### Level 1 — Modello dati

Verifica compatibilità con Meta-Modello, AIL, origine, identità, stato e tracciabilità.

### Level 2 — Pipeline

Verifica il flusso minimo Plugin API → AI Adapter → CORE-001 → AET → AIL → CORE → CORE-008.

### Level 3 — Validazione

Verifica richiamo di CORE-005 nei punti previsti, produzione degli esiti e impedimento del consolidamento non conforme.

### Level 4 — Audit

Verifica registrazione delle operazioni osservabili di KYVERNEX, delle regole applicate, degli esiti e dei limiti dichiarati.

### Level 5 — Plugin

Verifica integrazione con almeno una AI ospite o simulatore tramite Plugin API e AI Adapter.

### Level 6 — Implementazione certificabile

Verifica end-to-end, test ripetibili, compatibilità di versione, tracciabilità completa e assenza di violazioni bloccanti note.

I livelli sono cumulativi: un livello superiore richiede il soddisfacimento dei livelli precedenti, salvo limitazioni esplicitamente dichiarate.

## 5. Esiti

Gli esiti preliminari sono:

- `CONFORME`;
- `CONFORME_CON_LIMITAZIONI`;
- `NON_CONFORME`;
- `NON_VERIFICABILE`.

Un esito deve includere:

- oggetto valutato;
- livello richiesto;
- versione delle specifiche;
- evidenze;
- requisiti soddisfatti;
- requisiti non soddisfatti;
- limitazioni;
- data e identificatore della verifica.

## 6. Evidenze minime

Le evidenze possono includere:

- file e versioni del repository;
- configurazioni;
- schemi serializzati;
- risultati di test;
- record di validazione;
- Audit Trace;
- log delle operazioni KYVERNEX;
- dichiarazioni di capacità e limiti dell'AI ospite.

Non è ammessa una dichiarazione di conformità basata esclusivamente su descrizioni prive di evidenza verificabile.

## 7. Requisiti minimi per componente

### Repository

- Governance presente;
- file UPDATE per modifiche tecniche;
- dipendenze dichiarate;
- stato e versione dei documenti;
- TODO distinti dagli elementi consolidati.

### Dati e AIL

- identità;
- categoria cognitiva;
- origine;
- contenuto originale o riferimento;
- stato cognitivo;
- trasformazioni;
- esito di validazione;
- collegamento di audit.

### Pipeline

- ordine dei componenti dichiarato;
- passaggi osservabili registrati;
- limiti dell'AI ospite dichiarati;
- nessuna trasformazione silenziosa.

### Validazione

- controlli ripetibili;
- esiti espliciti;
- anomalie collegate a ERROR_MODEL;
- blocco del consolidamento non validato.

### Audit

- identificatori stabili;
- ordine ricostruibile degli eventi;
- versioni delle specifiche;
- distinzione tra passaggi osservabili e non osservabili.

## 8. Violazioni bloccanti preliminari

Sono bloccanti:

- perdita dell'origine;
- trasformazione non tracciata;
- presentazione di un risultato non verificato come validato;
- elusione non dichiarata del CCU o della validazione continua;
- fusione non dichiarata tra fatto, ipotesi, deduzione e opinione;
- dichiarazione di funzioni non implementate;
- assenza di evidenze per il livello richiesto.

## 9. Dipendenze

- GOVERNANCE;
- CCU_SPEC;
- METAMODEL_SPEC;
- AIL_SPEC;
- CORE_SPEC;
- VALIDATION_PROTOCOL;
- ERROR_MODEL;
- MEMORY_ARCHITECTURE;
- AUDIT_TRACE_SPEC;
- PLUGIN_API_SPEC;
- AI_ADAPTER_SPEC;
- DEPENDENCY_GRAPH_SPEC;
- IMPLEMENTATION_ROADMAP.

## 10. Parti ancora da definire

TODO:

- matrice machine-readable dei requisiti;
- identificatori normativi stabili;
- severità delle violazioni;
- procedura di riesame;
- firma delle evidenze;
- validatore automatico;
- suite di test ufficiale;
- regole di compatibilità tra versioni;
- autorità e processo di certificazione;
- uso eventuale di denominazioni come ARGUS Certified.

## 11. Requisiti per lo stato ALPHA

Il documento potrà passare ad ALPHA quando saranno disponibili:

- matrice dei requisiti serializzabile;
- almeno un controllo automatico Level 0;
- almeno un esempio Level 1;
- test ripetibili per gli esiti;
- Audit Trace formalizzato;
- regole di compatibilità di versione;
- rapporto di conformità di esempio.

## 12. Regola di prudenza

Fino al completamento dei requisiti ALPHA, nessun componente deve essere presentato come certificato. Sono ammesse esclusivamente valutazioni Draft con perimetro, evidenze e limitazioni esplicite.
