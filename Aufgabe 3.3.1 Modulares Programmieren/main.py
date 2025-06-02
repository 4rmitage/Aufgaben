# main.py

from bank_account import BankAccount

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