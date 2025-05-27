# Frage den Benutzer nach der oberen Grenze
max_zahl = int(input("Bis zu welcher Zahl möchtest du summieren? "))

# Initialisiere Variablen
summe = 0
zahl = 1

# Schleife, um alle Zahlen bis max_zahl zu durchlaufen
while zahl <= max_zahl:
    # Überprüfe, ob die Zahl gerade ist, ohne modulo oder // zu verwenden
    # Indem wir die Differenz zwischen der Zahl und der nächst kleineren geraden Zahl prüfen
    # oder eine andere Methode, z.B. durch Addition von 2
    # Hier verwenden wir eine einfache Methode: Wir zählen nur gerade Zahlen, indem wir bei 2 starten und immer um 2 erhöhen
    if zahl == 1:
        # Springe direkt zu 2, da 1 ungerade ist
        zahl = 2
        continue
    # Wenn die Zahl größer als max_zahl ist, beenden wir die Schleife
    if zahl > max_zahl:
        break
    # Addiere die gerade Zahl zur Summe
    summe += zahl
    # Erhöhe die Zahl um 2, um nur gerade Zahlen zu durchlaufen
    zahl += 2

# Ausgabe des Ergebnisses
print(f"Die Summe aller geraden Zahlen von 1 bis {max_zahl} ist: {summe}")