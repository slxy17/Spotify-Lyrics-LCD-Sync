#include <LiquidCrystal.h> 
// Libreria per controllare display LCD compatibili HD44780 in modalità parallela (4-bit)


// Inizializzazione del display LCD
// Pin collegati: RS=12, E=11, D4=5, D5=4, D6=3, D7=2
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);


// Variabili globali che contengono le due righe da mostrare sul display
String line1 = "";
String line2 = "";


// ================================
// SETUP
// ================================
void setup() {

  // inizializza LCD a 16 colonne e 2 righe
  lcd.begin(16, 2);

  // inizializza comunicazione seriale con PC (Python)
  Serial.begin(115200);

  // pulisce il display all’avvio
  lcd.clear();

  // messaggio iniziale di standby
  lcd.setCursor(0, 0);
  lcd.print("In attesa testo...");
}


// ================================
// LOOP PRINCIPALE
// ================================
void loop() {

  // controlla se arrivano dati dalla seriale USB
  if (Serial.available()) {

    // legge una riga completa fino al carattere '\n'
    String input = Serial.readStringUntil('\n');
    input.trim(); // rimuove spazi e caratteri invisibili

    // se la stringa è vuota, non fa nulla
    if (input.length() == 0) return;

    // ================================
    // PARSING DEL MESSAGGIO
    // ================================

    // formato atteso: "testo1|testo2"
    int delim = input.indexOf('|');

    if (delim >= 0) {
      // parte prima del separatore → prima riga LCD
      line1 = input.substring(0, delim);

      // parte dopo il separatore → seconda riga LCD
      line2 = input.substring(delim + 1);

    } else {
      // se non trova il separatore, usa tutto su una riga
      line1 = input;
      line2 = "";
    }


    // ================================
    // NORMALIZZAZIONE CARATTERI
    // ================================

    // sostituisce caratteri accentati non supportati dal LCD
    // (il controller HD44780 non gestisce bene UTF-8)
    line1.replace("è","e");
    line1.replace("é","e");
    line1.replace("à","a");
    line1.replace("ù","u");
    line1.replace("ò","o");
    line1.replace("ì","i");

    line2.replace("è","e");
    line2.replace("é","e");
    line2.replace("à","a");
    line2.replace("ù","u");
    line2.replace("ò","o");
    line2.replace("ì","i");


    // ================================
    // OUTPUT SU LCD
    // ================================

    // pulisce il display prima di scrivere nuovo testo
    lcd.clear();

    // scrive prima riga
    lcd.setCursor(0,0);
    lcd.print(line1);

    // scrive seconda riga
    lcd.setCursor(0,1);
    lcd.print(line2);
  }
}
