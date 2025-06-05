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
        self.channel = pygame.mixer.Channel(index)

        # GUI-Elemente
        self.frame = tk.Frame(master)
        self.frame.grid(row=index, column=0, sticky="ew", padx=5, pady=5)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=0)

        self.button = tk.Button(self.frame, text=f"Button {index+1}")
        self.button.grid(row=0, column=0, sticky="ew")
        self.button.bind("<Button-1>", self.toggle_play)
        self.button.bind("<Button-3>", self.choose_sound)

        self.volume_slider = tk.Scale(self.frame, from_=0, to=1, resolution=0.01,
                                      orient=tk.HORIZONTAL, label="Lautstärke", command=self.update_volume)
        self.volume_slider.set(self.volume)
        self.volume_slider.grid(row=0, column=1, sticky="ew")

        self.loop_var = tk.BooleanVar(value=self.loop_enabled)
        self.loop_checkbox = tk.Checkbutton(self.frame, text="Loop", variable=self.loop_var)
        self.loop_checkbox.grid(row=0, column=2, sticky="w")

    def toggle_play(self, event=None):
        if not self.sound_path:
            return

        if self.is_playing:
            self.channel.stop()
            self.is_playing = False
        else:
            try:
                sound = pygame.mixer.Sound(self.sound_path)
                sound.set_volume(self.volume_slider.get())
                loops = -1 if self.loop_var.get() else 0
                self.channel.play(sound, loops=loops)
                self.is_playing = True
            except Exception as e:
                print(f"Fehler beim Abspielen von {self.sound_path}: {e}")

    def choose_sound(self, event=None):
        filepath = filedialog.askopenfilename(
            title="Sound auswählen",
            filetypes=[("Audio-Dateien", "*.wav *.mp3 *.ogg *.flac")]
        )
        if filepath:
            self.sound_path = filepath
            self.is_playing = False
            self.channel.stop()

    def update_volume(self, value=None):
        if self.channel.get_busy():
            self.channel.set_volume(float(value))

    def get_config(self):
        return {
            "sound": self.sound_path,
            "volume": self.volume_slider.get(),
            "loop": self.loop_var.get()
        }

class SoundApp:
    def __init__(self, root):
        self.root = root
        root.title("Soundboard")
        root.columnconfigure(0, weight=1)

        pygame.mixer.init()
        self.sound_buttons = []

        config = self.load_config()

        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=0, column=0, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)

        for i in range(10):
            btn_config = config.get(str(i), {})
            sb = SoundButton(self.button_frame, i, btn_config)
            self.sound_buttons.append(sb)

        self.quit_button = tk.Button(root, text="Beenden", command=self.quit_app)
        self.quit_button.grid(row=1, column=0, pady=10)

        # Fenster dynamisch anpassen
        root.rowconfigure(0, weight=1)
        for i in range(10):
            self.button_frame.rowconfigure(i, weight=1)

        # Regelmäßige Lautstärke-Aktualisierung (falls während Wiedergabe geändert)
        self.update_volumes()

    def update_volumes(self):
        for btn in self.sound_buttons:
            if btn.channel.get_busy():
                btn.update_volume(btn.volume_slider.get())
        self.root.after(200, self.update_volumes)

    def quit_app(self):
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