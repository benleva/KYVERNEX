# DEPENDENCY GRAPH SPECIFICATION

**Versione:** 0.1 Draft  
**Stato:** incompleto e aggiornabile  
**Progetto:** Matrice ARGUS / KYVERNEX  
**Autore del progetto:** Andrea Pernarcic

## 1. Scopo

Definire la mappa ufficiale delle dipendenze tra i componenti documentali e architetturali già consolidati nel repository.

Questo documento non introduce nuove funzioni eseguibili. Organizza le relazioni già emerse tra ARGUS, KYVERNEX e le relative specifiche.

## 2. Livelli architetturali

### 2.1 Livello costituzionale ARGUS

ARGUS comprende:

- Principi Fondamentali;
- Assiomi della Matrice;
- Meta-Regole;
- Contratto Cognitivo Universale (CCU);
- Operatori Formali;
- Meta-Modello Cognitivo;
- AIL come linguaggio cognitivo interno.

### 2.2 Livello operativo KYVERNEX

KYVERNEX comprende:

- Plugin API;
- AI Adapter;
- AET;
- moduli CORE-001 fino a CORE-008;
- Protocollo di Validazione Continua;
- Modello degli Errori;
- Architettura della Memoria;
- Audit Trace.

## 3. Flusso operativo consolidato

`AI ospite o sorgente esterna → Plugin API → AI Adapter → CORE-001 → AET → AIL → CORE KYVERNEX → Validazione continua → Memoria / Audit / Error Model → CORE-008 → AI Adapter → Plugin API → AI ospite`

## 4. Dipendenze principali

- `Plugin API → AI Adapter`
- `AI Adapter → CORE-001`
- `CORE-001 → AET`
- `AET → Meta-Modello`
- `AET → AIL`
- `AIL → Meta-Modello`
- `AIL → CCU`
- `AIL → Operatori Formali`
- `CORE-002 → AET`
- `CORE-002 → AIL`
- `CORE-003 → Meta-Modello`
- `CORE-003 → Operatore Λ`
- `CORE-004 → Regole ARGUS`
- `CORE-004 → Operatori Formali`
- `CORE-005 → Validation Protocol`
- `CORE-005 → Error Model`
- `CORE-005 → Audit Trace`
- `CORE-006 → Memory Architecture`
- `CORE-006 → Operatore μ`
- `CORE-006 → record di validazione`
- `CORE-007 → coordinamento di CORE e AI ospite`
- `CORE-007 → Validation Protocol`
- `CORE-008 → esito di validazione`
- `CORE-008 → AI Adapter`
- `Validation Protocol → CCU`
- `Validation Protocol → Error Model`
- `Validation Protocol → Audit Trace`
- `Memory Architecture → AIL`
- `Memory Architecture → Meta-Modello`
- `Audit Trace → Validation Protocol`
- `Audit Trace → Error Model`
- `Audit Trace → Memory Architecture`

## 5. Regole di dipendenza

Ogni nuova specifica deve:

1. dichiarare le proprie dipendenze;
2. indicare quali file sono impattati;
3. evitare dipendenze circolari non dichiarate;
4. distinguere dipendenze normative, operative e informative;
5. generare un file `UPDATE_xxxx` quando modifica la mappa;
6. aggiornare questo documento quando introduce o modifica una relazione.

## 6. Tipi di dipendenza

### 6.1 Normativa

Un componente deve rispettare regole o vincoli definiti da un altro componente.

Esempio: `CORE-005 → CCU`.

### 6.2 Strutturale

Un componente utilizza strutture o categorie definite da un altro componente.

Esempio: `AIL → Meta-Modello`.

### 6.3 Operativa

Un componente invoca, riceve o trasmette informazioni a un altro componente.

Esempio: `AI Adapter → CORE-001`.

### 6.4 Di verifica

Un componente dipende da un altro per validazione, audit o gestione degli errori.

Esempio: `CORE-005 → Audit Trace`.

## 7. Vincoli

- ARGUS non dipende dall'implementazione specifica di una singola AI ospite.
- KYVERNEX può dipendere dalle capacità dichiarate dall'AI ospite solo attraverso Plugin API e AI Adapter.
- AET non può produrre categorie non registrate nel Meta-Modello.
- AIL non può rappresentare come consolidati oggetti non ammessi dal Meta-Modello.
- CORE-006 non può consolidare come valida un'informazione priva di esito conforme di CORE-005.
- CORE-008 deve dichiarare risultati parzialmente validati o non verificabili.
- Nessun componente può eludere il CCU o la validazione continua senza dichiararlo.

## 8. Parti ancora da definire

TODO:

- identificatori univoci delle dipendenze;
- formato machine-readable della mappa;
- regole automatiche di controllo delle dipendenze;
- rilevazione di cicli;
- severità delle violazioni;
- integrazione con CI/CD;
- diagramma generato automaticamente;
- compatibilità tra versioni delle specifiche.

## 9. Requisiti per lo stato ALPHA

Il documento potrà passare ad ALPHA quando saranno definiti:

- un formato serializzabile della mappa;
- un controllo automatico minimo;
- identificatori stabili dei componenti;
- regole di compatibilità tra versioni;
- almeno un test che rilevi una dipendenza mancante o circolare.
