import json
import os

def get_profile_path(username):
    return f"profile_{username}.json"

def load_profile(username):
    path = get_profile_path(username)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_profile(username, data):
    path = get_profile_path(username)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)