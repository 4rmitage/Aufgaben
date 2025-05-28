# Liste zum Speichern der eingegebenen Zahlen
zahlen = []

print("Gib Zahlen ein. Tippe 'stop', um die Eingabe zu beenden.")

# Variablen für die Zählung und Speicherung
anzahl = 0
summe = 0
min_zahl = None
max_zahl = None

while True:
    eingabe = input("Bitte Zahl eingeben (oder 'stop' zum Beenden): ")
    if eingabe == 'stop':
        break
    try:
        # Versuche, die Eingabe in eine float-Zahl umzuwandeln
        zahl = float(eingabe)
        # Zahl zur Liste hinzufügen
        zahlen += [zahl]
        anzahl += 1
        summe += zahl
        if min_zahl is None or zahl < min_zahl:
            min_zahl = zahl
        if max_zahl is None or zahl > max_zahl:
            max_zahl = zahl
    except ValueError:
        # Überprüfe, ob die Eingabe ein Integer ist
        try:
            int_eingabe = int(eingabe)
            # Wenn die Umwandlung funktioniert, ist die Zahl ein Integer
            print("Fehler: Bitte gib eine gültige Zahl ein (Dezimalzahlen sind erlaubt).")
        except ValueError:
            # Wenn auch die Integer-Umwandlung fehlschlägt, ist die Eingabe ungültig
            print("Das ist keine gültige Zahl. Bitte versuche es erneut.")

if anzahl == 0:
    print("Es wurden keine Zahlen eingegeben.")
else:
    durchschnitt = round(summe / anzahl, 2)
    sortierte_zahlen = sorted(zahlen)

    print(f"Die kleinste Zahl ist: {min_zahl}")
    print(f"Die größte Zahl ist: {max_zahl}")
    print(f"Der Durchschnitt ist: {durchschnitt}")
    print(f"Sortierte Liste: {sortierte_zahlen}")