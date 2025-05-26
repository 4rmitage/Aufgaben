print("Willkommen in der Lotterie")
number1 = int(input("Bitte wähle eine Zahl zwischen 1 und 49:"))
number2 = int(input("Bitte wähle eine Zahl zwischen 1 und 49:"))
number3 = int(input("Bitte wähle eine Zahl zwischen 1 und 49:"))

# Geheimzahl 1: 3
# Geheimzahl 2: 14
# Geheimzahl 3: 22


if number1 == 3 and number2 == 14 and number3 == 22:
    print("Herzlichen Glückwunsch, du hast die Lotterie gewonnen!")
else:
    print("Du hast leider verloren ...")