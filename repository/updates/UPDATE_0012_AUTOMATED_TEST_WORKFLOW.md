# UPDATE 0012 — AUTOMATED TEST WORKFLOW

**Stato:** applicato  
**Ambito:** KYVERNEX Reference Prototype 0.1  
**Tipo di modifica:** infrastruttura di test e verifica

## 1. Decisione

È introdotto il workflow GitHub Actions `.github/workflows/test.yml` per eseguire automaticamente la suite di test del prototipo KYVERNEX.

## 2. Comportamento

Il workflow viene avviato:

- a ogni push sul branch `main`;
- a ogni pull request verso `main`;
- manualmente tramite `workflow_dispatch`.

## 3. Ambienti verificati

La matrice iniziale comprende:

- Python 3.11;
- Python 3.12;
- Python 3.13.

## 4. Procedura

Per ciascuna versione Python il workflow:

1. recupera il repository;
2. configura l'interprete;
3. installa il package in modalità editable con le dipendenze di test;
4. esegue `python -m pytest -q`.

## 5. Evidenza di conformità

Un commit può essere considerato testato soltanto quando i job previsti dal workflow risultano completati con successo. La sola presenza dei test nel repository non costituisce evidenza di esecuzione.

## 6. Dipendenze coinvolte

- `pyproject.toml`;
- `tests/test_reference_prototype.py`;
- `repository/IMPLEMENTATION_ROADMAP_v0.1_DRAFT.md`;
- `repository/spec/CONFORMANCE_SPEC_v0.1_DRAFT.md`;
- `repository/updates/UPDATE_0011_REFERENCE_PROTOTYPE_BOOTSTRAP.md`.

## 7. Limiti attuali

- non sono ancora configurati coverage, linting, type checking o test di sicurezza;
- il workflow verifica il prototipo esistente, non certifica la conformità completa ARGUS/KYVERNEX;
- lo stato Alpha richiede ancora le evidenze e le specifiche mancanti indicate nei report del repository.
