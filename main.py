import requests  # per chiamate HTTP (API LRCLIB)
import os  # per pulizia terminale
import json  # per leggere/salvare config.json
import time  # per delay e timing
import spotipy  # libreria Spotify API
from spotipy.oauth2 import SpotifyOAuth  # autenticazione Spotify
import serial  # comunicazione seriale con Arduino
import serial.tools.list_ports  # scansione porte COM

# ================================
# CONFIG
# ================================

# Carica il file di configurazione JSON
# Contiene credenziali Spotify e porta seriale salvata
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

LCD_BAUD = 115200  # velocità seriale Arduino (deve combaciare col firmware)


# ================================
# SCAN PORTE SERIALI
# ================================

# Restituisce tutte le porte seriali disponibili nel sistema
def list_serial_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports


# Permette all’utente di scegliere la porta seriale Arduino
# e salva automaticamente la scelta nel config.json
def choose_serial_port():
    ports = list_serial_ports()

    # Se non trova porte seriali, esce
    if not ports:
        print("❌ Nessuna porta seriale trovata")
        return None

    print("\n🔌 Porte seriali disponibili:\n")

    # Mostra tutte le porte con descrizione
    for i, p in enumerate(ports, start=1):
        print(f"[{i}] {p.device} - {p.description}")

    print("\n[0] Usa porta salvata in config")

    choice = input("\nSeleziona porta: ")

    # Usa porta già salvata
    if choice == "0":
        return config.get("port")

    try:
        # Converte scelta utente in indice lista
        selected = ports[int(choice) - 1].device

        # Aggiorna config con nuova porta
        config["port"] = selected

        # Salva su file config.json
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        print(f"✔ Porta salvata: {selected}")

        return selected

    except:
        # fallback se input errato
        print("❌ Scelta non valida, uso config")
        return config.get("port")


# Avvio selezione porta seriale
LCD_PORT = choose_serial_port()

print(f"\nConnessione LCD su: {LCD_PORT}")

# (nota: qui sotto c’era un bug logico nel tuo codice originale:
# LCD_PORT veniva riassegnato da config ignorando la scelta utente)

LCD_BAUD = 115200  # ridichiarato (ridondante ma non critico)


# ================================
# LCD SERIAL
# ================================

# Apertura connessione seriale con Arduino
try:
    lcd_ser = serial.Serial(LCD_PORT, LCD_BAUD)
    time.sleep(2)  # tempo di reset Arduino
except Exception as e:
    print("⚠ LCD non connesso:", e)
    lcd_ser = None  # fallback: il programma continua senza LCD


# ================================
# SPOTIFY
# ================================

# Crea client Spotify autenticato
def connect_spotify():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            redirect_uri=config["redirect_uri"],
            scope="user-read-currently-playing user-read-playback-state"
        )
    )


# ================================
# SPLIT TESTO PER LCD (16 CARATTERI)
# ================================

# Divide una frase lunga in blocchi compatibili con LCD 16x2
# Evita di spezzare parole quando possibile
def split_line_by_16_chars(line, max_len=16):
    words = line.split()
    chunks = []
    current = ""

    for w in words:
        # se parola troppo lunga, la manda da sola
        if len(w) > max_len:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(w)
            continue

        # se supera limite riga, chiude e apre nuova riga
        if len(current) + len(w) + (1 if current else 0) > max_len:
            chunks.append(current)
            current = w
        else:
            # aggiunge parola alla riga corrente
            current = w if not current else current + " " + w

    # aggiunge ultimo buffer rimasto
    if current:
        chunks.append(current)

    return chunks


# ================================
# UI TERMINALE
# ================================

# Pulisce e stampa lo stato attuale del sistema
def print_screen(title, artist, l1="", l2="", pos=None):
    os.system("cls" if os.name == "nt" else "clear")

    print("🎧 SPOTIFY LYRICS SYNC")
    print("────────────────────────────")

    # informazioni brano
    print(f"▶ {title}")
    print(f"👤 {artist}")

    # timestamp riproduzione
    if pos is not None:
        mm = int(pos // 60)
        ss = int(pos % 60)
        print(f"⏱ {mm:02d}:{ss:02d}")

    print("────────────────────────────")

    # testo LCD simulato su terminale
    if l1 or l2:
        print(f"{l1:<16}")
        print(f"{l2:<16}")
    else:
        print("...")

    print("────────────────────────────")


# ================================
# LYRICS FETCH (LRCLIB)
# ================================

# Scarica e processa lyrics sincronizzate
def fetch_lyrics(track_name, artist_name, duration_sec, sp, track_id):
    print(f"Canzone rilevata: {track_name}")
    print(f"Artista rilevato: {artist_name}")
    print("🔍 ricerca lyrics...")

    # richiesta API LRCLIB
    url = f"https://lrclib.net/api/search?q={track_name}%20{artist_name}"
    res = requests.get(url)

    if res.status_code != 200:
        print("errore API")
        return None

    # controllo che la canzone sia ancora quella attuale
    current = sp.current_user_playing_track()
    if not current or current["item"]["id"] != track_id:
        return None

    data = res.json()

    # selezione canzone giusta tra i risultati
    track = next(
        (t for t in data
         if t.get("syncedLyrics")
         and abs(round(t.get("duration", 0)) - round(duration_sec)) <= 2),
        None
    )

    if not track:
        print("lyrics non trovate")
        return None

    lines = track["syncedLyrics"].split("\n")

    formatted = []

    # parsing timestamp + testo
    for line in lines:
        if not line.startswith("["):
            continue

        try:
            ts = line[1:9]  # formato [mm:ss.xx]
            m, s = ts.split(":")
            total = int(m) * 60 + float(s)

            text = line[10:].strip()

            # split per LCD
            chunks = split_line_by_16_chars(text)

            formatted.append((total, chunks))

        except:
            continue

    return formatted


# ================================
# MAIN LOOP
# ================================

def main():
    sp = connect_spotify()

    last_track_id = None
    lyrics = None
    last_ts = None

    while True:

        # lettura stato Spotify
        current = sp.current_user_playing_track()

        # se non sta suonando nulla
        if not current or not current.get("is_playing"):
            print_screen("...", "nessuna riproduzione")
            time.sleep(1)
            continue

        item = current["item"]

        # dati brano
        title = item["name"]
        artist = item["artists"][0]["name"]
        duration_sec = item["duration_ms"] / 1000
        pos_sec = current["progress_ms"] / 1000
        track_id = item["id"]

        # se cambia canzone → ricarica lyrics
        if track_id != last_track_id:
            last_track_id = track_id
            lyrics = fetch_lyrics(title, artist, duration_sec, sp, track_id)
            last_ts = None

        if not lyrics:
            print_screen(title, artist, "no lyrics", "", pos_sec)
            time.sleep(0.2)
            continue

        active = None
        current_ts = None
        next_ts = None

        # trova riga attuale in base al tempo
        for i, (ts, chunks) in enumerate(lyrics):
            if pos_sec >= ts:
                active = chunks
                current_ts = ts
                next_ts = lyrics[i + 1][0] if i + 1 < len(lyrics) else None

        if not active:
            print_screen(title, artist, "...", "", pos_sec)
            time.sleep(0.2)
            continue

        # evita aggiornamenti duplicati
        if current_ts == last_ts:
            time.sleep(0.1)
            continue

        last_ts = current_ts

        # tempo disponibile per animazione testo
        available = max(0.5, next_ts - pos_sec) if next_ts else 5

        # divide blocchi in coppie (2 righe LCD)
        pairs = [
            (active[i], active[i + 1] if i + 1 < len(active) else "")
            for i in range(0, len(active), 2)
        ]

        delay = available / len(pairs) if pairs else 1

        # loop visualizzazione LCD
        for i, (l1, l2) in enumerate(pairs):

            # sicurezza lunghezza LCD
            l1 = l1[:16]
            l2 = l2[:16]

            print_screen(title, artist, l1, l2, pos_sec)

            # invio ad Arduino
            if lcd_ser:
                lcd_ser.write(f"{l1}|{l2}\n".encode("utf-8"))

            # timing tra frame testo
            if i < len(pairs) - 1:
                time.sleep(delay)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
