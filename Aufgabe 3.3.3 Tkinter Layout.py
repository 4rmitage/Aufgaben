import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x400")

label1 = tk.Label(root, text="Label 1", bg="green")
label1.pack()

label2 = ttk.Label(root, text="Label 2")
label2.pack()

root.mainloop()