import tkinter as tk
from tkinter import messagebox, simpledialog

class BankAccount:
    def __init__(self, kontoinhaber, ueberziehungsrahmen=-100.0):
        self.kontoinhaber = kontoinhaber
        self.kontostand = 0.0
        self.ueberziehungsrahmen = ueberziehungsrahmen

    def einzahlen(self, betrag):
        if betrag > 0:
            self.kontostand += betrag
            return True, f"{betrag:.2f}€ wurden eingezahlt."
        else:
            return False, "Der Betrag zum Einzahlen muss positiv sein."

    def abheben(self, betrag):
        if betrag <= 0:
            return False, "Der Betrag zum Abheben muss positiv sein."
        elif self.kontostand - betrag < self.ueberziehungsrahmen:
            return False, "Warnung: Überziehungslimit überschritten. Abhebung nicht möglich."
        else:
            self.kontostand -= betrag
            return True, f"{betrag:.2f}€ wurden abgehoben."

    def zeige_kontostand(self):
        return f"Der aktuelle Kontostand von {self.kontoinhaber} beträgt {self.kontostand:.2f}€."

    def zinsen_berechnen(self, zinssatz):
        if self.kontostand > 0:
            zinsen = self.kontostand * (zinssatz / 100)
            self.kontostand += zinsen
            return True, f"Zinsen in Höhe von {zinsen:.2f}€ wurden berechnet und dem Konto gutgeschrieben."
        else:
            return False, "Der Kontostand ist nicht positiv. Zinsen werden nicht berechnet."

class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bankkonto Verwaltung")
        self.konto = None

        self.kontoinhaber = simpledialog.askstring("Willkommen", "Bitte geben Sie den Namen des Kontoinhabers ein:")
        if not self.kontoinhaber:
            self.root.destroy()
            return
        self.konto = BankAccount(self.kontoinhaber)

        self.label = tk.Label(root, text=f"Willkommen, {self.kontoinhaber}!", font=("Arial", 14))
        self.label.pack(pady=10)

        self.status_label = tk.Label(root, text=self.konto.zeige_kontostand(), font=("Arial", 12))
        self.status_label.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Einzahlen", width=15, command=self.einzahlen).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Abheben", width=15, command=self.abheben).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Kontostand anzeigen", width=15, command=self.anzeigen_k