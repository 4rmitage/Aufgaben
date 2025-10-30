from utils import eingabe_validieren, berechne_gesamt

def einnahme_hinzufuegen(einnahmen):
    betrag = input("Gib den Betrag der Einnahme ein: ")
    if not eingabe_validieren(betrag):
        print("Der Betrag muss eine positive Zahl sein!")
        return

    beschreibung = input("Gib eine Beschreibung der Einnahme ein: ")
    einnahmen.append((float(betrag), beschreibung))
    print(f"Einnahme von {betrag} Euro hinzugefügt!")

def ausgabe_hinzufuegen(ausgaben):
    betrag = input("Gib den Betrag der Ausgabe ein: ")
    if not eingabe_validieren(betrag):
        print("Der Betrag muss eine positive Zahl sein!")
        return

    beschreibung = input("Gib eine Beschreibung der Ausgabe ein: ")
    ausgaben.append((float(betrag), beschreibung))
    print(f"Ausgabe von {betrag} Euro hinzugefügt!")

def zeige_uebersicht(einnahmen, ausgaben):
    gesamt_einnahmen, gesamt_ausgaben = berechne_gesamt(einnahmen, ausgaben)
    saldo = gesamt_einnahmen - gesamt_ausgaben

    print("\n--- Übersicht ---")
    print(f"Gesamteinnahmen: {gesamt_einnahmen} Euro")
    print(f"Gesamtausgaben: {gesamt_ausgaben} Euro")
    print(f"Saldo: {saldo} Euro")
    if saldo < 0:
        print("Achtung: Budget überschritten!")

def main_terminal():
    einnahmen = []
    ausgaben = []

    while True:
        print("\nWähle eine Option:")
        print("1. Einnahmen hinzufügen")
        print("2. Ausgaben hinzufügen")
        print("3. Übersicht anzeigen")
        print("4. Beenden")

        auswahl = input("Deine Wahl: ")

        if auswahl == '1':
            einnahme_hinzufuegen(einnahmen)
        elif auswahl == '2':
            ausgabe_hinzufuegen(ausgaben)
        elif auswahl == '3':
            zeige_uebersicht(einnahmen, ausgaben)
        elif auswahl == '4':
            print("Programm beendet.")
            break
        else:
            print("Ungültige Wahl. Bitte versuche es erneut.")