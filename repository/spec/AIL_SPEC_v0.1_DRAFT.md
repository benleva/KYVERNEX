# AIL SPECIFICATION

**Titolo:** ARGUS Intermediate Language (AIL)  
**Versione:** 0.2 Draft  
**Stato:** incompleto, non implementabile  
**Progetto:** Matrice ARGUS / Kernel KYVERNEX  
**Autore del progetto:** Andrea Pernarcic

## 1. Scopo

AIL è il linguaggio interno della Matrice ARGUS. Deve rappresentare le informazioni in una forma strutturata, neutrale e indipendente dal linguaggio di origine, affinché il kernel KYVERNEX possa elaborarle in modo uniforme.

AIL deve rappresentare le categorie registrate nel `METAMODEL_SPEC_v0.1_DRAFT.md` senza fonderle o riclassificarle silenziosamente.

## 2. Requisiti consolidati

AIL deve:

1. essere indipendente dalla lingua naturale;
2. essere strutturato secondo regole formali;
3. essere compatibile con il Contratto Cognitivo Universale (CCU);
4. essere utilizzabile da tutti i moduli della Matrice ARGUS;
5. separare il significato dell'informazione dalla sua forma espressiva;
6. mantenere il collegamento con l'informazione originale;
7. consentire tracciabilità, verifica e ricostruzione delle trasformazioni;
8. mantenere distinti dati, regole, inferenze e risultati;
9. supportare gli stati cognitivi definiti dalla Matrice ARGUS;
10. consentire l'uso degli operatori formali Φ, Ω, Λ, Σ, V, μ e Δ;
11. dichiarare la categoria dell'oggetto cognitivo quando conosciuta;
12. essere compatibile con il Meta-Modello Cognitivo ARGUS.

## 3. Collocazione architetturale

Flusso consolidato:

`Input → AET → AIL → Kernel KYVERNEX → Validazione → Output`

AET riceve e normalizza l'input esterno. AIL fornisce la rappresentazione interna condivisa. KYVERNEX applica regole, verifiche e inferenze.

Il Meta-Modello definisce quali categorie strutturali AIL deve poter rappresentare; AIL ne definirà la sintassi e la serializzazione.

## 4. Elementi minimi da rappresentare

Ogni unità AIL dovrà poter conservare almeno:

- un'identità univoca nel proprio contesto;
- la categoria prevista dal Meta-Modello, quando determinabile;
- il riferimento al contenuto originale;
- la fonte o origine;
- le entità cognitive coinvolte;
- le relazioni tra le entità;
- lo stato cognitivo corrente;
- le trasformazioni applicate;
- le regole utilizzate;
- il risultato prodotto;
- gli esiti di validazione;
- la versione dell'oggetto o della rappresentazione;
- le informazioni necessarie alla verifica e alla ricostruzione del processo.

## 5. Categorie del Meta-Modello da supportare

AIL dovrà poter distinguere almeno:

- Entità Cognitiva;
- Dato;
- Fatto;
- Ipotesi;
- Deduzione;
- Opinione;
- Regola;
- Assioma;
- Meta-Regola;
- Relazione;
- Trasformazione;
- Risultato;
- Fonte o Origine;
- Stato Cognitivo;
- Validazione;
- Errore.

La codifica concreta di queste categorie non è ancora definita.

## 6. Stati cognitivi supportati

Gli stati consolidati sono:

1. `ACQUISITO`
2. `NORMALIZZATO`
3. `ELABORATO`
4. `VALIDATO`
5. `CONSOLIDATO`

La specifica degli stati negativi o di eccezione non è ancora definita.

## 7. Operatori formali supportati

- `Φ` identificazione dell'entità o del concetto;
- `Ω` risultato o stato finale;
- `Λ` relazione o collegamento;
- `Σ` aggregazione o composizione;
- `V` validazione e verifica;
- `μ` memoria e recupero;
- `Δ` variazione, trasformazione o cambiamento di stato.

Le firme, i parametri, la precedenza e le regole di composizione degli operatori non sono ancora definite.

## 8. Vincoli normativi

Una rappresentazione AIL valida deve:

- preservare l'integrità dell'informazione ricevuta;
- registrare ogni trasformazione;
- consentire la ricostruzione del percorso logico;
- non confondere dati, regole, inferenze e risultati;
- non fondere silenziosamente fatto, ipotesi, deduzione e opinione;
- rispettare il Meta-Modello, gli assiomi, le regole fondamentali e le meta-regole;
- poter essere sottoposta a validazione senza modificare i dati originali.

## 9. Componenti ancora da definire

La presente versione non definisce ancora:

- grammatica formale;
- sintassi concreta;
- formato di serializzazione;
- tipi di dato;
- campi obbligatori e facoltativi;
- schema serializzato dell'Entità Cognitiva;
- schema delle relazioni;
- cardinalità;
- gestione degli errori;
- stati negativi e di eccezione;
- regole di composizione degli operatori;
- compatibilità tra versioni AIL e Meta-Modello;
- esempi validi e non validi;
- parser e validatore di riferimento.

## 10. Criterio di completamento

AIL potrà passare da `Draft` a `Alpha` soltanto quando saranno definite e testabili:

1. grammatica;
2. sintassi;
3. schema dati conforme al Meta-Modello;
4. operatori;
5. errori;
6. validazione;
7. compatibilità di versione;
8. almeno un esempio completo dalla ricezione dell'input alla restituzione dell'output.

## 11. Dipendenze

- `METAMODEL_SPEC_v0.1_DRAFT.md`;
- CCU_SPEC;
- OPERATORS_SPEC;
- CORE_SPEC;
- VALIDATION_PROTOCOL;
- ERROR_MODEL.

## 12. Registro modifiche

| Versione | Stato | Modifica |
|---|---|---|
| 0.1 | Draft | Prima struttura della specifica AIL ricavata dai requisiti consolidati del repository. |
| 0.2 | Draft | Collegamento normativo con il Meta-Modello Cognitivo e registrazione delle categorie minime da rappresentare. |
