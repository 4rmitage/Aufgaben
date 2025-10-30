import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import csv
import os

DATEI = "bewerbungen.csv"


class BewerbungsManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Bewerbungsmanager")
        self.root.geometry("980x580")
        self.root.resizable(False, False)

        # CSV initialisieren
        if not os.path.exists(DATEI):
            with open(DATEI, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Firma", "Position", "Ansprechpartner", "Datum", "Status", "Notizen"])

        self.sort_spalte = None
        self.sort_aufsteigend = True

        # GUI aufbauen
        self.create_widgets()
        self.lade_daten()

    def create_widgets(self):
        # Eingabebereich
        frame_form = tk.LabelFrame(self.root, text="Neue / Bearbeiten Bewerbung", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        labels = ["Firma:", "Position:", "Ansprechpartner:", "Datum:", "Status:", "Notizen:"]
        for i, lbl in enumerate(labels):
            tk.Label(frame_form, text=lbl).grid(row=i, column=0, sticky="w", pady=3)

        self.entry_firma = tk.Entry(frame_form, width=40)
        self.entry_position = tk.Entry(frame_form, width=40)
        self.entry_ansprech = tk.Entry(frame_form, width=40)
        self.entry_datum = DateEntry(frame_form, width=18, date_pattern="dd.mm.yyyy", background="lightblue")
        self.status_var = tk.StringVar()
        self.status_box = ttk.Combobox(frame_form, textvariable=self.status_var, values=[
            "Gesendet", "Eingang bestätigt", "Einladung", "Absage", "Offen"
        ], state="readonly", width=18)
        self.entry_notizen = tk.Entry(frame_form, width=60)

        self.entry_firma.grid(row=0, column=1, sticky="w")
        self.entry_position.grid(row=1, column=1, sticky="w")
        self.entry_ansprech.grid(row=2, column=1, sticky="w")
        self.entry_datum.grid(row=3, column=1, sticky="w")
        self.status_box.grid(row=4, column=1, sticky="w")
        self.entry_notizen.grid(row=5, column=1, sticky="w")

        # Buttons
        frame_btn = tk.Frame(frame_form)
        frame_btn.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(frame_btn, text="Speichern / Hinzufügen", command=self.speichern).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Bearbeiten", command=self.bearbeiten).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Löschen", command=self.loeschen).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="CSV exportieren", command=self.export_csv).grid(row=0, column=3, padx=5)

        # Suchfeld
        frame_search = tk.LabelFrame(self.root, text="Suche & Filter", padx=10, pady=10)
        frame_search.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_search, text="Suche:").grid(row=0, column=0)
        self.suche_var = tk.StringVar()
        tk.Entry(frame_search, textvariable=self.suche_var, width=30).grid(row=0, column=1, padx=5)
        tk.Button(frame_search, text="Anwenden", command=self.filtern).grid(row=0, column=2, padx=5)
        tk.Button(frame_search, text="Alle anzeigen", command=self.lade_daten).grid(row=0, column=3, padx=5)

        # Tabelle
        frame_table = tk.Frame(self.root)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        spalten = ["Firma", "Position", "Ansprechpartner", "Datum", "Status", "Notizen"]
        self.tree = ttk.Treeview(frame_table, columns=spalten, show="headings", height=12)
        for col in spalten:
            self.tree.heading(col, text=col, command=lambda c=col: self.sortiere_nach_spalte(c))
            self.tree.column(col, width=150, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.auswahl_anzeigen)

    # --- Datenfunktionen ---
    def lade_daten(self):
        """Lädt alle Bewerbungen"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        with open(DATEI, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tree.insert("", "end", values=(row["Firma"], row["Position"], row["Ansprechpartner"],
                                                    row["Datum"], row["Status"], row["Notizen"]))

    def speichern(self):
        """Neue Bewerbung hinzufügen"""
        daten = [
            self.entry_firma.get().strip(),
            self.entry_position.get().strip(),
            self.entry_ansprech.get().strip(),
            self.entry_datum.get(),
            self.status_var.get(),
            self.entry_notizen.get().strip()
        ]
        if not all(daten[:2]):
            messagebox.showwarning("Fehler", "Firma und Position müssen ausgefüllt sein.")
            return

        with open(DATEI, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(daten)
        self.lade_daten()
        self.felder_leeren()

    def bearbeiten(self):
        """Bearbeitet die markierte Bewerbung"""
        auswahl = self.tree.focus()
        if not auswahl:
            messagebox.showinfo("Hinweis", "Bitte eine Bewerbung auswählen.")
            return
        alt = self.tree.item(auswahl, "values")
        neu = [
            self.entry_firma.get().strip(),
            self.entry_position.get().strip(),
            self.entry_ansprech.get().strip(),
            self.entry_datum.get(),
            self.status_var.get(),
            self.entry_notizen.get().strip()
        ]
        daten = []
        with open(DATEI, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if tuple(row) == alt:
                    daten.append(neu)
                else:
                    daten.append(row)
        with open(DATEI, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(daten)
        self.lade_daten()
        self.felder_leeren()

    def loeschen(self):
        """Löscht eine Bewerbung"""
        auswahl = self.tree.focus()
        if not auswahl:
            return
        werte = self.tree.item(auswahl, "values")
        if not messagebox.askyesno("Löschen bestätigen", f"Bewerbung bei {werte[0]} wirklich löschen?"):
            return
        daten = []
        with open(DATEI, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if tuple(row) != werte:
                    daten.append(row)
        with open(DATEI, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(daten)
        self.lade_daten()

    # --- Hilfsfunktionen ---
    def auswahl_anzeigen(self, event):
        auswahl = self.tree.focus()
        if not auswahl:
            return
        werte = self.tree.item(auswahl, "values")
        self.entry_firma.delete(0, tk.END)
        self.entry_firma.insert(0, werte[0])
        self.entry_position.delete(0, tk.END)
        self.entry_position.insert(0, werte[1])
        self.entry_ansprech.delete(0, tk.END)
        self.entry_ansprech.insert(0, werte[2])
        self.entry_datum.set_date(werte[3])
        self.status_var.set(werte[4])
        self.entry_notizen.delete(0, tk.END)
        self.entry_notizen.insert(0, werte[5])

    def filtern(self):
        suchtext = self.suche_var.get().lower().strip()
        if not suchtext:
            self.lade_daten()
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        with open(DATEI, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if suchtext in row["Firma"].lower() or suchtext in row["Position"].lower():
                    self.tree.insert("", "end", values=(row["Firma"], row["Position"], row["Ansprechpartner"],
                                                        row["Datum"], row["Status"], row["Notizen"]))

    def export_csv(self):
        datei = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Dateien", "*.csv")])
        if not datei:
            return
        with open(DATEI, newline="", encoding="utf-8") as src, open(datei, "w", newline="", encoding="utf-8") as dest:
            dest.write(src.read())
        messagebox.showinfo("Export erfolgreich", f"Datei wurde gespeichert als:\n{datei}")

    def felder_leeren(self):
        self.entry_firma.delete(0, tk.END)
        self.entry_position.delete(0, tk.END)
        self.entry_ansprech.delete(0, tk.END)
        self.entry_notizen.delete(0, tk.END)
        self.status_var.set("")
        self.entry_datum.set_date("")

    def sortiere_nach_spalte(self, spalte):
        """Sortiert Tabelle beim Klick auf Spaltenkopf"""
        daten = [self.tree.item(child)["values"] for child in self.tree.get_children()]
        index = self.tree["columns"].index(spalte)
        if self.sort_spalte == spalte:
            self.sort_aufsteigend = not self.sort_aufsteigend
        else:
            self.sort_spalte = spalte
            self.sort_aufsteigend = True

        daten.sort(key=lambda x: x[index], reverse=not self.sort_aufsteigend)

        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in daten:
            self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = BewerbungsManager(root)
    root.mainloop()