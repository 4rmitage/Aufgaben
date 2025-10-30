import tkinter as tk
from tkinter import messagebox
from core.user_manager import UserManager
from ui.quiz_screen import QuizScreen

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Login")
        self.user_manager = UserManager()
        
        tk.Label(master, text="Benutzername").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Passwort").pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        tk.Button(master, text="Login", command=self.login).pack()
        tk.Button(master, text="Registrieren", command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.login(username, password):
            self.start_quiz(username)
        else:
            messagebox.showerror("Fehler", "Login fehlgeschlagen!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.register(username, password):
            messagebox.showinfo("Erfolg", "Registrierung erfolgreich!")
        else:
            messagebox.showerror("Fehler", "Benutzer existiert bereits.")

    def start_quiz(self, username):
        self.master.destroy()
        root = tk.Tk()
        QuizScreen(root, username)
        root.mainloop()