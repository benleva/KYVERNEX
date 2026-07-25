# INTER_PROCESS_DELETION_LOCK_SPEC v0.1 DRAFT

## 1. Scopo

Definire il coordinamento esclusivo tra processi KYVERNEX che condividono la stessa directory dei journal di cancellazione.

## 2. Ambito

La specifica protegge le operazioni:

- creazione e aggiornamento dei journal;
- cancellazione coordinata memoria-grafo;
- recupero dei journal pendenti;
- lettura dell'elenco delle transazioni pendenti.

Non definisce un lock distribuito tra host diversi.

## 3. Lock canonico

Ogni directory di journal usa il file stabile:

```text
.kyvernex-deletion.lock
```

Tutti i processi cooperanti devono usare lo stesso percorso canonico.

## 4. Semantica

Il lock è:

- esclusivo;
- advisory;
- acquisito prima di ogni mutazione o recupero;
- rilasciato anche quando l'operazione genera un'eccezione;
- soggetto a timeout configurabile;
- implementato tramite `fcntl.flock` su POSIX e `msvcrt.locking` su Windows.

## 5. Errori

```text
PROCESS_LOCK_GIA_ACQUISITO
PROCESS_LOCK_NON_ACQUISITO
PROCESS_LOCK_TIMEOUT
PROCESS_LOCK_RELEASE_FAILED
LOCK_TIMEOUT_NEGATIVO
LOCK_POLL_INTERVAL_NON_VALIDO
```

## 6. Componente di riferimento

```text
InterProcessFileLock
ProcessSafeMultiTransactionDeletionCoordinator
```

## 7. Garanzie

Quando tutti i processi usano il coordinatore process-safe, una sola operazione di cancellazione, recupero o ispezione dei journal può attraversare la sezione critica per volta.

## 8. Limiti

- Nessuna garanzia per processi che ignorano il lock.
- Nessun coordinamento tra macchine differenti.
- L'affidabilità dipende dalla semantica del filesystem e del sistema operativo.
- Non viene dichiarata serializzabilità generale di tutte le operazioni KYVERNEX.
