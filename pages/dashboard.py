import customtkinter as ctk


class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=400)
        self.title = ctk.CTkLabel(self, text="Dashboard").pack(fill="x")

