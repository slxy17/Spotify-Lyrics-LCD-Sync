
````md
# Spotify Lyrics LCD Sync

Sistema per la visualizzazione in tempo reale dei testi sincronizzati di Spotify su un display LCD 16x2 collegato ad Arduino tramite comunicazione seriale.

Il software rileva automaticamente il brano in riproduzione su Spotify, scarica i testi sincronizzati tramite LRCLIB e li mostra sia nel terminale che sul display LCD.

---

# Caratteristiche

- Rilevamento automatico del brano in riproduzione
- Download dei testi sincronizzati
- Cambio automatico del brano
- Supporto display LCD 16x2
- Comunicazione seriale con Arduino
- Interfaccia terminale in tempo reale
- Gestione automatica delle righe da 16 caratteri
- Compatibilità con Spotify Desktop
- Sincronizzazione basata su timestamp

---

# Requisiti Hardware

## Computer

- Windows, Linux o macOS
- Connessione Internet
- Porta USB disponibile

## Microcontrollore

Compatibile con:

- Arduino Uno
- Arduino Nano
- Arduino Mega
- ESP32
- Schede compatibili Arduino

## Display

- LCD 16x2 (HD44780)

---

# Requisiti Software

- Python 3.10 o superiore
- Spotify Desktop installato
- Account Spotify Premium
- Arduino IDE (per caricare il firmware)

---

# Installazione

## Clonazione del repository

```bash
git clone https://github.com/slxy17/Spotify-Lyrics-LCD-Sync.git
cd Spotify-Lyrics-LCD-Sync
````

## Installazione dipendenze

```bash
pip install -r requirements.txt
```

---

# Configurazione Spotify

Accedere al portale:

[https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

Creare una nuova applicazione e ottenere:

* Client ID
* Client Secret

Aggiungere il Redirect URI:

```text
http://127.0.0.1:8888/callback
```

---

# Configurazione `config.json`

Nel progetto è presente il file:

```text
config.json
```

Contenuto:

```json
{
    "client_id": "IL_TUO_CLIENT_ID",
    "client_secret": "IL_TUO_CLIENT_SECRET",
    "redirect_uri": "http://127.0.0.1:8888/callback"
}
```

Prima di eseguire il programma:

* sostituire `IL_TUO_CLIENT_ID`
* sostituire `IL_TUO_CLIENT_SECRET`

Il `redirect_uri` deve coincidere con quello configurato su Spotify Developer Dashboard.

---

# Configurazione porta seriale

Il programma seleziona automaticamente la porta seriale Arduino all’avvio.

Se necessario, è possibile modificarla nel file `config.json` oppure tramite il menu di selezione integrato.

La velocità seriale deve rimanere:

```python
115200
```

---

# Caricamento firmware Arduino

Aprire il file `.ino` con Arduino IDE e caricarlo sulla scheda.

Il firmware:

* riceve i dati via seriale
* interpreta il protocollo `riga1|riga2`
* aggiorna il display LCD
* sostituisce automaticamente i caratteri accentati non supportati

All’avvio il display mostra:

```text
In attesa testo...
```

---

# Avvio del programma

```bash
python main.py
```

Al primo avvio:

* si aprirà il browser per l’autenticazione Spotify
* verrà selezionata la porta seriale Arduino

---

# Funzionamento

1. Connessione alle API Spotify
2. Lettura brano in riproduzione
3. Download testi sincronizzati da LRCLIB
4. Parsing timestamp
5. Suddivisione testo per LCD (16 caratteri)
6. Invio dati ad Arduino
7. Aggiornamento display LCD

---

# Protocollo seriale

Formato inviato:

```text
riga1|riga2
```

Esempio:

```text
Hello darkness|my old friend
```

* prima parte → riga 1 LCD
* seconda parte → riga 2 LCD

---

# Gestione testo

Il software:

* divide automaticamente le righe lunghe
* evita di spezzare parole quando possibile
* sincronizza il testo con il tempo del brano
* adatta tutto al limite di 16 caratteri

---

# Dipendenze

* spotipy
* requests
* pyserial

Installabili con:

```bash
pip install -r requirements.txt
```

---

# Limitazioni

* non tutti i brani hanno lyrics sincronizzate
* dipendenza da LRCLIB
* LCD limitato a 16 caratteri
* richiede connessione Internet
* consigliato Spotify Premium

---

# Licenza

Questo progetto è distribuito sotto licenza MIT.

La licenza MIT consente l’uso, modifica e distribuzione del software anche per scopi commerciali, purché venga mantenuto il copyright originale.

Per maggiori dettagli consultare il file `LICENSE`.

```

---

## 🔥 Se vuoi prossimo upgrade serio posso farti:

- README con badge GitHub (Python, MIT, status build)
- screenshot section + GIF animata
- diagramma architettura
- versione “pro repo” stile 1k+ stars
- oppure ottimizzazione codice (ora è ancora migliorabile parecchio in sync e performance)

Dimmi.
```
