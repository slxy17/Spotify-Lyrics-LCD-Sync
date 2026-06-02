# Spotify-Lyrics-LCD-Sync
Sistema per la visualizzazione in tempo reale dei testi sincronizzati di Spotify su un display LCD 16x2 collegato ad Arduino.
# Spotify Lyrics LCD Sync

Sistema per la visualizzazione in tempo reale dei testi sincronizzati di Spotify su un display LCD 16x2 collegato ad Arduino.

Il software rileva automaticamente il brano in riproduzione su Spotify, scarica i testi sincronizzati tramite LRCLIB e li visualizza sia nel terminale che su un display LCD esterno tramite comunicazione seriale.

---

# Caratteristiche

* Rilevamento automatico del brano in riproduzione
* Download automatico dei testi sincronizzati
* Cambio automatico del brano
* Supporto display LCD 16x2
* Comunicazione seriale con Arduino
* Interfaccia terminale in tempo reale
* Gestione automatica delle righe lunghe
* Compatibilità con Spotify Desktop

---

# Requisiti Hardware

## Computer

* Windows, Linux o macOS
* Connessione Internet
* Porta USB disponibile

## Microcontrollore

Compatibile con:

* Arduino Uno
* Arduino Nano
* Arduino Mega
* ESP32
* Schede compatibili Arduino

## Display

* LCD 16x2 compatibile HD44780

---

# Requisiti Software

* Python 3.10 o superiore
* Spotify Desktop installato
* Account Spotify Premium
* Arduino IDE (per il firmware LCD)

---

# Installazione

## 1. Clonazione repository

```bash
git clone https://github.com/NOMEUTENTE/spotify-lyrics-lcd.git
cd spotify-lyrics-lcd
```

## 2. Installazione dipendenze

```bash
pip install -r requirements.txt
```

## 3. Creazione applicazione Spotify

Accedere al portale Spotify for Developers:

https://developer.spotify.com/dashboard

Creare una nuova applicazione e ottenere:

* Client ID
* Client Secret

Aggiungere il seguente Redirect URI:

```text
http://127.0.0.1:8888/callback
```

---

# Configurazione

Creare un file denominato:

```text
config.json
```

con il seguente contenuto:

```json
{
    "client_id": "INSERIRE_CLIENT_ID",
    "client_secret": "INSERIRE_CLIENT_SECRET",
    "redirect_uri": "http://127.0.0.1:8888/callback"
}
```

---

# Avvio del programma

```bash
python main.py
```

Al primo avvio verrà aperto automaticamente il browser per autorizzare l'accesso all'account Spotify.

Una volta completata l'autenticazione, il programma inizierà a monitorare il brano in riproduzione.

---

# Funzionamento

Il software esegue il seguente flusso operativo:

1. Connessione alle API Spotify.
2. Rilevamento del brano in riproduzione.
3. Download dei testi sincronizzati da LRCLIB.
4. Elaborazione dei timestamp.
5. Suddivisione automatica del testo in righe compatibili con il display.
6. Invio delle informazioni ad Arduino tramite seriale.
7. Aggiornamento del display LCD.

---

# Comunicazione Seriale

Il software invia una riga nel formato:

```text
riga1|riga2
```

Esempio:

```text
Hello darkness|my old friend
```

Il carattere "|" viene utilizzato come separatore tra la prima e la seconda riga del display.

---

# Gestione dei Testi

Poiché il display dispone di soli 16 caratteri per riga, il software:

* divide automaticamente le frasi lunghe;
* evita di spezzare le parole quando possibile;
* distribuisce il testo su più schermate se necessario;
* sincronizza la visualizzazione con i timestamp del brano.

---

# Dipendenze

* Spotipy
* Requests
* PySerial

---

# Limitazioni

* Non tutti i brani dispongono di testi sincronizzati.
* La qualità della sincronizzazione dipende dai dati forniti da LRCLIB.
* Alcuni caratteri speciali potrebbero non essere supportati dal display LCD.
* È richiesta una connessione Internet attiva.

---

# Licenza

Distribuito sotto licenza MIT.
