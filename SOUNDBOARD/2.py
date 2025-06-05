import tkinter as tk
from tkinter import filedialog
import pygame
import json
import os

CONFIG_FILE = "sound_config.json"

class SoundButton:
    def __init__(self, master, index, sound_config):
        self.index = index
        self.sound_path = sound_config.get("sound", "")
        self.volume = sound_config.get("volume", 1.0)

        self.button = tk.Button(master, text=f"Button {index+1}", width=20)
        self.button.grid(row=index, column=0, padx=5, pady=5)
        self.button.bind("<Button-1>", self.play_sound)
        self.button.bind("<Button-3>", self.choose_sound)

        self.scale = tk.Scale(master, from_=0, to=1, resolution=0.01,
                              orient=tk.HORIZONTAL, label="Lautstärke")
        self.scale.set(self.volume)
        self.scale.grid(row=index, column=1, padx=5, pady=5)

    def play_sound(self, event=None):
        if self.sound_path:
            try:
                sound = pygame.mixer.Sound(self.sound_path)
                volume = self.scale.get()
                sound.set_volume(volume)
                sound.play()
            except Exception as e:
                print(f"Fehler beim Abspielen von Sound {self.sound_path}: {e}")

    def choose_sound(self, event=None):
        filepath = filedialog.askopenfilename(
            title="Sound auswählen",
            filetypes=[("Audio-Dateien", "*.wav *.mp3 *.ogg *.flac")]
        )
        if filepath:
            self.sound_path = filepath

    def get_config(self):
        return {
            "sound": self.sound_path,
            "volume": self.scale.get()
        }

class SoundApp:
    def __init__(self, root):
        self.root = root
        root.title("Sound Button App")

        pygame.mixer.init()

        self.sound_buttons = []

        config = self.load_config()

        for i in range(10):
            btn_config = config.get(str(i), {})
            btn = SoundButton(root, i, btn_config)
            self.sound_buttons.append(btn)

        self.quit_button = tk.Button(root, text="Beenden", command=self.quit)
        self.quit_button.grid(row=10, column=0, columnspan=2, pady=10)

    def quit(self):
        self.save_config()
        self.root.destroy()

    def save_config(self):
        config = {str(i): btn.get_config() for i, btn in enumerate(self.sound_buttons)}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")
        return {}

if __name__ == "__main__":
    root = tk.Tk()
    app = SoundApp(root)
    root.mainloop()