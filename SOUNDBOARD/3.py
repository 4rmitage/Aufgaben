import tkinter as tk
from tkinter import filedialog
import pygame
import json
import os

CONFIG_FILE = "sound_config.json"

class SoundButton:
    def __init__(self, master, index, config):
        self.index = index
        self.sound_path = config.get("sound", "")
        self.volume = config.get("volume", 1.0)
        self.loop_enabled = config.get("loop", False)
        self.is_playing = False
        self.channel = None
        self.sound = None

        self.button = tk.Button(master, text=f"Button {index+1}", width=20)
        self.button.grid(row=index, column=0, padx=5, pady=5)
        self.button.bind("<Button-1>", self.toggle_play)
        self.button.bind("<Button-3>", self.choose_sound)

        self.scale = tk.Scale(master, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Lautstärke", command=self.update_volume)
        self.scale.set(self.volume)
        self.scale.grid(row=index, column=1, padx=5, pady=5)

        self.loop_var = tk.BooleanVar(value=self.loop_enabled)
        self.loop_checkbox = tk.Checkbutton(master, text="Loop", variable=self.loop_var)
        self.loop_checkbox.grid(row=index, column=2, padx=5, pady=5)

    def toggle_play(self, event=None):
        if not self.sound_path:
            return
        if not self.is_playing:
            try:
                self.sound = pygame.mixer.Sound(self.sound_path)
                self.sound.set_volume(self.scale.get())
                loops = -1 if self.loop_var.get() else 0
                self.channel = self.sound.play(loops=loops)
                self.is_playing = True
            except Exception as e:
                print(f"Fehler beim Abspielen von Sound {self.sound_path}: {e}")
        else:
            if self.channel:
                self.channel.stop()
            self.is_playing = False

    def choose_sound(self, event=None):
        filepath = filedialog.askopenfilename(
            title="Sound auswählen",
            filetypes=[("Audio-Dateien", "*.wav *.mp3 *.ogg *.flac")]
        )
        if filepath:
            self.sound_path = filepath
            self.is_playing = False  # Reset status

    def update_volume(self, value=None):
        if self.channel:
            self.channel.set_volume(float(value))

    def get_config(self):
        return {
            "sound": self.sound_path,
            "volume": self.scale.get(),
            "loop": self.loop_var.get()
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
        self.quit_button.grid(row=10, column=0, columnspan=3, pady=10)

        self.update_volume_loop()

    def update_volume_loop(self):
        for btn in self.sound_buttons:
            if btn.channel and btn.channel.get_busy():
                btn.update_volume(btn.scale.get())
        self.root.after(200, self.update_volume_loop)

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