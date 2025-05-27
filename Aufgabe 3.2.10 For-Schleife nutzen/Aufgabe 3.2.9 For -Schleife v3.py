# Initialisiere die Summe
summe = 0

# Setze die Startzahl auf 2, da 2 die erste gerade Zahl ist
zahl = 2

# Schleife, solange die Zahl kleiner oder gleich 100 ist
while zahl <= 100:
    summe += zahl
    # Erhöhe die Zahl um 2, um die nächste gerade Zahl zu erhalten
    zahl = zahl + 2

# Ausgabe des Ergebnisses
print("Die Summe aller geraden Zahlen von 1 bis 100 ist:", summe)