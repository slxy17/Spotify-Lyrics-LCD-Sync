# Spotify Lyrics LCD Sync

Sistema per la visualizzazione in tempo reale dei testi sincronizzati di Spotify su un display LCD 16x2 collegato ad Arduino tramite comunicazione seriale.

Il software rileva automaticamente il brano in riproduzione su Spotify, scarica i testi sincronizzati tramite LRCLIB e li visualizza sia nel terminale che sul display LCD.

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
* Sincronizzazione dei testi basata sui timestamp

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
* Arduino IDE (per il caricamento del firmware)

---

# Installazione

## Clonazione del repository

```bash
git clone https://github.com/slxy17/Spotify-Lyrics-LCD-Sync.git
cd Spotify-Lyrics-LCD-Sync
```

## Installazione delle dipendenze

```bash
pip install -r requirements.txt
```

---

# Configurazione Spotify

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

# Configurazione del file config.json

Nella cartella principale del progetto è presente il file:

```text
config.json
```

con il seguente contenuto:

```json
{
    "client_id": "IL_TUO_CLIENT_ID",
    "client_secret": "IL_TUO_CLIENT_SECRET",
    "redirect_uri": "http://127.0.0.1:8888/callback"
}
```

Prima di eseguire il programma è necessario sostituire:

* `IL_TUO_CLIENT_ID` con il Client ID della propria applicazione Spotify;
* `IL_TUO_CLIENT_SECRET` con il Client Secret della propria applicazione Spotify.

Il valore di `redirect_uri` deve coincidere con quello configurato nella Dashboard Spotify.

---

# Configurazione della porta seriale

Nel file `main.py` è presente la seguente configurazione:

```python
LCD_PORT = "COM7"
LCD_BAUD = 115200
```

Modificare il valore di `LCD_PORT` inserendo la porta COM utilizzata dal proprio Arduino.

Esempi:

```python
LCD_PORT = "COM3"
```

```python
LCD_PORT = "COM5"
```

```python
LCD_PORT = "COM12"
```

Per verificare la porta assegnata ad Arduino:

### Windows

1. Aprire Gestione Dispositivi.
2. Espandere la sezione "Porte (COM e LPT)".
3. Individuare la porta associata ad Arduino.

### Linux

```bash
ls /dev/tty*
```

### macOS

```bash
ls /dev/cu.*
```

La velocità seriale deve rimanere impostata a:

```python
LCD_BAUD = 115200
```

e deve corrispondere a quella utilizzata nel firmware Arduino.

---

# Caricamento del firmware Arduino

Aprire il file `.ino` con Arduino IDE e caricarlo sulla scheda.

Il firmware ha il compito di:

* ricevere i dati inviati dal software Python;
* interpretare il protocollo seriale;
* aggiornare il display LCD;
* sostituire automaticamente i caratteri accentati non supportati dal controller HD44780.

All'avvio il display mostrerà:

```text
In attesa testo...
```

finché non verrà ricevuto il primo messaggio dal programma Python.

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
3. Download dei testi sincronizzati tramite LRCLIB.
4. Elaborazione dei timestamp.
5. Suddivisione automatica del testo in righe da 16 caratteri.
6. Invio delle informazioni ad Arduino tramite seriale.
7. Aggiornamento del display LCD.
8. Aggiornamento automatico in caso di cambio brano.

---

# Protocollo di comunicazione seriale

Il software invia i dati nel seguente formato:

```text
riga1|riga2
```

Esempio:

```text
Hello darkness|my old friend
```

Dove:

* il testo prima del carattere `|` viene visualizzato sulla prima riga del display;
* il testo dopo il carattere `|` viene visualizzato sulla seconda riga del display.

---

# Gestione dei testi

Poiché il display LCD dispone di 16 caratteri per riga, il software:

* divide automaticamente le frasi lunghe;
* evita di spezzare le parole quando possibile;
* distribuisce il testo su più schermate se necessario;
* sincronizza la visualizzazione con il tempo di riproduzione del brano.

---

# Dipendenze

Il progetto utilizza le seguenti librerie Python:

* Spotipy
* Requests
* PySerial

Le dipendenze sono installabili tramite il file `requirements.txt`.

---

# Limitazioni

* Non tutti i brani dispongono di testi sincronizzati su LRCLIB.
* La precisione della sincronizzazione dipende dai dati forniti da LRCLIB.
* Alcuni caratteri speciali potrebbero non essere supportati dal display LCD.
* È richiesta una connessione Internet attiva.
* È consigliato utilizzare Spotify Premium per ottenere una sincronizzazione più affidabile.

---

# Licenza

Questo progetto è distribuito sotto licenza MIT.

La licenza MIT consente di utilizzare, modificare, distribuire e pubblicare il software anche per scopi commerciali, purché venga mantenuto il testo della licenza originale e il relativo copyright.

Per maggiori informazioni consultare il file `LICENSE` presente nel repository.
