# bank_account.py

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