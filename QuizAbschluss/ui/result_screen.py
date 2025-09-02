import tkinter as tk
from core.quiz_logic import QuizLogic

def show_results(master, username, score, total):
    master.title("Auswertung")
    logic = QuizLogic(username)
    feedback = logic.get_feedback()

    tk.Label(master, text=f"Ergebnis für {username}", font=("Arial", 16)).pack(pady=10)
    tk.Label(master, text=f"Punkte: {score} von {total}", font=("Arial", 14)).pack(pady=5)
    tk.Label(master, text=f"Feedback: {feedback}", wraplength=400, justify="center").pack(pady=10)

    tk.Button(master, text="Beenden", command=master.quit).pack(pady=20)