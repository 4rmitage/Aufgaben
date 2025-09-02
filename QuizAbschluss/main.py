from ui.login_screen import LoginScreen
import tkinter as tk

def main():
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()