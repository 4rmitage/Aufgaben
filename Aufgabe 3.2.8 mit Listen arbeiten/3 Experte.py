# Deine Liste von Zahlen
zahlen = [4, 7, 2, 9, 1, 5, 3]

# 1. Länge der Liste ausgeben
print("Länge der Liste:", len(zahlen))

# 2. Größte und kleinste Zahl ausgeben
groesste_zahl = max(zahlen)
kleinste_zahl = min(zahlen)
print("Größte Zahl:", groesste_zahl)
print("Kleinste Zahl:", kleinste_zahl)

# 3. Durchschnitt (Mittelwert) berechnen
durchschnitt = sum(zahlen) / len(zahlen)
print("Durchschnitt (Mittelwert):", durchschnitt)

# 4. Liste in umgekehrter Reihenfolge ausgeben
umgekehrte_liste = list(reversed(zahlen))
print("Liste in umgekehrter Reihenfolge:", umgekehrte_liste)

# 5. Neue Liste mit nur geraden Zahlen
gerade_zahlen = [zahl for zahl in zahlen if zahl % 2 == 0]
print("Gerade Zahlen:", gerade_zahlen)