def celsius_zu_fahrenheit(c):
    """Wandelt Celsius in Fahrenheit um."""
    return c * 9/5 + 32

def fahrenheit_zu_celsius(f):
    """Wandelt Fahrenheit in Celsius um."""
    return (f - 32) * 5/9

def main():
    print("=" * 50)
    print("Willkommen! Ich helfe dir bei Temperaturumwandlungen".center(50))
    print("=" * 50)
    
    while True:
        umwandlung = input("Möchtest du Celsius in Fahrenheit umwandeln (C) oder Fahrenheit in Celsius (F)? Gib 'C' oder 'F' ein: ").strip().upper()
        if umwandlung in ['C', 'F']:
            break
        else:
            print("Ungültige Eingabe. Bitte gib 'C' oder 'F' ein.")
    
    if umwandlung == 'C':
        while True:
            eingabe = input("Bitte gib die Temperatur in Celsius ein: ").strip()
            try:
                celsius = float(eingabe)
                fahrenheit = celsius_zu_fahrenheit(celsius)
                print(f"\n{celsius:.2f}°C sind {fahrenheit:.2f}°F.")
                break
            except ValueError:
                print("Das ist keine gültige Zahl. Bitte versuche es erneut.")
    else:  # umwandlung == 'F'
        while True:
            eingabe = input("Bitte gib die Temperatur in Fahrenheit ein: ").strip()
            try:
                fahrenheit = float(eingabe)
                celsius = fahrenheit_zu_celsius(fahrenheit)
                print(f"\n{fahrenheit:.2f}°F sind {celsius:.2f}°C.")
                break
            except ValueError:
                print("Das ist keine gültige Zahl. Bitte versuche es erneut.")
    
    print("=" * 50)
    print("Vielen Dank fürs Benutzen des Programms!".center(50))
    print("=" * 50)

if __name__ == "__main__":
    main()