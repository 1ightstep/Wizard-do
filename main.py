import customtkinter as ctk
import tkinter as tk
from components import navbar

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wizard-do")
        self.geometry("600x400")

        self.navbar = navbar.navbar(self).pack(side="left", fill="y")
        self.page_display = 0
        self.mainloop()

if __name__ == "__main__":
    Main()
