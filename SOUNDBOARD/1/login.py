import tkinter as tk
from tkinter import messagebox
import json
import os

USER_DATA_FILE = "user_data.json"

# Hilfsfunktionen für Benutzerdaten
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")

        self.users = load_users()
        self.mode = "login"  # oder "register"

        self._create_widgets()
        self._draw_login()

    def _create_widgets(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        self.title_label = tk.Label(self.frame, text="Login", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        tk.Label(self.frame, text="Benutzername:").grid(row=1, column=0, sticky="e")
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Passwort:").grid(row=2, column=0, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1)

        self.action_button = tk.Button(self.frame, text="Login", command=self._handle_action)
        self.action_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.switch_button = tk.Button(self.frame, text="Noch kein Konto? Registrieren", command=self._switch_mode)
        self.switch_button.grid(row=4, column=0, columnspan=2)

    def _draw_login(self):
        if self.mode == "login":
            self.title_label.config(text="Login")
            self.action_button.config(text="Einloggen")
            self.switch_button.config(text="Noch kein Konto? Registrieren")
        else:
            self.title_label.config(text="Registrierung")
            self.action_button.config(text="Registrieren")
            self.switch_button.config(text="Schon registriert? Zum Login")

    def _switch_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self._draw_login()

    def _handle_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Fehler", "Benutzername und Passwort dürfen nicht leer sein.")
            return

        if self.mode == "login":
            if username in self.users and self.users[username] == password:
                messagebox.showinfo("Erfolg", f"Willkommen zurück, {username}!")
            else:
                messagebox.showerror("Fehler", "Ungültige Zugangsdaten.")
        else:  # Registrierung
            if username in self.users:
                messagebox.showerror("Fehler", "Benutzername existiert bereits.")
            else:
                self.users[username] = password
                save_users(self.users)
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich! Du kannst dich jetzt einloggen.")
                self._switch_mode()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()