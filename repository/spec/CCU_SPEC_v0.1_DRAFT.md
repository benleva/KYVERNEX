# CCU_SPEC_v0.1_DRAFT

## Stato del documento

- Versione: 0.1 Draft
- Stato: incompleto e aggiornabile
- Ambito: Contratto Cognitivo Universale (CCU)
- Progetto: MATRICE ARGUS / KYVERNEX

## 1. Scopo

Il Contratto Cognitivo Universale (CCU) definisce le condizioni operative comuni che ogni componente della Matrice ARGUS deve rispettare durante lo scambio, la trasformazione e la restituzione delle informazioni.

Il presente documento formalizza esclusivamente gli elementi già consolidati nel repository e identifica in modo esplicito le parti ancora non definite.

## 2. Principi consolidati

Ogni modulo aderente al CCU deve rispettare i seguenti principi:

1. **Coerenza**: ogni componente interpreta e produce informazioni secondo regole formali condivise.
2. **Integrità**: nessuna informazione può essere alterata senza che la trasformazione venga tracciata.
3. **Compatibilità**: ogni modulo comunica attraverso rappresentazioni condivise.
4. **Verificabilità**: ogni risultato deve poter essere ricostruito e controllato.
5. **Responsabilità cognitiva**: ogni elaborazione mantiene il collegamento con dati, regole e passaggi che l'hanno generata.

## 3. Ambito di applicazione

Il CCU si applica a:

- AET, durante ricezione, normalizzazione e conversione degli input;
- AIL, come rappresentazione cognitiva condivisa;
- kernel KYVERNEX, durante elaborazione, inferenza, memoria e validazione;
- moduli CORE-001 fino a CORE-008;
- fase di restituzione dell'output;
- processi di bootstrap e validazione.

## 4. Obblighi minimi di ogni modulo

Ogni modulo che partecipa alla pipeline deve:

- ricevere dati senza alterarne silenziosamente l'origine;
- preservare l'identità delle informazioni trattate;
- registrare ogni trasformazione rilevante;
- distinguere dati, regole, inferenze e risultati;
- produrre un output compatibile con il modulo successivo;
- consentire la ricostruzione del percorso logico;
- segnalare l'impossibilità di completare correttamente l'operazione.

## 5. Struttura minima di uno scambio cognitivo

Ogni scambio tra moduli deve poter contenere almeno:

- identificatore dell'operazione;
- identificatore dell'informazione o dell'entità trattata;
- modulo sorgente;
- modulo destinatario;
- stato cognitivo corrente;
- contenuto ricevuto o prodotto;
- trasformazione applicata;
- regola o criterio utilizzato;
- origine dei dati;
- esito della verifica;
- collegamento con i passaggi precedenti.

La forma sintattica definitiva di questi campi non è ancora consolidata.

## 6. Ciclo operativo conforme al CCU

Un passaggio tra moduli è conforme quando:

1. l'input è identificabile;
2. il modulo sorgente è noto;
3. la trasformazione applicata è registrata;
4. l'output mantiene il collegamento con l'origine;
5. il destinatario può interpretare la rappresentazione ricevuta;
6. il risultato può essere validato;
7. eventuali anomalie vengono dichiarate.

## 7. Esiti minimi

Il CCU deve poter distinguere almeno i seguenti esiti logici:

- completato;
- completato con riserva;
- non verificabile;
- incompleto;
- incompatibile;
- rifiutato;
- errore.

Questi esiti sono introdotti come categorie operative necessarie alla formalizzazione del contratto, ma la loro codifica definitiva resta da consolidare.

## 8. Violazioni del contratto

Costituiscono violazione del CCU:

- perdita dell'origine dell'informazione;
- trasformazione non registrata;
- fusione non dichiarata tra fatto, ipotesi, deduzione e opinione;
- output non interpretabile dal modulo destinatario;
- risultato non ricostruibile;
- modifica dei dati originali durante la verifica;
- omissione di un errore rilevato.

## 9. Dipendenze

Il CCU dipende da:

- Principi Fondamentali;
- Assiomi della Matrice;
- Regole Fondamentali del Kernel;
- Meta-Regole;
- AET;
- AIL;
- Pipeline del Kernel;
- Stati Cognitivi;
- Regole di Validazione.

## 10. Parti ancora da definire

Restano non consolidate:

- schema formale del messaggio CCU;
- sintassi e serializzazione;
- tipi di identificatore;
- codici di esito ed errore;
- regole di compatibilità tra versioni;
- firma dei messaggi;
- criteri temporali e timeout;
- autorizzazioni tra moduli;
- gestione della concorrenza;
- gestione delle ripetizioni e dell'idempotenza;
- test di conformità.

## 11. Criterio di avanzamento

Il documento potrà passare da `Draft` ad `Alpha` quando saranno definite e approvate:

- struttura obbligatoria del messaggio;
- codifica degli esiti;
- gestione degli errori;
- regole di compatibilità;
- almeno un esempio completo di scambio AET → AIL → KYVERNEX → output;
- test minimi di conformità per ogni modulo.

## 12. Regola di modifica

Ogni aggiornamento del CCU deve essere:

- coerente con gli assiomi;
- compatibile con l'architettura esistente;
- documentato;
- motivato;
- versionato;
- verificabile.
