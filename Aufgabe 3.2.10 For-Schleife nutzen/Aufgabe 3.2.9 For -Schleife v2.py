summe = 0
zahl = 2  # Die erste gerade Zahl in diesem Bereich

for _ in range(50):  # Es gibt 50 gerade Zahlen zwischen 1 und 100
    summe += zahl
    zahl += 2  # Nächste gerade Zahl

print("Die Summe aller geraden Zahlen von 1 bis 100 ist:", summe)