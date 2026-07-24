# AIL / AET ADDENDUM v0.1 DRAFT

## Scopo

Definire il passaggio tra la traduzione esecutiva AET e la rappresentazione interna AIL.

## Regole consolidate

- AET produce una rappresentazione candidata ad AIL.
- AIL conserva identità, origine, categorie cognitive, trasformazioni, stato ed elementi necessari alla verifica.
- Un output AET ambiguo, incompleto o non verificabile deve mantenere tale condizione nella rappresentazione AIL.
- AIL non può cancellare le riserve dichiarate da AET.
- La validità sintattica e semantica definitiva resta da definire.

## Requisiti minimi del passaggio

Il trasferimento AET → AIL deve preservare almeno:

- riferimento all'input originale;
- sorgente;
- categorie cognitive identificate;
- elementi non classificati;
- trasformazioni applicate;
- ambiguità;
- livello di completezza;
- esito preliminare AET;
- riferimenti per la validazione.

## Stato

Draft. Schema, serializzazione, parser e validatore restano TODO.
