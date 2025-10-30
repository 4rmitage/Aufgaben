# Listen zum Speichern der Einnahmen und Ausgaben
einnahmen = []
ausgaben = []

def einnahme_hinzufuegen():
    while True:
        try:
            betrag = float(input("Geben Sie die Einnahme ein (positive Zahl): "))
            if betrag > 0:
                einnahmen.append(betrag)
                print(f"Einnahme von {betrag} € hinzugefügt.\n")
                break
            else:
                print("Bitte eine positive Zahl eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

def ausgabe_hinzufuegen():
    while True:
        try:
            betrag = float(input("Geben Sie die Ausgabe ein (positive Zahl): "))
            if betrag > 0:
                ausgaben.append(betrag)
                print(f"Ausgabe von {betrag} € hinzugefügt.\n")
                break
            else:
                print("Bitte eine positive Zahl eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

def zeige_uebersicht():
    gesamt_einnahmen = sum(einnahmen)
    gesamt_ausgaben = sum(ausgaben)
    saldo = gesamt_einnahmen - gesamt_ausgaben
    print("\n--- Übersicht ---")
    print(f"Gesamteinnahmen: {gesamt_einnahmen:.2f} €")
    print(f"Gesamtausgaben: {gesamt_ausgaben:.2f} €")
    print(f"Saldo: {saldo:.2f} €")
    if saldo < 0:
        print("Achtung: Budget überschritten!")
    print("------------------\n")

def main():
    while True:
        print("Bitte wählen Sie eine Option:")
        print("1. Einnahmen hinzufügen")
        print("2. Ausgaben hinzufügen")
        print("3. Übersicht anzeigen")
        print("4. Beenden")
        wahl = input("Ihre Wahl (1-4): ")

        if wahl == '1':
            einnahme_hinzufuegen()
        elif wahl == '2':
            ausgabe_hinzufuegen()
        elif wahl == '3':
            zeige_uebersicht()
        elif wahl == '4':
            print("Programm beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.\n")

if __name__ == "__main__":
    main()