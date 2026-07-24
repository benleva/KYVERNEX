# REPOSITORY GOVERNANCE

Versione: 0.1 Draft
Stato: normativo per il repository, aggiornabile
Progetto: MATRICE ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Questo documento definisce le regole di governo del repository affinché l'evoluzione di ARGUS e KYVERNEX resti coerente, tracciabile, verificabile e compatibile con i principi consolidati.

## 2. Principi vincolanti

Ogni modifica al repository deve rispettare:

- coerenza con gli assiomi e le regole fondamentali;
- separazione tra dati consolidati, ipotesi progettuali e parti ancora da definire;
- tracciabilità delle decisioni;
- versionamento dei documenti modificati;
- aggiornamento delle interdipendenze;
- verificabilità del contenuto introdotto;
- evoluzione controllata.

## 3. Regola di creazione

Ogni nuova funzione, specifica o concetto tecnico deve essere accompagnato da:

1. un file tecnico nella cartella appropriata;
2. un file di aggiornamento nella cartella `repository/updates`;
3. l'elenco delle dipendenze coinvolte;
4. l'aggiornamento dei file interdipendenti;
5. una versione e uno stato espliciti;
6. un commit identificabile.

## 4. Regola delle interdipendenze

Prima di creare o modificare un file occorre identificare:

- documenti sorgente;
- documenti dipendenti;
- moduli coinvolti;
- eventuali effetti su CCU, AIL, CORE, memoria, validazione, errori, audit, plugin e adattatori AI.

Nessuna modifica può essere considerata completa finché i file direttamente dipendenti non sono stati aggiornati oppure dichiarati esplicitamente non coinvolti.

## 5. Regola del Meta-Modello

Nessuna nuova specifica può introdurre un nuovo oggetto cognitivo senza:

- registrarlo nel futuro `METAMODEL_SPEC`;
- definirne identità, ruolo e relazioni minime;
- dichiararne lo stato come consolidato, proposto o TODO;
- aggiornare le specifiche che lo utilizzano.

Fino alla creazione del `METAMODEL_SPEC`, ogni nuovo concetto deve essere marcato come `PROPOSTO` e non può essere trattato come consolidato.

## 6. Stati documentali

Ogni documento deve dichiarare uno dei seguenti stati:

- `DRAFT`: incompleto e non implementabile;
- `ALPHA`: formalizzato in modo preliminare e testabile;
- `BETA`: sufficientemente completo per integrazioni controllate;
- `STABLE`: approvato come riferimento stabile;
- `DEPRECATED`: mantenuto solo per compatibilità o storico.

## 7. Regola di modifica

Ogni modifica deve indicare:

- motivo;
- contenuto modificato;
- file coinvolti;
- compatibilità;
- parti ancora mancanti;
- commit risultante.

Le modifiche silenziose o prive di file `UPDATE_xxxx` non sono conformi alla governance.

## 8. Regola di non invenzione

Il repository distingue sempre tra:

- elementi consolidati;
- deduzioni necessarie;
- proposte progettuali;
- TODO.

Una proposta non diventa requisito consolidato finché non viene approvata e registrata in un file di aggiornamento.

## 9. Regola di nomenclatura

- `ARGUS` indica la Costituzione Cognitiva Universale.
- `KYVERNEX` indica l'unico motore operativo, kernel e plugin di controllo e validazione continua.
- Non deve essere introdotto un secondo nome per il motore operativo senza una modifica architetturale esplicita.

## 10. Criterio di conformità

Una modifica è conforme solo se:

- è documentata;
- è versionata;
- è tracciabile;
- non contraddice gli assiomi;
- aggiorna le dipendenze;
- non presenta come consolidato ciò che è ancora ipotetico;
- può essere ricostruita dai commit e dai file di aggiornamento.

## 11. Parti da completare

TODO:

- convenzione definitiva per numerazione degli aggiornamenti;
- schema obbligatorio dei file `UPDATE_xxxx`;
- matrice automatica delle dipendenze;
- regole per pull request e revisione;
- criteri di approvazione dei passaggi di stato;
- politica dei tag Git;
- procedura di rollback documentale.

## 12. Stato del documento

Questa versione costituisce la prima governance ufficiale del repository e diventa vincolante per tutte le modifiche successive.