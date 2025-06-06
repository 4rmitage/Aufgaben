import tkinter as tk
from tkinter import filedialog
import pygame
from user_profile import load_profile, save_profile
from PIL import Image, ImageTk
import os

class SoundButton:
    def __init__(self, master, index, config):
        self.index = index
        self.config = config
        self.path = config.get("sound", "")
        self.volume = config.get("volume", 1.0)
        self.loop = tk.BooleanVar(value=config.get("loop", False))
        self.sound = None
        self.channel = None

        self.frame = tk.Frame(master, bd=1, relief="solid")
        self.frame.grid(row=index//5, column=index%5, sticky="nsew", padx=2, pady=2)
        self.frame.bind("<Configure>", self._resize_font)

        self.button = tk.Button(self.frame, text=str(index+1), command=self.toggle_play)
        self.button.pack(expand=True, fill="both")
        self.button.bind("<Button-3>", self.choose_file)

        self.check = tk.Checkbutton(self.frame, text="Loop", variable=self.loop)
        self.check.pack()

        self.scale = tk.Scale(self.frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=self.set_volume)
        self.scale.set(self.volume)
        self.scale.pack(fill="x")

    def _resize_font(self, event):
        size = min(event.width, event.height) // 5
        self.button.config(font=("Arial", size))

    def choose_file(self, event):
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.wav *.mp3 *.ogg *.flac")])
        if path:
            self.path = path
            self.config["sound"] = path

    def toggle_play(self):
        if not self.path:
            return
        if self.channel and self.channel.get_busy():
            self.channel.stop()
        else:
            try:
                self.sound = pygame.mixer.Sound(self.path)
                self.sound.set_volume(self.scale.get())
                loops = -1 if self.loop.get() else 0
                self.channel = self.sound.play(loops=loops)
            except Exception as e:
                print(f"Fehler beim Abspielen: {e}")

    def set_volume(self, val):
        if self.channel:
            self.channel.set_volume(float(val))

    def get_config(self):
        return {"sound": self.path, "volume": self.scale.get(), "loop": self.loop.get()}

class SoundBoardApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Soundboard - {username}")

        pygame.mixer.init()

        self.background = tk.Label(self.root)
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self._resize_bg)

        self.bg_img = Image.open("assets/background.jpg")
        self._resize_bg()

        self.buttons = []
        self.grid = tk.Frame(self.root)
        self.grid.pack(expand=True, fill="both")

        profile = load_profile(username)

        for i in range(15):
            conf = profile.get(str(i), {})
            btn = SoundButton(self.grid, i, conf)
            self.buttons.append(btn)

        control = tk.Frame(self.root)
        control.pack(pady=10)

        tk.Button(control, text="Beenden", command=self.root.quit).pack(side="left", padx=10)
        tk.Button(control, text="Zurücksetzen", command=self.reset).pack(side="right", padx=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _resize_bg(self, event=None):
        img = self.bg_img.resize((self.root.winfo_width(), self.root.winfo_height()))
        self.tk_img = ImageTk.PhotoImage(img)
        self.background.config(image=self.tk_img)

    def reset(self):
        for btn in self.buttons:
            btn.path = ""
            btn.config["sound"] = ""
            btn.scale.set(1.0)
            btn.loop.set(False)

    def on_close(self):
        data = {str(i): btn.get_config() for i, btn in enumerate(self.buttons)}
        save_profile(self.username, data)
        self.root.destroy()