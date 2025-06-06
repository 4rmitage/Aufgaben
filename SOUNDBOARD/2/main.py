import tkinter as tk
from login import LoginApp
from soundboard import SoundBoardApp

def start():
    root = tk.Tk()

    def on_success(username):
        for widget in root.winfo_children():
            widget.destroy()
        SoundBoardApp(root, username)

    LoginApp(root, on_success)
    root.mainloop()

if __name__ == "__main__":
    start()
