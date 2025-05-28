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
        print("Das ist keine gültige Zahl. Bitte versuche es erneut.")

if anzahl == 0:
    print("Es wurden keine Zahlen eingegeben.")
else:
    durchschnitt = summe / anzahl
    sortierte_zahlen = sorted(zahlen)

    print(f"Die kleinste Zahl ist: {min_zahl}")
    print(f"Die größte Zahl ist: {max_zahl}")
    print(f"Der Durchschnitt ist: {durchschnitt}")
    print(f"Sortierte Liste: {sortierte_zahlen}")