# UPDATE 0030 - COGNITIVE CONFIDENCE PROPAGATION

## Stato

Implementato. Test creati, esecuzione non ancora confermata.

## Modifiche

Creati:

- `src/kyvernex/confidence.py`
- `tests/test_confidence.py`
- `repository/specifications/COGNITIVE_CONFIDENCE_PROPAGATION_SPEC_v0.1_DRAFT.md`

Aggiornato:

- `src/kyvernex/__init__.py`

## Funzioni introdotte

- confidenza diretta da metadata;
- valore predefinito configurabile;
- propagazione tramite `SUPPORTS` e `DEPENDS_ON`;
- penalizzazione tramite `CONTRADICTS`;
- rilevazione dei cicli;
- elenco delle evidenze positive e contrarie;
- riserve esplicite;
- validazione dell'intervallo numerico `[0, 1]`.

## Limiti

Il risultato è una misura strutturale, non una certificazione di verità.

La suite automatica non è stata osservata in esecuzione al momento della creazione di questo aggiornamento.
