import json
import os

CONFIG_FILE = "sound_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")
    return {}

def save_config(buttons):
    config = {str(i): btn.get_config() for i, btn in enumerate(buttons)}
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Fehler beim Speichern der Konfiguration: {e}")