# UPDATE 0013 — EXECUTABLE CLI AND SERIALIZATION

**Stato:** applicato  
**Ambito:** KYVERNEX Reference Prototype 0.1  
**Tipo di modifica:** codice, test e interfaccia eseguibile

## 1. Decisione

Il Reference Prototype acquisisce una prima interfaccia realmente avviabile da terminale e un formato JSON serializzabile per risultati, oggetti cognitivi, validazioni ed eventi di audit.

## 2. File introdotti

- `src/kyvernex/serialization.py`
- `src/kyvernex/cli.py`
- `tests/test_cli_and_serialization.py`

## 3. File aggiornati

- `pyproject.toml`
- `src/kyvernex/__init__.py`

## 4. Comando introdotto

Dopo l'installazione del package:

```bash
kyvernex "contenuto" --source "origine"
```

Il comando restituisce JSON su standard output.

## 5. Regole operative

- il contenuto originale deve restare presente nel risultato;
- gli enum vengono serializzati tramite il loro valore ufficiale;
- la traccia di audit viene inclusa nella risposta;
- un risultato con errori di validazione produce exit code `2`;
- un risultato senza errori produce exit code `0`;
- la serializzazione non certifica ancora conformità AIL completa.

## 6. Dipendenze

- `AET_SPEC_v0.1_DRAFT.md`
- `AIL_SPEC_v0.1_DRAFT.md`
- `VALIDATION_PROTOCOL_v0.1_DRAFT.md`
- `CONFORMANCE_SPEC_v0.1_DRAFT.md`
- `IMPLEMENTATION_ROADMAP_v0.1_DRAFT.md`

## 7. Limiti

Restano da definire:

- schema JSON formale;
- compatibilità tra versioni;
- firma della traccia di audit;
- input da file o standard input;
- Plugin API di rete;
- validazione rispetto a uno schema machine-readable.
