import customtkinter as ctk
import ttkbootstrap as ttk

class Settings(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure()
        self.title = ctk.CTkLabel(self, text="Settings").pack(fill="x")
