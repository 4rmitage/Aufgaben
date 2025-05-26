# Eingabe der Zahl vom Benutzer
zahl_str = input("Bitte gib eine Zahl ein: ")

# Umwandlung des Strings in eine ganze Zahl
zahl = int(zahl_str)

# Überprüfung, ob die Zahl gerade oder ungerade ist
if zahl % 2 == 0:
    print("Die Zahl ist gerade.")
else:
    print("Die Zahl ist ungerade.")