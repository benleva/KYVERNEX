# AUDIT TRACE SPEC v0.1 DRAFT

## 1. Scopo

Definire il tracciamento durevole, ordinato e verificabile degli eventi prodotti dai componenti KYVERNEX.

## 2. Modello

Ogni record contiene:

- numero di sequenza globale;
- evento `AuditEvent` completo;
- hash del record precedente;
- hash SHA-256 del record corrente.

Il primo record usa un hash di genesi composto da 64 zeri.

## 3. Proprietà richieste

1. Append-only tramite API pubblica.
2. Ordinamento deterministico per sequenza.
3. Persistenza JSON versionata.
4. Scrittura atomica con file temporaneo, `fsync` e sostituzione.
5. Verifica dell'integrità della catena a ogni caricamento.
6. Filtraggio in lettura per `session_id` senza modificare l'ordine globale.
7. Nessuna dichiarazione di non ripudio crittografico o firma digitale.

## 4. Canonicalizzazione

L'hash è calcolato sulla rappresentazione JSON canonica di:

```text
sequence + event + previous_hash
```

con chiavi ordinate e separatori compatti UTF-8.

## 5. Errori normativi

- `AUDIT_TRACE_VERSION_UNSUPPORTED`
- `AUDIT_TRACE_RECORDS_INVALID`
- `AUDIT_TRACE_FILE_INVALID`
- `AUDIT_TRACE_CHAIN_BROKEN`
- `AUDIT_TRACE_HASH_MISMATCH`
- `AUDIT_SESSION_ID_MANCANTE`
- `AUDIT_OPERATION_ID_MANCANTE`
- `AUDIT_EVENT_DATA_MANCANTI`

## 6. Limiti

La catena rileva alterazioni accidentali o successive del file, ma non impedisce a un attore con accesso completo di riscrivere l'intero ledger e ricalcolare gli hash. Firma digitale, ancoraggio esterno e storage WORM restano fuori dalla versione 0.1.

## 7. Conformità

Un'implementazione è conforme quando conserva e ricarica i record, verifica sequenza e hash, rifiuta formati incompatibili e non altera gli eventi durante la serializzazione.
