class BankAccount:
    def __init__(self, kontoinhaber):
        self.kontoinhaber = kontoinhaber
        self.kontostand = 0.0

    def einzahlen(self, betrag):
        if betrag > 0:
            self.kontostand += betrag
            print(f"{betrag}€ wurden eingezahlt.")
        else:
            print("Der Betrag zum Einzahlen muss positiv sein.")

    def abheben(self, betrag):
        if betrag > self.kontostand:
            print("Warnung: Nicht genügend Geld auf dem Konto.")
        elif betrag <= 0:
            print("Der Betrag zum Abheben muss positiv sein.")
        else:
            self.kontostand -= betrag
            print(f"{betrag}€ wurden abgehoben.")

    def zeige_kontostand(self):
        print(f"Der aktuelle Kontostand von {self.kontoinhaber} beträgt {self.kontostand}€.")

# Beispiel: Nutzung der Klasse mit Eingaben
def main():
    kontoinhaber = input("Bitte geben Sie den Namen des Kontoinhabers ein: ")
    konto = BankAccount(kontoinhaber)

    while True:
        print("\nWas möchten Sie tun?")
        print("1. Einzahlen")
        print("2. Abheben")
        print("3. Kontostand anzeigen")
        print("4. Beenden")
        wahl = input("Bitte wählen Sie eine Option (1-4): ")

        if wahl == '1':
            try:
                betrag = float(input("Geben Sie den Betrag zum Einzahlen ein: "))
                konto.einzahlen(betrag)
            except ValueError:
                print("Bitte geben Sie eine gültige Zahl ein.")
        elif wahl == '2':
            try:
                betrag = float(input("Geben Sie den Betrag zum Abheben ein: "))
                konto.abheben(betrag)
            except ValueError:
                print("Bitte geben Sie eine gültige Zahl ein.")
        elif wahl == '3':
            konto.zeige_kontostand()
        elif wahl == '4':
            print("Vielen Dank! Auf Wiedersehen.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()