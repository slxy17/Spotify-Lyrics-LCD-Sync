
# Hardware del progetto

---

## Componenti necessari

### Microcontrollore

- Arduino Uno (consigliato)
- Arduino Nano
- Arduino Mega
- ESP32

---

### Display

- LCD 16x2 (HD44780)
- Modalità 4-bit

---

## Collegamenti LCD → Arduino

<img width="400" align="center" alt="Screenshot 2026-06-02 130538" src="https://github.com/user-attachments/assets/a260541a-03eb-4db4-8857-6292a360d405" />


| LCD | Arduino |
|-----|--------|
| RS  | 12 |
| E   | 11 |
| D4  | 5 |
| D5  | 4 |
| D6  | 3 |
| D7  | 2 |

---

## Comunicazione seriale

- Baud rate: 115200
- USB diretta da PC

Formato:  
riga1|riga2

---

## Schema logico

PC → USB → Arduino → LCD

---

## Note importanti

- Il contrasto LCD va regolato con potenziometro
- Alimentazione 5V stabile consigliata
- Se il display è vuoto → controllare wiring
