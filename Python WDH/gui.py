import tkinter as tk
from tkinter import messagebox
from utils import eingabe_validieren, berechne_gesamt

class FinanzManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finanz Manager")

        # Initialisiere Listen
        self.einnahmen = []
        self.ausgaben = []

        # Erstelle Widgets
        self.betrag_label = tk.Label(root, text="Betrag:")
        self.betrag_label.grid(row=0, column=0)

        self.betrag_entry = tk.Entry(root)
        self.betrag_entry.grid(row=0, column=1)

        self.beschreibung_label = tk.Label(root, text="Beschreibung:")
        self.beschreibung_label.grid(row=1, column=0)

        self.beschreibung_entry = tk.Entry(root)
        self.beschreibung_entry.grid(row=1, column=1)

        # Buttons
        self.einnahme_button = tk.Button(root, text="Einnahme hinzufügen", command=self.einnahme_hinzufuegen)
        self.einnahme_button.grid(row=2, column=0)

        self.ausgabe_button = tk.Button(root, text="Ausgabe hinzufügen", command=self.ausgabe_hinzufuegen)
        self.ausgabe_button.grid(row=2, column=1)

        self.uebersicht_button = tk.Button(root, text="Übersicht anzeigen", command=self.zeige_uebersicht)
        self.uebersicht_button.grid(row=3, column=0, columnspan=2)

        # Textbereich für die Übersicht
        self.uebersicht_text = tk.Text(root, height=10, width=40)
        self.uebersicht_text.grid(row=4, column=0, columnspan=2)

    def einnahme_hinzufuegen(self):
        betrag = self.betrag_entry.get()
        beschreibung = self.beschreibung_entry.get()

        if not eingabe_validieren(betrag):
            messagebox.showerror("Fehler", "Der Betrag muss eine positive Zahl sein!")
            return

        self.einnahmen.append((float(betrag), beschreibung))
        self.betrag_entry.delete(0, tk.END)
        self.beschreibung_entry.delete(0, tk.END)
        messagebox.showinfo("Erfolg", f"Einnahme von {betrag} Euro hinzugefügt!")

    def ausgabe_hinzufuegen(self):
        betrag = self.betrag_entry.get()
        beschreibung = self.beschreibung_entry.get()

        if not eingabe_validieren(betrag):
            messagebox.showerror("Fehler", "Der Betrag muss eine positive Zahl sein!")
            return

        self.ausgaben.append((float(betrag), beschreibung))
        self.betrag_entry.delete(0, tk.END)
        self.beschreibung_entry.delete(0, tk.END)
        messagebox.showinfo("Erfolg", f"Ausgabe von {betrag} Euro hinzugefügt!")

    def zeige_uebersicht(self):
        gesamt_einnahmen, gesamt_ausgaben = berechne_gesamt(self.einnahmen, self.ausgaben)
        saldo = gesamt_einnahmen - gesamt_ausgaben

        uebersicht = f"Gesamteinnahmen: {gesamt_einnahmen} Euro\n"
        uebersicht += f"Gesamtausgaben: {gesamt_ausgaben} Euro\n"
        uebersicht += f"Saldo: {saldo} Euro\n"

        if saldo < 0:
            uebersicht += "Achtung: Budget überschritten!"

        self.uebersicht_text.delete(1.0, tk.END)
        self.uebersicht_text.insert(tk.END, uebersicht)

def main_gui():
    root = tk.Tk()
    app = FinanzManagerApp(root)
    root.mainloop()