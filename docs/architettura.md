
# Architettura del sistema

Questo documento descrive la struttura interna e il flusso dati del progetto Spotify Lyrics LCD Sync.

---

# Panoramica

Il sistema è composto da tre livelli principali:

1. Acquisizione dati Spotify
2. Recupero e sincronizzazione lyrics
3. Output su hardware (Arduino + LCD)

---

# Componenti principali

## 1. Spotify Layer (Spotipy)

Questo modulo gestisce la comunicazione con le API Spotify.

### Funzioni principali:
- autenticazione utente
- rilevamento brano in riproduzione
- acquisizione dati del brano:
  - titolo
  - artista
  - durata
  - progressione (timestamp corrente)

### Output:
→ dati del brano in tempo reale

---

## 2. Lyrics Engine (LRCLIB)

Questo modulo si occupa del recupero dei testi sincronizzati.

### Funzioni principali:
- richiesta HTTP a LRCLIB
- ricerca del brano tramite titolo e artista
- selezione versione con timestamp
- filtro basato sulla durata del brano

### Output:
→ lista di tuple sincronizzate

Esempio struttura dati:  
[  
    (12.5, ["hello darkness"]),  
    (15.0, ["my old friend"])  
]  


---

## 3. Display Layer (Arduino + LCD)

Questo modulo gestisce la parte hardware.

### Funzioni principali:

* ricezione dati via seriale USB
* parsing formato `riga1|riga2`
* aggiornamento LCD 16x2
* gestione caratteri non supportati

### Output:

→ visualizzazione fisica del testo sul display

---

# Flusso dei dati

Il sistema segue questo flusso:

Spotify API  
&emsp↓  
Python (main.py)  
&emsp↓  
LRCLIB API  
&emsp↓  
Parsing + sincronizzazione timestamp  
&emsp↓  
Seriale USB (PySerial)  
&emsp↓  
Arduino  
&emsp↓  
LCD 16x2  


---

# Logica di sincronizzazione

La sincronizzazione si basa sul tempo di riproduzione del brano:

* `progress_ms` fornito da Spotify
* confronto con timestamp delle lyrics
* aggiornamento quando il tempo corrente supera il timestamp della riga

Risultato:
→ sincronizzazione quasi real-time tra audio e testo

---

# Struttura software

## main.py

File principale del progetto.

### Responsabilità:

* gestione Spotify API
* loop principale del programma
* recupero lyrics
* sincronizzazione tempo-testo
* invio dati ad Arduino

---

## Librerie utilizzate

* spotipy → API Spotify
* requests → chiamate HTTP (LRCLIB)
* pyserial → comunicazione seriale con Arduino
* json → gestione configurazione

---

# Design del sistema

Il progetto è basato su:

* architettura modulare
* approccio event-driven (cambio brano)
* esecuzione realtime
* pipeline dati lineare

---

# Obiettivo

Creare un sistema fisico che:

* mostra lyrics Spotify in tempo reale
* sincronizza audio e testo
* utilizza hardware economico (Arduino + LCD 16x2)

---

# Limitazioni

* non tutti i brani hanno lyrics sincronizzate
* dipendenza da LRCLIB
* latenza variabile delle API Spotify
* precisione non perfetta al millisecondo
* limite fisico LCD (16 caratteri per riga)

---

# Possibili miglioramenti

* caching locale delle lyrics
* fallback a più API lyrics
* algoritmo di sincronizzazione più preciso
* supporto OLED / display più grandi
* ottimizzazione buffer seriale

