# Fahrzeug-Variablen
farbe = "blau"
größe = "groß"
anzahl_türen = 3
antrieb = "Diesel"
fahrzeug_typ = "Lkw"

# Weitere Variablen, die ich selbst definiert habe
marke = "Mercedes"
modell = "Actros"
leistung_ps = 400
farbe_innenraum = "schwarz"
reifenhersteller = "Michelin"

# Tausche die Werte zwischen zwei Variablen, z.B. marke und modell
marke, modell = modell, marke

# Ausgabe aller Variablen
print("Fahrzeug-Details:")
print(f"Farbe außen: {farbe}")
print(f"Größe: {größe}")
print(f"Anzahl der Türen: {anzahl_türen}")
print(f"Antrieb: {antrieb}")
print(f"Fahrzeugtyp: {fahrzeug_typ}")
print(f"Marke: {marke}")
print(f"Modell: {modell}")
print(f"Leistung (PS): {leistung_ps}")
print(f"Innenraumfarbe: {farbe_innenraum}")
print(f"Reifenhersteller: {reifenhersteller}")
