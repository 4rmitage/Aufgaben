def celsius_zu_fahrenheit(c):
    """Wandelt Celsius in Fahrenheit um."""
    return c * 9/5 + 32

def fahrenheit_zu_celsius(f):
    """Wandelt Fahrenheit in Celsius um."""
    return (f - 32) * 5/9

def main():
    print("Willkommen! Ich helfe dir gerne bei Temperaturumwandlungen.")
    umwandlung = input("Möchtest du Celsius in Fahrenheit umwandeln (C) oder Fahrenheit in Celsius (F)? Gib 'C' oder 'F' ein: ").strip().upper()

    if umwandlung == 'C':
        try:
            celsius = float(input("Bitte gib die Temperatur in Celsius ein: "))
            fahrenheit = celsius_zu_fahrenheit(celsius)
            print(f"{celsius}°C sind {fahrenheit:.2f}°F.")
        except ValueError:
            print("Das ist keine gültige Zahl. Bitte starte das Programm neu und gib eine Zahl ein.")
    elif umwandlung == 'F':
        try:
            fahrenheit = float(input("Bitte gib die Temperatur in Fahrenheit ein: "))
            celsius = fahrenheit_zu_celsius(fahrenheit)
            print(f"{fahrenheit}°F sind {celsius:.2f}°C.")
        except ValueError:
            print("Das ist keine gültige Zahl. Bitte starte das Programm neu und gib eine Zahl ein.")
    else:
        print("Ungültige Eingabe. Bitte starte das Programm neu und gib 'C' oder 'F' ein.")

if __name__ == "__main__":
    main()