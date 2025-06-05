import tkinter as tk

# Erstelle das Hauptfenster
root = tk.Tk()
root.title("Button GUI mit Schleife")

# Erstelle einen Frame, um die Buttons zu halten
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

buttons = []
i = 0
# Erzeuge 4 Buttons mit einer while-Schleife
while i < 4:
    btn = tk.Button(frame, text=f"Button {i+1}", anchor='w', width=20)
    btn.pack(anchor='w')  # linksbündig
    buttons.append(btn)
    i += 1

# Erstelle den Button zum Schließen des Programms
def beenden():
    root.destroy()

schliessen_button = tk.Button(frame, text="Programm beenden", command=beenden)
schliessen_button.pack(anchor='w', pady=5)

# Starte die GUI
root.mainloop()