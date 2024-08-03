import customtkinter as ctk


class Todo(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=master.winfo_reqwidth())
        self.title = ctk.CTkLabel(self, text="Todo").pack(fill="x")

