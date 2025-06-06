import tkinter as tk
from tkinter import messagebox
import json
import os

USER_FILE = "user_profiles.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

class LoginApp:
    def __init__(self, root, on_success):
        self.root = root
        self.users = load_users()
        self.mode = "login"
        self.on_success = on_success
        self._build_ui()

    def _build_ui(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        self.title = tk.Label(self.frame, text="Login", font=("Arial", 16))
        self.title.grid(row=0, column=0, columnspan=2)

        tk.Label(self.frame, text="Benutzername:").grid(row=1, column=0)
        self.username = tk.Entry(self.frame)
        self.username.grid(row=1, column=1)

        tk.Label(self.frame, text="Passwort:").grid(row=2, column=0)
        self.password = tk.Entry(self.frame, show="*")
        self.password.grid(row=2, column=1)

        self.button = tk.Button(self.frame, text="Einloggen", command=self._handle)
        self.button.grid(row=3, column=0, columnspan=2, pady=5)

        self.switch = tk.Button(self.frame, text="Noch kein Konto? Registrieren", command=self._toggle_mode)
        self.switch.grid(row=4, column=0, columnspan=2)

    def _toggle_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.title.config(text="Registrieren" if self.mode == "register" else "Login")
        self.button.config(text="Registrieren" if self.mode == "register" else "Einloggen")
        self.switch.config(
            text="Schon registriert? Zum Login" if self.mode == "register" else "Noch kein Konto? Registrieren")

    def _handle(self):
        user = self.username.get().strip()
        pw = self.password.get().strip()

        if not user or not pw:
            messagebox.showwarning("Fehler", "Benutzername und Passwort erforderlich")
            return

        if self.mode == "login":
            if user in self.users and self.users[user] == pw:
                self.on_success(user)
            else:
                messagebox.showerror("Fehler", "Ungültige Zugangsdaten")
        else:
            if user in self.users:
                messagebox.showerror("Fehler", "Benutzer existiert bereits")
            else:
                self.users[user] = pw
                save_users(self.users)
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich")
                self._toggle_mode()