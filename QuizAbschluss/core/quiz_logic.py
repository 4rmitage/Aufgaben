import json
import random
import os

class QuizLogic:
    def __init__(self, username):
        self.username = username
        self.questions_file = "C:/Python/Aufgaben-1/QuizAbschluss/data/questions.json"
        self.users_file = "C:/Python/Aufgaben-1/QuizAbschluss/data/users.json"
        self.previous_score = self.load_previous_score()

    def load_previous_score(self):
        if not os.path.exists(self.users_file):
            return None

        with open(self.users_file, "r", encoding="utf-8") as file:
            users = json.load(file)

        user_data = users.get(self.username)
        if user_data and "last_score" in user_data:
            return user_data["last_score"]
        return None

    def get_random_questions(self, difficulty, count):
        if not os.path.exists(self.questions_file):
            return []

        with open(self.questions_file, "r", encoding="utf-8") as file:
            all_questions = json.load(file)

        filtered = [q for q in all_questions if q.get("difficulty") == difficulty]
        return random.sample(filtered, min(count, len(filtered)))

    def save_result(self, score, total):
        if not os.path.exists(self.users_file):
            users = {}
        else:
            with open(self.users_file, "r", encoding="utf-8") as file:
                users = json.load(file)

        previous = self.previous_score
        feedback = ""

        if previous is None:
            feedback = "Erstes Ergebnis gespeichert."
        elif score > previous:
            feedback = "Gut gemacht! Du hast dich verbessert."
        elif score < previous:
            feedback = "Du hast dich verschlechtert – probier’s nochmal!"
        else:
            feedback = "Gleich geblieben – halte das Niveau!"

        users[self.username]["last_score"] = score
        users[self.username]["feedback"] = feedback

        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)

    def get_feedback(self):
        if not os.path.exists(self.users_file):
            return ""

        with open(self.users_file, "r", encoding="utf-8") as file:
            users = json.load(file)

        return users.get(self.username, {}).get("feedback", "")