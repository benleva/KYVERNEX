# VERSIONING POLICY SPEC v0.1 DRAFT

## Scopo
Definire una politica minima e verificabile per la revisione degli oggetti cognitivi KYVERNEX.

## Principi normativi
1. Un oggetto cognitivo memorizzato non viene sovrascritto.
2. Ogni revisione genera un nuovo `CognitiveObject` con un nuovo `object_id`.
3. La nuova versione deve essere collegata alla precedente tramite `DERIVED_FROM`.
4. La motivazione della revisione è obbligatoria.
5. Il tipo di cambiamento deve essere esplicito.
6. Una scrittura parziale non deve lasciare il successore in memoria senza la relazione di provenienza.

## Tipi di cambiamento
- `CORREZIONE`
- `ARRICCHIMENTO`
- `RICLASSIFICAZIONE`
- `SOSTITUZIONE`

## Formato versione
Il prototipo supporta il formato numerico `major.minor` e incrementa il componente `minor` di una unità.

Esempio:

```text
0.1 -> 0.2 -> 0.3
```

## Metadati obbligatori del successore
- `previous_object_id`
- `version_change_type`
- `version_reason`

## Storia delle versioni
La storia è ricostruita seguendo le relazioni `DERIVED_FROM` dal più recente al più antico.

Devono essere segnalati come conflitto:
- più predecessori per la stessa versione;
- cicli nella catena;
- predecessori non presenti in memoria;
- formato versione non valido.

## Limiti della versione 0.1
- nessun branching o merge di versioni;
- nessuna numerazione semantica completa;
- nessuna persistenza autonoma;
- nessuna firma crittografica della transizione;
- coordinamento process-local tra memoria e grafo.
