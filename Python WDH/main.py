from terminal import main_terminal
from gui import main_gui

def main():
    print("Wähle den Modus:")
    print("1. Terminal-Modus")
    print("2. GUI-Modus")

    mode = input("Deine Wahl: ")

    if mode == '1':
        main_terminal()
    elif mode == '2':
        main_gui()
    else:
        print("Ungültige Wahl. Programm wird beendet.")

if __name__ == "__main__":
    main()