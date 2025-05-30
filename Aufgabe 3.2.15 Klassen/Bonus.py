class BankAccount:
    def __init__(self, kontoinhaber, ueberziehungsrahmen=-100.0):
        self.kontoinhaber = kontoinhaber
        self.kontostand = 0.0
        self.ueberziehungsrahmen = ueberziehungsrahmen

    def einzahlen(self, betrag):
        if betrag > 0:
            self.kontostand += betrag
            print(f"{betrag}€ wurden eingezahlt.")
        else:
            print("Der Betrag zum Einzahlen muss positiv sein.")

    def abheben(self, betrag):
        if betrag <= 0:
            print("Der Betrag zum Abheben muss positiv sein.")
        elif self.kontostand - betrag < self.ueberziehungsrahmen:
            print("Warnung: Überziehungslimit überschritten. Abhebung nicht möglich.")
        else:
            self.kontostand -= betrag
            print(f"{betrag}€ wurden abgehoben.")

    def zeige_kontostand(self):
        print(f"Der aktuelle Kontostand von {self.kontoinhaber} beträgt {self.kontostand:.2f}€.")

    def __str__(self):
        return f"Konto von {self.kontoinhaber} – Kontostand: {self.kontostand:.2f} €"

    def zinsen_berechnen(self, zinssatz):
        if self.kontostand > 0:
            zinsen = self.kontostand * (zinssatz / 100)
            self.kontostand += zinsen
            print(f"Zinsen in Höhe von {zinsen:.2f}€ wurden berechnet und dem Konto gutgeschrieben.")
        else:
            print("Der Kontostand ist nicht positiv. Zinsen werden nicht berechnet.")

# Nutzung der Klasse
def main():
    kontoinhaber = input("Bitte geben Sie den Namen des Kontoinhabers ein: ")
    konto = BankAccount(kontoinhaber)

    while True:
        print("\nWas möchten Sie tun?")
        print("1. Einzahlen")
        print("2. Abheben")
        print("3. Kontostand anzeigen")
        print("4. Zinsen berechnen")
        print("5. Beenden")
        wahl = input("Bitte wählen Sie eine Option (1-5): ")

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
            try:
                zinssatz = float(input("Geben Sie den Zinssatz in % ein: "))
                konto.zinsen_berechnen(zinssatz)
            except ValueError:
                print("Bitte geben Sie eine gültige Zahl ein.")
        elif wahl == '5':
            print("Vielen Dank! Auf Wiedersehen.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()