import tkinter as tk
from tkinter import ttk

def play_sound():
    print("Abspielen")  # Hier kannst du die Sound-Logik integrieren

def pause_sound():
    print("Pause")  # Hier kannst du die Sound-Logik integrieren

def stop_sound():
    print("Stopp")  # Hier kannst du die Sound-Logik integrieren

def set_volume(val):
    print(f"Lautstärke: {int(float(val))}")  # Hier kannst du die Lautstärke anpassen

# Hauptfenster erstellen
root = tk.Tk()
root.title("Soundbar GUI")
root.geometry("400x200")

# Buttons für Steuerung
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

play_button = ttk.Button(button_frame, text="Abspielen", command=play_sound)
play_button.grid(row=0, column=0, padx=5)

pause_button = ttk.Button(button_frame, text="Pause", command=pause_sound)
pause_button.grid(row=0, column=1, padx=5)

stop_button = ttk.Button(button_frame, text="Stopp", command=stop_sound)
stop_button.grid(row=0, column=2, padx=5)

# Lautstärkeregler
volume_label = ttk.Label(root, text="Lautstärke")
volume_label.pack()

volume_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=set_volume)
volume_slider.set(50)  # Anfangslautstärke
volume_slider.pack(pady=5)

# GUI starten
root.mainloop()