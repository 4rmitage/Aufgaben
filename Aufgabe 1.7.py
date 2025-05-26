# Variablen definieren
farbe = "blau"
größe = "groß"
türen = 3
kraftstoff = "Diesel"
fahrzeugtyp = "Lkw"

# Weitere Variablen selbst definieren
marke = "Mercedes"
modell = "Actros"
leistung = 400  # in PS
gewicht = 18000  # in kg
farbe_innen = "schwarz"

# Ausgabe vor dem Tausch
print("Vor dem Tausch:")
print(f"Farbe: {farbe}")
print(f"Marke: {marke}")
print(f"Modell: {modell}")
print(f"Leistung: {leistung} PS")
print(f"Gewicht: {gewicht} kg")
print(f"Innenfarbe: {farbe_innen}")

# Tauschen der Werte zwischen zwei Variablen, z.B. Farbe und Innenfarbe
farbe, farbe_innen = farbe_innen, farbe

# Ausgabe nach dem Tausch
print("Nach dem Tausch:")
print(f"Farbe: {farbe}")
print(f"Innenfarbe: {farbe_innen}")