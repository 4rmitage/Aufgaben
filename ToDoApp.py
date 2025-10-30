"""
To-Do-Liste mit GUI in Python
Vollständige Implementierung mit allen Erweiterungen:
- Grundfunktionen: Hinzufügen, Löschen, Anzeigen
- Prioritäten (Hoch, Mittel, Niedrig)
- Datumsauswahl (Fälligkeitsdatum)
- Speicherung in JSON-Datei
- Filter nach Status und Priorität
- Theme-Wechsel (Hell/Dunkel)
- Erinnerungsfunktion
- Aufgaben als erledigt markieren
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meine To-Do-Liste")
        self.root.geometry("900x700")
        
        # Daten
        self.tasks: List[Dict] = []
        self.data_file = "tasks.json"
        self.current_theme = "light"
        self.filter_priority = "Alle"
        self.filter_status = "Alle"
        
        # Farb-Themes
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "button_bg": "#4CAF50",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "listbox_bg": "#ffffff",
                "frame_bg": "#e0e0e0"
            },
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#ffffff",
                "button_bg": "#1e88e5",
                "button_fg": "#ffffff",
                "entry_bg": "#3c3c3c",
                "listbox_bg": "#3c3c3c",
                "frame_bg": "#1e1e1e"
            }
        }
        
        # Prioritäts-Farben
        self.priority_colors = {
            "Hoch": "#ff4444",
            "Mittel": "#ffaa00",
            "Niedrig": "#44ff44"
        }
        
        # GUI erstellen
        self.setup_gui()
        
        # Daten laden
        self.load_tasks()
        self.refresh_task_list()
        
        # Erinnerungs-Check starten
        self.check_reminders()
        
    def setup_gui(self):
        """Erstellt die gesamte GUI"""
        
        # Menüleiste
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Datei-Menü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Speichern", command=self.save_tasks)
        file_menu.add_command(label="Laden", command=self.load_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.quit)
        
        # Ansicht-Menü
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ansicht", menu=view_menu)
        view_menu.add_command(label="Theme wechseln", command=self.toggle_theme)
        
        # Hauptframe
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titelbereich
        title_frame = tk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="📝 Meine To-Do-Liste",
            font=("Arial", 24, "bold")
        )
        title_label.pack()
        
        # Eingabebereich
        self.create_input_section()
        
        # Filterbereich
        self.create_filter_section()
        
        # Aufgabenliste
        self.create_task_list_section()
        
        # Steuerungsbuttons
        self.create_control_buttons()
        
        # Statusleiste
        self.create_status_bar()
        
        # Theme anwenden
        self.apply_theme()
        
    def create_input_section(self):
        """Erstellt den Eingabebereich"""
        input_frame = tk.LabelFrame(
            self.main_frame,
            text="Neue Aufgabe hinzufügen",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Aufgabenname
        tk.Label(input_frame, text="Aufgabe:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.task_entry = tk.Entry(input_frame, width=40, font=("Arial", 10))
        self.task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Priorität
        tk.Label(input_frame, text="Priorität:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.priority_var = tk.StringVar(value="Mittel")
        priority_combo = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["Hoch", "Mittel", "Niedrig"],
            state="readonly",
            width=15
        )
        priority_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Fälligkeitsdatum
        tk.Label(input_frame, text="Fällig am:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", pady=5
        )
        date_frame = tk.Frame(input_frame)
        date_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        self.due_date_var = tk.StringVar(value="")
        self.due_date_entry = tk.Entry(
            date_frame,
            textvariable=self.due_date_var,
            width=15,
            font=("Arial", 10)
        )
        self.due_date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(date_frame, text="(TT.MM.JJJJ oder leer)", font=("Arial", 8)).pack(
            side=tk.LEFT
        )
        
        # Schnell-Datum-Buttons
        quick_date_frame = tk.Frame(input_frame)
        quick_date_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        tk.Button(
            quick_date_frame,
            text="Heute",
            command=lambda: self.set_quick_date(0),
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            quick_date_frame,
            text="Morgen",
            command=lambda: self.set_quick_date(1),
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            quick_date_frame,
            text="In 1 Woche",
            command=lambda: self.set_quick_date(7),
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        # Hinzufügen-Button
        add_button = tk.Button(
            input_frame,
            text="➕ Aufgabe hinzufügen",
            command=self.add_task,
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        )
        add_button.grid(row=0, column=2, rowspan=4, padx=10, pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        
    def create_filter_section(self):
        """Erstellt den Filterbereich"""
        filter_frame = tk.LabelFrame(
            self.main_frame,
            text="Filter",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Prioritätsfilter
        tk.Label(filter_frame, text="Priorität:", font=("Arial", 9)).pack(
            side=tk.LEFT, padx=5
        )
        self.filter_priority_var = tk.StringVar(value="Alle")
        priority_filter = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_priority_var,
            values=["Alle", "Hoch", "Mittel", "Niedrig"],
            state="readonly",
            width=12
        )
        priority_filter.pack(side=tk.LEFT, padx=5)
        priority_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Statusfilter
        tk.Label(filter_frame, text="Status:", font=("Arial", 9)).pack(
            side=tk.LEFT, padx=5
        )
        self.filter_status_var = tk.StringVar(value="Alle")
        status_filter = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_status_var,
            values=["Alle", "Offen", "Erledigt"],
            state="readonly",
            width=12
        )
        status_filter.pack(side=tk.LEFT, padx=5)
        status_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Filter zurücksetzen
        tk.Button(
            filter_frame,
            text="Filter zurücksetzen",
            command=self.reset_filters
        ).pack(side=tk.LEFT, padx=20)
        
    def create_task_list_section(self):
        """Erstellt den Aufgabenlistenbereich"""
        list_frame = tk.LabelFrame(
            self.main_frame,
            text="Aufgaben",
            font=("Arial", 12, "bold"),
            padx=5,
            pady=5
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.task_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier New", 10),
            selectmode=tk.SINGLE,
            height=15
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Doppelklick zum Erledigt-Markieren
        self.task_listbox.bind("<Double-Button-1>", lambda e: self.toggle_complete())
        
    def create_control_buttons(self):
        """Erstellt die Steuerungsbuttons"""
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(
            button_frame,
            text="✓ Als erledigt markieren",
            command=self.toggle_complete,
            font=("Arial", 10),
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🗑️ Aufgabe löschen",
            command=self.delete_task,
            font=("Arial", 10),
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="📝 Bearbeiten",
            command=self.edit_task,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🗑️ Alle löschen",
            command=self.clear_all_tasks,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
    def create_status_bar(self):
        """Erstellt die Statusleiste"""
        self.status_bar = tk.Label(
            self.root,
            text="Bereit",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def add_task(self):
        """Fügt eine neue Aufgabe hinzu"""
        task_text = self.task_entry.get().strip()
        
        if not task_text:
            messagebox.showwarning("Warnung", "Bitte geben Sie eine Aufgabe ein!")
            return
        
        # Datum validieren
        due_date = self.due_date_var.get().strip()
        if due_date:
            try:
                datetime.strptime(due_date, "%d.%m.%Y")
            except ValueError:
                messagebox.showerror(
                    "Fehler",
                    "Ungültiges Datum! Format: TT.MM.JJJJ"
                )
                return
        
        # Aufgabe erstellen
        task = {
            "text": task_text,
            "priority": self.priority_var.get(),
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        
        self.tasks.append(task)
        self.refresh_task_list()
        self.save_tasks()
        
        # Eingabefelder zurücksetzen
        self.task_entry.delete(0, tk.END)
        self.due_date_var.set("")
        self.priority_var.set("Mittel")
        
        self.update_status(f"Aufgabe '{task_text}' hinzugefügt")
        
    def delete_task(self):
        """Löscht die ausgewählte Aufgabe"""
        try:
            selection = self.task_listbox.curselection()[0]
            filtered_tasks = self.get_filtered_tasks()
            task_to_delete = filtered_tasks[selection]
            
            confirm = messagebox.askyesno(
                "Bestätigung",
                f"Aufgabe '{task_to_delete['text']}' wirklich löschen?"
            )
            
            if confirm:
                self.tasks.remove(task_to_delete)
                self.refresh_task_list()
                self.save_tasks()
                self.update_status("Aufgabe gelöscht")
        except IndexError:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Aufgabe aus!")
            
    def toggle_complete(self):
        """Markiert eine Aufgabe als erledigt/unerledigt"""
        try:
            selection = self.task_listbox.curselection()[0]
            filtered_tasks = self.get_filtered_tasks()
            task = filtered_tasks[selection]
            
            # Status umschalten
            task["completed"] = not task["completed"]
            
            self.refresh_task_list()
            self.save_tasks()
            
            status = "erledigt" if task["completed"] else "offen"
            self.update_status(f"Aufgabe als {status} markiert")
        except IndexError:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Aufgabe aus!")
            
    def edit_task(self):
        """Bearbeitet eine ausgewählte Aufgabe"""
        try:
            selection = self.task_listbox.curselection()[0]
            filtered_tasks = self.get_filtered_tasks()
            task = filtered_tasks[selection]
            
            # Eingabefelder mit aktuellen Werten füllen
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task["text"])
            self.priority_var.set(task["priority"])
            self.due_date_var.set(task["due_date"])
            
            # Alte Aufgabe löschen
            self.tasks.remove(task)
            self.refresh_task_list()
            
            self.update_status("Aufgabe wird bearbeitet")
        except IndexError:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Aufgabe aus!")
            
    def clear_all_tasks(self):
        """Löscht alle Aufgaben"""
        if not self.tasks:
            messagebox.showinfo("Info", "Keine Aufgaben vorhanden!")
            return
            
        confirm = messagebox.askyesno(
            "Bestätigung",
            f"Wirklich alle {len(self.tasks)} Aufgaben löschen?"
        )
        
        if confirm:
            self.tasks.clear()
            self.refresh_task_list()
            self.save_tasks()
            self.update_status("Alle Aufgaben gelöscht")
            
    def set_quick_date(self, days):
        """Setzt ein Schnelldatum"""
        date = datetime.now() + timedelta(days=days)
        self.due_date_var.set(date.strftime("%d.%m.%Y"))
        
    def get_filtered_tasks(self):
        """Gibt gefilterte Aufgaben zurück"""
        filtered = self.tasks.copy()
        
        # Prioritätsfilter
        if self.filter_priority_var.get() != "Alle":
            filtered = [
                t for t in filtered
                if t["priority"] == self.filter_priority_var.get()
            ]
        
        # Statusfilter
        if self.filter_status_var.get() == "Offen":
            filtered = [t for t in filtered if not t["completed"]]
        elif self.filter_status_var.get() == "Erledigt":
            filtered = [t for t in filtered if t["completed"]]
        
        return filtered
        
    def apply_filters(self):
        """Wendet Filter an"""
        self.refresh_task_list()
        self.update_status("Filter angewendet")
        
    def reset_filters(self):
        """Setzt Filter zurück"""
        self.filter_priority_var.set("Alle")
        self.filter_status_var.set("Alle")
        self.refresh_task_list()
        self.update_status("Filter zurückgesetzt")
        
    def refresh_task_list(self):
        """Aktualisiert die Aufgabenliste"""
        self.task_listbox.delete(0, tk.END)
        
        filtered_tasks = self.get_filtered_tasks()
        
        if not filtered_tasks:
            self.task_listbox.insert(tk.END, "Keine Aufgaben vorhanden")
            return
        
        for task in filtered_tasks:
            # Status-Symbol
            status = "✓" if task["completed"] else "○"
            
            # Prioritäts-Symbol
            priority_symbol = {
                "Hoch": "🔴",
                "Mittel": "🟡",
                "Niedrig": "🟢"
            }[task["priority"]]
            
            # Datum formatieren
            date_str = f" | Fällig: {task['due_date']}" if task['due_date'] else ""
            
            # Zeile formatieren
            task_line = f"{status} {priority_symbol} {task['text']}{date_str}"
            
            self.task_listbox.insert(tk.END, task_line)
            
            # Farbe setzen
            index = self.task_listbox.size() - 1
            if task["completed"]:
                self.task_listbox.itemconfig(index, fg="gray")
            else:
                # Überfällige Aufgaben rot markieren
                if task["due_date"]:
                    try:
                        due = datetime.strptime(task["due_date"], "%d.%m.%Y")
                        if due.date() < datetime.now().date():
                            self.task_listbox.itemconfig(index, fg="red")
                    except:
                        pass
        
        # Statistik aktualisieren
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["completed"]])
        open_tasks = total - completed
        self.update_status(
            f"Gesamt: {total} | Offen: {open_tasks} | Erledigt: {completed}"
        )
        
    def save_tasks(self):
        """Speichert Aufgaben in JSON-Datei"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Fehler", f"Speichern fehlgeschlagen: {e}")
            
    def load_tasks(self):
        """Lädt Aufgaben aus JSON-Datei"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
                self.update_status("Aufgaben geladen")
            except Exception as e:
                messagebox.showerror("Fehler", f"Laden fehlgeschlagen: {e}")
                self.tasks = []
        
    def toggle_theme(self):
        """Wechselt zwischen Hell- und Dunkel-Theme"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        self.update_status(f"Theme gewechselt zu: {self.current_theme}")
        
    def apply_theme(self):
        """Wendet das aktuelle Theme an"""
        theme = self.themes[self.current_theme]
        
        self.root.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])
        self.task_listbox.configure(
            bg=theme["listbox_bg"],
            fg=theme["fg"]
        )
        self.status_bar.configure(bg=theme["bg"], fg=theme["fg"])
        
    def check_reminders(self):
        """Prüft auf fällige Aufgaben und zeigt Erinnerungen"""
        today = datetime.now().date()
        
        for task in self.tasks:
            if task["completed"] or not task["due_date"]:
                continue
                
            try:
                due_date = datetime.strptime(task["due_date"], "%d.%m.%Y").date()
                
                # Heute fällig
                if due_date == today:
                    messagebox.showinfo(
                        "Erinnerung",
                        f"Heute fällig:\n{task['text']}"
                    )
                # Überfällig
                elif due_date < today:
                    messagebox.showwarning(
                        "Überfällig!",
                        f"Diese Aufgabe ist überfällig:\n{task['text']}"
                    )
            except:
                pass
        
        # Alle 60 Sekunden prüfen
        self.root.after(60000, self.check_reminders)
        
    def update_status(self, message):
        """Aktualisiert die Statusleiste"""
        self.status_bar.config(text=message)


def main():
    """Hauptfunktion"""
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()