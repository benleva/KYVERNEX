# KYVERNEX REFERENCE PROTOTYPE — TEST REPORT

**Data:** 2026-07-25  
**Versione testata:** Reference Prototype 0.1  
**Esito:** SUPERATO CON LIMITAZIONI

## 1. Ambito

È stata ricostruita ed eseguita in un ambiente Python isolato la versione corrente dei seguenti file del repository:

- `pyproject.toml`;
- `src/kyvernex/models.py`;
- `src/kyvernex/core.py`;
- `src/kyvernex/__init__.py`;
- `tests/test_reference_prototype.py`.

## 2. Comando eseguito

```text
python -m pytest -q
```

## 3. Risultato

```text
....                                                                     [100%]
4 passed in 0.06s
```

## 4. Funzioni verificate

- preservazione del contenuto originale;
- registrazione della fonte;
- passaggio allo stato `VALIDATO` per input conforme;
- rifiuto della validazione completa quando manca la fonte;
- rifiuto della validazione completa per input vuoto;
- produzione di quattro eventi di audit nel percorso minimo;
- isolamento degli identificatori tra sessioni distinte.

## 5. Limitazioni dell'evidenza

- il test è stato eseguito in un ambiente isolato ricostruito dai file correnti del repository;
- il workflow GitHub Actions è stato aggiunto, ma al momento della verifica non risultavano ancora workflow run o status pubblicati per il commit più recente;
- non sono stati ancora eseguiti test su tutte le versioni Python della matrice CI;
- non sono ancora configurati coverage, linting, type checking o security scanning;
- questo esito non autorizza la classificazione del prototipo come `ALPHA`.

## 6. Conclusione

Il Vertical Slice minimo di KYVERNEX è eseguibile e i quattro test iniziali risultano superati. Il prossimo gate tecnico è ottenere la stessa evidenza tramite GitHub Actions e ampliare la suite con serializzazione, audit, errori e compatibilità del modello dati.
