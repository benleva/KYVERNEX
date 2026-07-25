# UPDATE 0014 — JSON Schema e Rule Engine eseguibile

Data: 2026-07-25
Stato: IMPLEMENTATO NEL REFERENCE PROTOTYPE, DA VALIDARE IN CI
Progetto: ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Introdurre il primo motore deterministico di regole e un contratto JSON machine-readable per il risultato di esecuzione del Reference Prototype 0.1.

## 2. File creati

- `src/kyvernex/rules.py`;
- `schemas/execution-result.schema.json`;
- `tests/test_rule_engine.py`.

## 3. File aggiornati

- `src/kyvernex/core.py`;
- `src/kyvernex/__init__.py`;
- `tests/test_reference_prototype.py`.

## 4. Funzioni introdotte

Il Rule Engine:

- registra regole mediante identificatori stabili;
- applica regole deterministiche a un oggetto cognitivo;
- distingue severità informative, riserve ed errori;
- converte eccezioni interne alle regole in errori controllati;
- registra nell'oggetto gli identificatori delle regole applicate;
- genera un evento di audit dedicato `RULE_ENGINE / REGOLE_APPLICATE`.

Le prime regole eseguibili sono:

- `ARGUS-R001`: origine obbligatoria;
- `ARGUS-R002`: contenuto originale obbligatorio;
- `ARGUS-R003`: trasformazioni osservabili tracciate.

## 5. Contratto JSON

Lo schema `execution-result.schema.json` formalizza la struttura serializzata di:

- sessione;
- oggetto cognitivo;
- validazione;
- traccia di audit.

Lo schema è Draft 2020-12. In questa fase i test verificano il contratto strutturale essenziale senza introdurre una dipendenza runtime da un validatore JSON Schema esterno.

## 6. Dipendenze e impatti

Dipendenze normative e strutturali:

- ARGUS;
- AIL Specification;
- Meta-Modello;
- Validation Protocol;
- Error Model;
- Audit Trace provvisorio;
- Implementation Roadmap;
- Dependency Graph.

Impatto operativo:

`AET → Rule Engine → CORE-005 → Audit → CORE-008`

## 7. Limiti dichiarati

- le tre regole non rappresentano l'intera Costituzione ARGUS;
- lo schema JSON è un primo contratto e non la grammatica AIL definitiva;
- il Rule Engine non supporta ancora dipendenze tra regole, priorità, versionamento o caricamento sicuro di plugin esterni;
- i nuovi test devono ancora essere confermati da un'esecuzione CI verificabile;
- il progetto resta `Reference Prototype 0.1` e non può essere dichiarato Alpha.

## 8. Criterio del prossimo avanzamento

Il prossimo incremento dovrà introdurre almeno uno tra:

1. validazione completa dello schema JSON in CI;
2. registro versionato delle regole;
3. Plugin API locale con request e response formalizzate;
4. memoria minima isolata per sessione.
