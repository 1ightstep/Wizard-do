import customtkinter as ctk


class Settings(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure()
        self.title = ctk.CTkLabel(self, text="Settings").pack(fill="x")
