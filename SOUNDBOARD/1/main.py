import tkinter as tk
import pygame
from sound_button import SoundButton
from config_utils import load_config, save_config
from login import LoginApp  # <-- Importiere LoginApp aus login.py

class SoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sound Button App")

        pygame.mixer.init()
        self.sound_buttons = []

        self._load_buttons()
        self._create_quit_button()
        self._configure_grid()
        self._volume_update_loop()

    def _load_buttons(self):
        config = load_config()
        for i in range(10):
            btn_config = config.get(str(i), {})
            button = SoundButton(self.root, i, btn_config)
            self.sound_buttons.append(button)

    def _create_quit_button(self):
        quit_button = tk.Button(self.root, text="Beenden", command=self.quit)
        quit_button.grid(row=10, column=0, columnspan=3, pady=10, sticky="nsew")

    def _configure_grid(self):
        for i in range(11):
            self.root.rowconfigure(i, weight=1)
        for j in range(3):
            self.root.columnconfigure(j, weight=1)

    def _volume_update_loop(self):
        for btn in self.sound_buttons:
            if btn.channel and btn.channel.get_busy():
                btn.update_volume(btn.scale.get())
        self.root.after(200, self._volume_update_loop)

    def quit(self):
        save_config(self.sound_buttons)
        self.root.destroy()


# Hauptprogrammstart mit Login
if __name__ == "__main__":
    root = tk.Tk()

    def on_login_success():
        # Alle bisherigen Widgets (Login-GUI) löschen
        for widget in root.winfo_children():
            widget.destroy()
        # SoundApp starten
        SoundApp(root)

    # Login starten mit Callback für Erfolg
    LoginApp(root, on_success_callback=on_login_success)
    root.mainloop()