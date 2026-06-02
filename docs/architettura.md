# Architettura del sistema

Questo documento descrive la struttura interna e il flusso dati del progetto Spotify Lyrics LCD Sync.

---

# Panoramica

Il sistema è composto da tre livelli principali:

1. Spotify API (acquisizione dati brano)
2. Motore Lyrics (recupero e sincronizzazione testi)
3. Output hardware (Arduino + LCD)

---

# Componenti principali

## 1. Spotify Layer (Python - Spotipy)

Questo modulo si occupa di:

- autenticazione con Spotify
- lettura del brano attualmente in riproduzione
- acquisizione di:
  - titolo
  - artista
  - durata
  - progressione del brano

Output:
→ dati del brano in tempo reale

---

## 2. Lyrics Engine (LRCLIB)

Questo modulo:

- invia richiesta HTTP a LRCLIB
- cerca i testi del brano
- seleziona la versione con timestamp
- filtra in base alla durata del brano

Output:
→ lista di righe sincronizzate con timestamp

Esempio struttura interna:
```python
[
    (12.5, ["hello darkness"]),
    (15.0, ["my old friend"])
]```
---

## 3. Display Layer (Arduino + LCD)

Questo modulo:

- riceve dati dalla seriale USB
- interpreta il formato `riga1|riga2`
- aggiorna il display LCD 16x2
- gestisce caratteri non supportati

Output:
→ visualizzazione fisica su LCD

---

# Flusso dei dati
Spotify API
    ↓
Python (main.py)
    ↓
LRCLIB API
    ↓
Parsing + sincronizzazione timestamp
    ↓
Seriale USB (PySerial)
    ↓
Arduino
    ↓
LCD 16x2

# Logica di sincronizzazione

Il sistema utilizza il tempo di riproduzione del brano:

- `progress_ms` (Spotify)
- confronto con timestamp delle lyrics
- aggiornamento quando viene raggiunto il tempo corretto

Questo permette una sincronizzazione quasi reale.

---

# Struttura software

## main.py

Contiene tutta la logica principale:

- connessione Spotify
- gestione loop principale
- richiesta lyrics
- sincronizzazione
- invio dati ad Arduino

---

## Librerie utilizzate

- spotipy → Spotify API
- requests → HTTP LRCLIB
- pyserial → comunicazione Arduino
- json → configurazione

---

# Design del sistema

Il progetto è progettato con un approccio:

- modulare
- event-driven (basato sul brano in riproduzione)
- realtime (aggiornamento continuo)

---

# Obiettivo

Creare un sistema fisico che:

- visualizza i testi Spotify in tempo reale
- sincronizza audio e testo
- usa hardware economico (Arduino + LCD)

---

# Limiti architetturali

- dipendenza da LRCLIB per i testi
- latenza variabile API Spotify
- precisione non perfetta al millisecondo
- LCD limitato a 16 caratteri per riga

---

# Possibili miglioramenti futuri

- caching locale dei testi
- fallback API lyrics alternative
- miglior algoritmo di sync
- supporto OLED display
- buffering seriale ottimizzato
