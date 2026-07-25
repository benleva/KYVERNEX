# UPDATE_0028 - Continuous Integration

## Stato
IMPLEMENTATO, ESECUZIONE DA VERIFICARE

## Obiettivo
Introdurre una pipeline GitHub Actions ripetibile per eseguire l'intera suite di test KYVERNEX a ogni modifica del ramo principale e a ogni pull request.

## Modifiche
- Creato `.github/workflows/tests.yml`.
- Configurata l'esecuzione su Python 3.11, 3.12 e 3.13.
- Installazione del progetto in modalità editable con dipendenze di test.
- Comando di verifica: `python -m pytest -q`.
- Aggiunto avvio manuale tramite `workflow_dispatch`.
- Limitati i permessi del workflow alla sola lettura dei contenuti.

## Criterio di completamento
L'aggiornamento sarà considerato VERIFICATO soltanto dopo la conclusione positiva di tutte le esecuzioni della matrice GitHub Actions.

## Vincoli
La presenza del file workflow non dimostra che i test siano passati. Lo stato della CI deve essere letto dai risultati effettivi di GitHub Actions.
