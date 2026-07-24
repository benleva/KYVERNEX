# UPDATE 0011 — REFERENCE PROTOTYPE BOOTSTRAP

**Stato:** applicato  
**Ambito:** KYVERNEX Reference Prototype 0.1  
**Tipo:** implementazione iniziale, non Alpha

## 1. Decisione tecnica

Per il primo prototipo di riferimento viene adottato Python 3.11 come linguaggio provvisorio. La scelta non modifica l'indipendenza architetturale di ARGUS e non impedisce future implementazioni in altri linguaggi.

## 2. Componenti creati

- `pyproject.toml`;
- `src/kyvernex/models.py`;
- `src/kyvernex/core.py`;
- `src/kyvernex/__init__.py`;
- `tests/test_reference_prototype.py`.

## 3. Funzioni implementate

Il prototipo comprende esclusivamente:

1. acquisizione dell'input;
2. preservazione del contenuto originale;
3. registrazione dell'origine;
4. normalizzazione AET minima;
5. creazione dell'oggetto cognitivo minimo;
6. validazione dei campi obbligatori;
7. esiti `VALIDATO`, `VALIDATO_CON_RISERVA` e `INCOMPLETO` nel percorso attualmente eseguibile;
8. Audit Trace provvisorio delle operazioni osservabili;
9. restituzione di oggetto, esito e traccia;
10. isolamento minimo tra sessioni.

## 4. Vincoli

- Il codice è un Reference Prototype e non è dichiarato Alpha.
- Non implementa ancora Rule Engine, memoria persistente, Plugin API di rete, AI Adapter specifici, operatori formali o inferenza.
- L'Audit Trace è provvisorio, poiché la relativa specifica completa è ancora mancante.
- I test sono stati aggiunti al repository, ma non risultano eseguiti da una pipeline CI in questo aggiornamento.
- Nessun output del prototipo deve essere presentato come certificato ARGUS.

## 5. Interdipendenze

Riferimenti applicati:

- `repository/IMPLEMENTATION_ROADMAP_v0.1_DRAFT.md`;
- `repository/spec/CONFORMANCE_SPEC_v0.1_DRAFT.md`;
- `repository/spec/AET_SPEC_v0.1_DRAFT.md`;
- `repository/spec/AIL_SPEC_v0.1_DRAFT.md`;
- `repository/spec/VALIDATION_PROTOCOL_v0.1_DRAFT.md`;
- `repository/spec/CORE_SPEC_v0.1_DRAFT.md`.

## 6. Prossimo gate

Prima di estendere il prototipo devono essere:

1. eseguiti i test in ambiente controllato;
2. formalizzata la specifica Audit Trace mancante;
3. introdotta una serializzazione stabile degli oggetti;
4. aggiunto il primo controllo di conformità automatico.
