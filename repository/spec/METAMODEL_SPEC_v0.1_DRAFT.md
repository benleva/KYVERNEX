# METAMODEL SPECIFICATION

**Titolo:** Meta-Modello Cognitivo ARGUS  
**Versione:** 0.1 Draft  
**Stato:** incompleto, non implementabile  
**Progetto:** Matrice ARGUS / KYVERNEX  
**Autore del progetto:** Andrea Pernarcic

## 1. Scopo

Il Meta-Modello definisce le categorie strutturali minime che la Matrice ARGUS deve poter distinguere, rappresentare, collegare, validare e tracciare.

Il presente documento non introduce una sintassi eseguibile e non sostituisce AIL. Stabilisce il vocabolario strutturale comune sul quale dovranno basarsi AET, AIL, CCU, CORE, memoria, validazione ed errori.

## 2. Principi vincolanti

Ogni oggetto cognitivo deve:

- possedere un'identità nel proprio contesto;
- mantenere il collegamento con la propria origine;
- dichiarare la propria categoria quando conosciuta;
- mantenere distinto il contenuto originale dalle trasformazioni successive;
- poter essere collegato a regole, relazioni, stati ed esiti;
- poter essere sottoposto a verifica senza alterare i dati originali;
- mantenere una traccia delle trasformazioni rilevanti;
- rispettare CCU, assiomi, regole fondamentali e meta-regole.

## 3. Oggetto radice consolidato

### 3.1 Entità Cognitiva

Ogni informazione trattata dal sistema è rappresentabile come entità cognitiva.

Campi strutturali minimi richiesti, ancora privi di sintassi definitiva:

- identificatore;
- contesto;
- categoria;
- contenuto o riferimento al contenuto;
- origine;
- stato cognitivo;
- relazioni;
- trasformazioni;
- regole applicate;
- esiti di validazione;
- versione.

## 4. Categorie cognitive consolidate

Le categorie seguenti derivano dalla documentazione già consolidata.

### 4.1 Dato

Contenuto ricevuto o registrato prima delle inferenze prodotte dal kernel.

### 4.2 Fatto

Informazione trattata dal sistema come fatto dichiarato o verificato nel contesto disponibile.

La specifica definitiva dei criteri probatori non è ancora definita.

### 4.3 Ipotesi

Informazione proposta come possibile spiegazione o possibilità, distinta da un fatto.

### 4.4 Deduzione

Risultato derivato da dati e regole attraverso passaggi logici tracciabili.

### 4.5 Opinione

Valutazione o interpretazione che non deve essere fusa silenziosamente con fatti, ipotesi o deduzioni.

### 4.6 Regola

Vincolo o criterio applicabile a una trasformazione, inferenza, validazione o decisione operativa.

### 4.7 Assioma

Regola fondante della Matrice ARGUS che non può essere violata da una trasformazione conforme.

### 4.8 Meta-Regola

Regola che governa l'evoluzione, la precedenza, la compatibilità e la verificabilità delle regole del sistema.

### 4.9 Relazione

Collegamento esplicito tra due o più entità cognitive.

### 4.10 Trasformazione

Passaggio documentato che produce una nuova rappresentazione mantenendo il collegamento con l'origine.

### 4.11 Risultato

Esito prodotto da un'elaborazione, una trasformazione, un'inferenza o una validazione.

### 4.12 Fonte o Origine

Riferimento alla provenienza dell'informazione o al contenuto originale da cui deriva.

### 4.13 Stato Cognitivo

Condizione assunta da un'entità durante il ciclo di elaborazione.

Stati positivi consolidati:

- ACQUISITO;
- NORMALIZZATO;
- ELABORATO;
- VALIDATO;
- CONSOLIDATO.

Gli stati negativi o di eccezione restano da formalizzare nel modello degli errori.

### 4.14 Validazione

Controllo documentato della conformità di un oggetto rispetto a regole, assiomi, meta-regole, CCU e vincoli applicabili.

### 4.15 Errore

Segnalazione strutturata di una condizione non conforme, non verificabile, incompatibile o incompleta.

La tassonomia normativa resta demandata a `ERROR_MODEL_v0.2_DRAFT.md`.

## 5. Relazioni minime da rappresentare

Il Meta-Modello deve consentire almeno le relazioni seguenti:

- entità deriva da origine;
- entità è trasformata in nuova entità;
- entità è collegata a entità;
- regola si applica a entità o trasformazione;
- deduzione deriva da dati e regole;
- risultato deriva da elaborazione;
- validazione controlla entità, trasformazione o risultato;
- errore riguarda entità, trasformazione, modulo o validazione;
- stato appartiene a entità in un determinato passaggio;
- memoria conserva una rappresentazione e la relativa provenienza.

La codifica e la cardinalità di tali relazioni non sono ancora consolidate.

## 6. Invarianti preliminari

- Un'entità non perde il collegamento con la propria origine.
- Una trasformazione non sostituisce silenziosamente il contenuto originale.
- Fatto, ipotesi, deduzione e opinione restano categorie distinguibili.
- Una deduzione deve mantenere il collegamento con dati e regole che l'hanno generata.
- Un risultato non diventa consolidato senza un esito di validazione conforme.
- Un errore non può essere registrato come risultato validato senza una nuova elaborazione e validazione.
- Una relazione deve identificare gli oggetti collegati.
- Ogni modifica strutturale al Meta-Modello deve essere versionata e registrata tramite un file UPDATE.

## 7. Dipendenze

Il Meta-Modello dipende da:

- Principi Fondamentali;
- Assiomi della Matrice;
- Regole Fondamentali del Kernel;
- Meta-Regole;
- CCU;
- Stati Cognitivi;
- Regole di Validazione;
- Governance del repository.

Sono dipendenti dal Meta-Modello:

- AET_SPEC;
- AIL_SPEC;
- CORE_SPEC;
- MEMORY_ARCHITECTURE;
- VALIDATION_PROTOCOL;
- ERROR_MODEL;
- future specifiche di audit e adattamento AI.

## 8. Parti non ancora definite

TODO:

- schema formale dell'Entità Cognitiva;
- tipi e formati degli identificatori;
- cardinalità delle relazioni;
- gerarchia definitiva delle categorie;
- criteri per distinguere fatto verificato e fatto dichiarato;
- rappresentazione temporale;
- gestione del contesto;
- provenienza multipla;
- conflitti tra entità;
- versionamento degli oggetti cognitivi;
- serializzazione AIL;
- vincoli di validità;
- test di conformità.

## 9. Regola di estensione

Nessuna nuova categoria cognitiva può essere considerata consolidata se non viene:

1. definita nel Meta-Modello;
2. motivata tramite un file `UPDATE_xxxx`;
3. collegata alle specifiche interdipendenti;
4. versionata;
5. verificata rispetto ad assiomi, meta-regole e CCU.

## 10. Criteri per il passaggio ad Alpha

Il documento potrà passare da Draft ad Alpha quando saranno definiti e testabili:

- schema minimo dell'Entità Cognitiva;
- categorie normative;
- relazioni e cardinalità;
- invarianti;
- gestione del contesto e della provenienza;
- collegamento serializzato con AIL;
- collegamento con validazione, memoria ed errori;
- esempi conformi e non conformi;
- test minimi di conformità.

## 11. Registro modifiche

| Versione | Stato | Modifica |
|---|---|---|
| 0.1 | Draft | Prima formalizzazione del Meta-Modello ricavata esclusivamente dai concetti già consolidati nel repository. |
