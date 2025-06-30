import json
import os

class UserManager:
    def __init__(self):
        self.users_file = "C:/Python/Aufgaben-1/Quiz Abschluss/data/users.json"
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4)

    def _load_users(self):
        with open(self.users_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_users(self, users):
        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)

    def register(self, username, password):
        users = self._load_users()
        if username in users:
            return False  # Benutzer existiert bereits
        users[username] = {
            "password": password,
            "last_score": None,
            "feedback": ""
        }
        self._save_users(users)
        return True

    def login(self, username, password):
        users = self._load_users()
        if username in users and users[username]["password"] == password:
            return True
        return False