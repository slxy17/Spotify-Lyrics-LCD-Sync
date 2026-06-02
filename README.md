# Spotify Lyrics LCD Sync

Sistema che sincronizza i testi di Spotify in tempo reale e li mostra su un display LCD 16x2 collegato ad Arduino tramite comunicazione seriale.

---

# 🚀 Funzionalità

* Rilevamento automatico brano Spotify
* Download testi sincronizzati (LRCLIB)
* Sync real-time con timestamp
* Output su terminale
* Output su LCD 16x2
* Selezione automatica porta seriale
* Salvataggio porta in config
* Gestione overflow testo LCD

---

# 📦 Requisiti

## Hardware

* Arduino Uno / Nano / Mega / ESP32
* Display LCD 16x2 (HD44780)
* Cavo USB

## Software

* Python 3.10+
* Spotify Desktop
* Account Spotify Premium

---

# ⚙️ Installazione

## Clona repository

```bash
git clone https://github.com/slxy17/Spotify-Lyrics-LCD-Sync.git
cd Spotify-Lyrics-LCD-Sync
```

## Installa dipendenze

```bash
pip install -r requirements.txt
```

---

# 🔑 Configurazione Spotify

Creare un’app su:

https://developer.spotify.com/dashboard

Aggiungere redirect URI:

```
http://127.0.0.1:8888/callback
```

---

# 🧩 config.json

Nel progetto è presente `config.json`.

Devi modificare SOLO questi valori:

```json
{
  "client_id": "IL_TUO_CLIENT_ID",
  "client_secret": "IL_TUO_CLIENT_SECRET",
  "redirect_uri": "http://127.0.0.1:8888/callback",
  "port": "COM7"
}
```

---

# 🔌 Gestione porta seriale

All’avvio il programma:

* scansiona le porte disponibili
* mostra dispositivi collegati
* permette selezione manuale
* salva la scelta automaticamente

Selezione esempio:

```
🔌 Porte seriali disponibili:

[1] COM7 - Arduino Uno (COM7)

[0] Usa porta salvata in config
```

---

# ▶️ Avvio

```bash
python main.py
```

Al primo avvio:

* login Spotify nel browser
* selezione porta Arduino

---

# 📡 Protocollo seriale

Formato inviato ad Arduino:

```
linea1|linea2
```

Esempio:

```
hello darkness|my old friend
```

---

# 🧠 Come funziona

1. Connessione Spotify API
2. Lettura brano in riproduzione
3. Download lyrics sincronizzate
4. Parsing timestamp
5. Split testo per LCD 16 caratteri
6. Invio seriale ad Arduino
7. Visualizzazione su LCD

---

# ⚠️ Limitazioni

* non tutti i brani hanno lyrics sincronizzate
* dipendenza da LRCLIB
* LCD limitato a 16 caratteri
* richiede connessione internet

---

# 📜 Licenza

MIT License

Copyright (c) 2026 slxy17

Permesso concesso gratuitamente di usare, copiare, modificare e distribuire il software.
