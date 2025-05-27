import random

# Das Programm wählt eine zufällige Zahl zwischen 1 und 100
zufallszahl = random.randint(1, 100)
versuche = 0

print("Willkommen zum Zahlenraten-Spiel!")
print("Ich habe mir eine Zahl zwischen 1 und 100 ausgedacht. Versuche sie zu erraten.")

while True:
    eingabe = input("Gib deine Zahl ein: ")
    # Überprüfen, ob die Eingabe eine Zahl ist
    if eingabe.isdigit():
        zahl = int(eingabe)
        if 1 <= zahl <= 100:
            versuche += 1
            if zahl == zufallszahl:
                print(f"Herzlichen Glückwunsch! Du hast die Zahl {zufallszahl} in {versuche} Versuchen erraten.")
                break
            elif zahl < zufallszahl:
                print("Zu niedrig! Versuch es nochmal.")
            else:
                print("Zu hoch! Versuch es nochmal.")
        else:
            print("Bitte gib eine Zahl zwischen 1 und 100 ein.")
    else:
        print("Das ist keine gültige Zahl. Bitte gib eine Zahl zwischen 1 und 100 ein.")