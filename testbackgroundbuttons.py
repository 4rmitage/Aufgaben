import tkinter as tk
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hintergrundbild mit Tkinter")
        self.geometry("800x600")  # Anfangsgröße des Fensters

        # Laden des Hintergrundbildes
        self.original_image = Image.open("dein_bild.jpg")  # Ersetze den Dateinamen durch dein Bild
        self.background_label = tk.Label(self)
        self.background_label.place(relwidth=1, relheight=1)

        # Beispiel-Button, der über dem Hintergrund liegt
        btn = tk.Button(self, text="Klick mich")
        btn.pack(pady=20)

        # Binde die Resize-Event, um das Bild anzupassen
        self.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        # Verhindere unendliche Rekursion
        if event.widget == self:
            # Berechne die neue Größe
            new_width = event.width
            new_height = event.height

            # Skaliere das Bild auf die neue Fenstergröße
            resized_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.bg_image = ImageTk.PhotoImage(resized_image)

            # Aktualisiere das Label mit dem neuen Bild
            self.background_label.config(image=self.bg_image)

if __name__ == "__main__":
    app = App()
    app.mainloop()