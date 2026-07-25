# UPDATE_0017 — Controlled AI Adapter

## Stato
IMPLEMENTATO — TEST SCRITTI, NON ANCORA VERIFICATI DA CI

## Obiettivo
Introdurre il primo confine eseguibile tra KYVERNEX e un modello di intelligenza artificiale esterno senza incorporare il ragionamento del modello nel CORE.

## Componenti aggiunti
- `src/kyvernex/adapters.py`
- `src/kyvernex/orchestrator.py`
- `tests/test_ai_adapter_orchestration.py`

## Componenti aggiornati
- `src/kyvernex/__init__.py`

## Architettura

```text
INPUT
  ↓
KYVERNEX ENGINE
  ↓
AET → RULE ENGINE → VALIDATION → MEMORY
  ↓
AI ADAPTER GATE
  ├─ BLOCCO, se la governance non consente l'esecuzione
  └─ ADAPTER INVOCATION, se l'input supera la governance
       ↓
ADAPTER RESPONSE + ADAPTER AUDIT
```

## Decisioni
1. `AIAdapter` è un protocollo, non un provider specifico.
2. Il CORE non dipende da SDK esterni.
3. `EchoAdapter` è deterministico, offline e destinato a sviluppo e test.
4. `FailingAdapter` permette di verificare il contenimento degli errori.
5. Gli esiti `INCOMPLETO`, `INCOMPATIBILE`, `RIFIUTATO` ed `ERRORE` bloccano l'invocazione.
6. `VALIDATO_CON_RISERVA` può raggiungere l'adapter, mantenendo la riserva nella governance.
7. L'output del modello non sostituisce né altera l'oggetto originale memorizzato.
8. Errori inattesi di provider terzi vengono convertiti in `ADAPTER_UNEXPECTED_ERROR` senza esporre dettagli arbitrari.

## Audit introdotto
- `RICHIESTA_ADAPTER_PREPARATA`
- `INVOCAZIONE_BLOCCATA`
- `RISPOSTA_ADAPTER_RICEVUTA`
- `ADAPTER_ERRORE_CONTROLLATO`
- `ADAPTER_ERRORE_IMPREVISTO`

## Test previsti
- input valido inoltrato all'adapter simulato;
- input incompleto bloccato prima dell'invocazione;
- errore controllato dell'adapter contenuto e tracciato;
- separazione tra oggetto governato e risposta del modello.

## Limitazioni
- nessun provider reale collegato;
- nessuna chiamata di rete;
- nessuna autenticazione o gestione segreti;
- nessun timeout o retry;
- nessuna validazione semantica della risposta del modello;
- Audit dell'adapter restituito separatamente dall'`ExecutionResult` per non rompere il contratto JSON esistente.

## Prossimo incremento consigliato
Introdurre un `ResponseGovernanceLayer` che trasformi la risposta dell'adapter in un nuovo oggetto cognitivo, la validi, la registri in memoria come oggetto derivato e colleghi input e output tramite una relazione tracciabile.
