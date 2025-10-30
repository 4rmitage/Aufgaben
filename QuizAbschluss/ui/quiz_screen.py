import tkinter as tk
from tkinter import messagebox
import random
from core.quiz_logic import QuizLogic
from ui.result_screen import show_results

class QuizScreen:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Quiz")
        self.username = username
        self.logic = QuizLogic(self.username)

        self.current_question = None
        self.selected_option = tk.StringVar()
        self.score = 0
        self.question_index = 0
        self.total_questions = 5
        self.question_pool = []

        self.create_start_screen()

    def create_start_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Wähle einen Schwierigkeitsgrad").pack(pady=10)
        self.difficulty = tk.StringVar(value="einfach")

        for level in ["einfach", "mittel", "schwer"]:
            tk.Radiobutton(self.master, text=level.capitalize(), variable=self.difficulty, value=level).pack(anchor="w")

        tk.Button(self.master, text="Quiz starten", command=self.start_quiz).pack(pady=20)

    def start_quiz(self):
        self.question_pool = self.logic.get_random_questions(self.difficulty.get(), self.total_questions)
        if not self.question_pool:
            messagebox.showerror("Fehler", "Nicht genug Fragen verfügbar!")
            return
        self.show_next_question()

    def show_next_question(self):
        if self.question_index >= self.total_questions:
            self.finish_quiz()
            return

        self.current_question = self.question_pool[self.question_index]
        self.selected_option.set("")

        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"Frage {self.question_index + 1} von {self.total_questions}").pack()
        tk.Label(self.master, text=self.current_question["question"], wraplength=400, justify="left").pack(pady=10)

        for option in self.current_question["options"]:
            tk.Radiobutton(self.master, text=option, variable=self.selected_option, value=option).pack(anchor="w")

        tk.Button(self.master, text="Weiter", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        selected = self.selected_option.get()
        if not selected:
            messagebox.showwarning("Achtung", "Bitte wähle eine Antwort aus.")
            return

        correct = self.current_question["answer"]
        if selected == correct:
            self.score += 1

        self.question_index += 1
        self.show_next_question()

    def finish_quiz(self):
        self.logic.save_result(self.score, self.total_questions)
        self.master.destroy()
        root = tk.Tk()
        show_results(root, self.username, self.score, self.total_questions)
        root.mainloop()