import tkinter as tk
from tkinter import filedialog
import pygame

class SoundButton:
    def __init__(self, master, index, config):
        self.index = index
        self.sound_path = config.get("sound", "")
        self.volume = config.get("volume", 1.0)
        self.loop_enabled = config.get("loop", False)

        self.is_playing = False
        self.channel = None
        self.sound = None

        self._create_widgets(master)
        self._apply_config()

    def _create_widgets(self, master):
        self.button = tk.Button(master, text=f"Button {self.index+1}", width=20)
        self.button.grid(row=self.index, column=0, padx=5, pady=5, sticky="nsew")
        self.button.bind("<Button-1>", self.toggle_play)
        self.button.bind("<Button-3>", self.choose_sound)

        self.scale = tk.Scale(master, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL,
                              label="Lautstärke", command=self.update_volume)
        self.scale.grid(row=self.index, column=1, padx=5, pady=5, sticky="nsew")

        self.loop_var = tk.BooleanVar(value=self.loop_enabled)
        self.loop_checkbox = tk.Checkbutton(master, text="Loop", variable=self.loop_var)
        self.loop_checkbox.grid(row=self.index, column=2, padx=5, pady=5, sticky="nsew")

    def _apply_config(self):
        self.scale.set(self.volume)

    def toggle_play(self, event=None):
        if not self.sound_path:
            return

        if not self.is_playing:
            try:
                self.sound = pygame.mixer.Sound(self.sound_path)
                loops = -1 if self.loop_var.get() else 0
                self.channel = self.sound.play(loops=loops)
                if self.channel:
                    self.channel.set_volume(self.scale.get())
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
            self.is_playing = False

    def update_volume(self, value=None):
        if self.channel:
            try:
                self.channel.set_volume(float(value))
            except Exception as e:
                print(f"Fehler beim Setzen der Lautstärke: {e}")

    def get_config(self):
        return {
            "sound": self.sound_path,
            "volume": self.scale.get(),
            "loop": self.loop_var.get()
        }