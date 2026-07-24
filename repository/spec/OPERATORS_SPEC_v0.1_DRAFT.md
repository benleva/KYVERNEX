# ARGUS Formal Operators Specification

Versione: 0.1 Draft
Stato: incompleto e aggiornabile
Progetto: MATRICE ARGUS / KYVERNEX
Autore del progetto: Andrea Pernarcic

## 1. Scopo

Questo documento raccoglie e organizza la definizione preliminare degli operatori formali della Matrice ARGUS.

Gli operatori costituiscono il vocabolario operativo utilizzato per rappresentare e manipolare relazioni cognitive all'interno dell'ARGUS Intermediate Language (AIL) e del kernel KYVERNEX.

Il presente file non introduce semantiche ulteriori rispetto a quelle già consolidate. Le parti non definite sono indicate esplicitamente come incomplete.

## 2. Principi vincolanti

Ogni operatore deve rispettare i seguenti principi:

- coerenza con gli assiomi della Matrice;
- tracciabilità delle trasformazioni;
- verificabilità del risultato;
- separazione tra dati, regole, inferenze e risultati;
- compatibilità con AIL e CCU;
- comportamento riproducibile a parità di dati e condizioni;
- documentazione e versionamento di ogni modifica.

## 3. Registro degli operatori consolidati

### 3.1 Φ - Phi

Funzione consolidata:

- identificazione dell'entità o del concetto trattato.

Stato della specifica:

- significato generale definito;
- firma formale non definita;
- dominio e codominio non definiti;
- sintassi AIL non definita;
- condizioni di errore non definite.

### 3.2 Ω - Omega

Funzione consolidata:

- rappresentazione del risultato o dello stato finale di un processo cognitivo.

Stato della specifica:

- significato generale definito;
- firma formale non definita;
- relazione con gli Stati Cognitivi non formalizzata;
- sintassi AIL non definita;
- condizioni di errore non definite.

### 3.3 Λ - Lambda

Funzione consolidata:

- rappresentazione delle relazioni e dei collegamenti tra entità.

Stato della specifica:

- significato generale definito;
- tipi di relazione non definiti;
- direzionalità non definita;
- cardinalità non definita;
- sintassi AIL non definita.

### 3.4 Σ - Sigma

Funzione consolidata:

- aggregazione e composizione delle informazioni.

Stato della specifica:

- significato generale definito;
- regole di aggregazione non definite;
- ordinamento non definito;
- gestione dei duplicati non definita;
- sintassi AIL non definita.

### 3.5 V

Funzione consolidata:

- validazione e verifica della coerenza logica.

Stato della specifica:

- significato generale definito;
- criteri di esito non definiti;
- livelli di validazione non definiti;
- formato del rapporto di validazione non definito;
- sintassi AIL non definita.

Nota:

- il simbolo V deve essere mantenuto come operatore ufficiale finché una revisione esplicita non ne stabilisca un'altra forma.

### 3.6 μ - Mu

Funzione consolidata:

- memoria e recupero delle informazioni rilevanti.

Stato della specifica:

- significato generale definito;
- tipi di memoria non definiti;
- criteri di rilevanza non definiti;
- regole di persistenza e recupero non definite;
- sintassi AIL non definita.

### 3.7 Δ - Delta

Funzione consolidata:

- rappresentazione di variazioni, trasformazioni o cambiamenti di stato.

Stato della specifica:

- significato generale definito;
- tipi di cambiamento non definiti;
- relazione tra stato iniziale e stato finale non formalizzata;
- reversibilità non definita;
- sintassi AIL non definita.

## 4. Requisiti comuni ancora mancanti

Per ogni operatore devono ancora essere definiti:

- identificatore canonico;
- nome esteso;
- descrizione normativa;
- firma;
- numero e tipo degli argomenti;
- dominio;
- codominio;
- precondizioni;
- postcondizioni;
- invarianti;
- regole di composizione;
- precedenza;
- associatività;
- eventuale commutatività;
- comportamento deterministico;
- gestione dei dati mancanti;
- gestione delle contraddizioni;
- gestione degli errori;
- tracciato di audit;
- rappresentazione AIL;
- esempi validi;
- esempi non validi;
- test di conformità.

## 5. Vincoli di composizione

Sono consolidati soltanto i seguenti vincoli generali:

- nessuna composizione può violare gli assiomi della Matrice;
- ogni trasformazione deve mantenere il collegamento con l'origine;
- ogni risultato deve poter essere ricostruito;
- dati, regole, inferenze e risultati devono restare distinguibili;
- l'esito deve poter essere sottoposto a validazione mediante V;
- ogni variazione prodotta deve poter essere rappresentata mediante Δ;
- ogni informazione recuperata mediante μ deve restare tracciabile.

La precedenza tra operatori non è ancora definita.

## 6. Dipendenze

Questa specifica dipende da:

- AIL_SPEC_v0.1_DRAFT.md;
- CCU_SPEC_v0.1_DRAFT.md;
- Assiomi della Matrice;
- Regole Fondamentali del Kernel;
- Meta-Regole;
- Stati Cognitivi;
- Regole di Validazione.

## 7. Criteri per il passaggio ad Alpha

Il documento potrà passare da Draft ad Alpha soltanto quando, per ogni operatore, saranno definiti e approvati almeno:

- firma formale;
- dominio e codominio;
- sintassi AIL;
- regole di composizione;
- condizioni di errore;
- esempi di utilizzo;
- test minimi di conformità.

## 8. Registro delle lacune

Stato attuale:

- operatori identificati: 7;
- significato generale consolidato: sì;
- formalizzazione matematica: assente;
- grammatica AIL: assente;
- precedenza: assente;
- composizione: assente;
- gestione errori: assente;
- test di conformità: assenti.

Questo documento deve essere aggiornato progressivamente senza alterare le funzioni consolidate degli operatori se non attraverso una revisione esplicita, motivata e versionata.
