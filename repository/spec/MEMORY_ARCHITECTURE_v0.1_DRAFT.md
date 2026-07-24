# MEMORY_ARCHITECTURE v0.2 DRAFT

Stato: DRAFT  
Versione: 0.2  
Ambito: Matrice ARGUS / Kernel KYVERNEX

## 1. Scopo

Definire l'architettura preliminare della memoria della Matrice ARGUS e del kernel KYVERNEX, senza introdurre comportamenti non ancora consolidati.

La memoria deve conservare oggetti e categorie coerenti con `METAMODEL_SPEC_v0.1_DRAFT.md`.

## 2. Elementi consolidati

- La memoria è parte integrante del kernel KYVERNEX.
- CORE-006 è il modulo responsabile della gestione della memoria e della persistenza delle informazioni.
- L'operatore μ è associato alla memoria e al recupero delle informazioni rilevanti.
- La memoria deve rispettare il Contratto Cognitivo Universale (CCU).
- Ogni informazione memorizzata deve mantenere identità, categoria, origine e tracciabilità.
- Ogni trasformazione applicata a un contenuto memorizzato deve essere ricostruibile.
- La memoria deve essere compatibile con AIL e con il Meta-Modello Cognitivo.
- Le informazioni consolidate possono essere utilizzate come base per elaborazioni successive.
- Fatto, ipotesi, deduzione e opinione non devono essere fusi silenziosamente durante persistenza o recupero.

## 3. Responsabilità minime di CORE-006

CORE-006 deve almeno:

- ricevere informazioni candidate alla persistenza;
- preservarne l'identità e la categoria cognitiva;
- mantenere il collegamento con la fonte e con le trasformazioni subite;
- consentirne il recupero;
- distinguere i contenuti consolidati da quelli non ancora validati;
- conservare il collegamento con gli esiti di validazione;
- operare senza alterare i dati originali;
- comunicare con gli altri moduli secondo il CCU.

## 4. Oggetti minimi da poter conservare

In coerenza con il Meta-Modello, la memoria dovrà poter conservare o referenziare almeno:

- Entità Cognitive;
- Dati;
- Fatti;
- Ipotesi;
- Deduzioni;
- Opinioni;
- Regole, Assiomi e Meta-Regole;
- Relazioni;
- Trasformazioni;
- Risultati;
- Fonti o Origini;
- Stati Cognitivi;
- Validazioni;
- Errori.

Lo schema dei record non è ancora definito.

## 5. Relazione con gli Stati Cognitivi

La memoria deve poter registrare almeno i seguenti stati già consolidati:

1. Acquisito
2. Normalizzato
3. Elaborato
4. Validato
5. Consolidato

La persistenza non modifica automaticamente lo stato cognitivo dell'informazione.

## 6. Relazione con μ

μ rappresenta l'operatore associato alla memoria e al recupero delle informazioni rilevanti.

Non sono ancora definiti:

- firma formale;
- dominio e codominio;
- criteri di rilevanza;
- sintassi AIL;
- errori;
- comportamento in presenza di più risultati;
- filtri per categoria cognitiva;
- comportamento in presenza di versioni differenti dello stesso oggetto.

## 7. Vincoli normativi

La memoria deve rispettare:

- integrità;
- tracciabilità;
- verificabilità;
- separazione tra dati, regole, inferenze e risultati;
- separazione tra fatto, ipotesi, deduzione e opinione;
- compatibilità con il Meta-Modello e con l'architettura esistente;
- documentazione e versionamento delle modifiche.

## 8. Parti non ancora definite

TODO:

- modello interno della memoria;
- tipologie di memoria;
- schema dei record conforme al Meta-Modello;
- criteri di persistenza;
- politiche di consolidamento;
- politiche di cancellazione;
- indicizzazione;
- recupero e ranking;
- gestione dei conflitti;
- gestione delle versioni;
- gestione dell'obsolescenza;
- politiche di isolamento tra contesti;
- API di CORE-006;
- errori e stati negativi;
- requisiti di sicurezza;
- test di conformità.

## 9. Criteri per il passaggio ad Alpha

Il documento potrà passare da DRAFT ad ALPHA quando saranno definiti e approvati:

- struttura dei dati memorizzati conforme al Meta-Modello;
- interfacce di CORE-006;
- comportamento di μ;
- regole di persistenza e recupero;
- gestione degli errori;
- invarianti;
- test minimi di conformità.

## 10. Dipendenze

- `METAMODEL_SPEC_v0.1_DRAFT.md`;
- AIL_SPEC;
- CCU_SPEC;
- OPERATORS_SPEC;
- CORE_SPEC;
- Stati Cognitivi;
- Regole di Validazione.

## 11. Registro modifiche

| Versione | Stato | Modifica |
|---|---|---|
| 0.1 | Draft | Prima struttura della memoria ricavata dai requisiti consolidati. |
| 0.2 | Draft | Collegamento al Meta-Modello Cognitivo e registrazione delle categorie minime conservabili. |

## 12. Stato del documento

Questo file organizza esclusivamente gli elementi già consolidati e marca come TODO tutte le parti ancora mancanti.
