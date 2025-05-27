# Frage den Benutzer nach der oberen Grenze
obergrenze = int(input("Bis zu welcher Zahl möchtest du die geraden Zahlen summieren? "))

# Initialisiere die Summe
summe = 0

# Setze die Startzahl auf 2, da 2 die erste gerade Zahl ist
zahl = 2

# Schleife, solange die Zahl kleiner oder gleich der Obergrenze ist
while zahl <= obergrenze:
    summe += zahl
    # Erhöhe die Zahl um 2, um die nächste gerade Zahl zu erhalten
    zahl = zahl + 2

# Ausgabe des Ergebnisses
print(f"Die Summe aller geraden Zahlen von 1 bis {obergrenze} ist: {summe}")