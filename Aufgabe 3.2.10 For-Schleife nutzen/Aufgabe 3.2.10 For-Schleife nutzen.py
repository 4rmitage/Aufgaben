# Initialisiere die Summe
summe = 0

# Schleife von 1 bis 100
for zahl in range(1, 101):
    # Überprüfe, ob die Zahl gerade ist, ohne den Modulo-Operator
    # Indem wir die Zahl durch 2 teilen und den Rest mit Subtraktion ermitteln
    if (zahl - (zahl // 2) * 2) == 0:
        summe += zahl

# Ausgabe des Ergebnisses
print("Die Summe aller geraden Zahlen von 1 bis 100 ist:", summe)