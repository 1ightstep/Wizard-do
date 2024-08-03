import customtkinter as ctk


class Settings(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=master.winfo_reqwidth())
        self.title = ctk.CTkLabel(self, text="Settings").pack(fill="x")