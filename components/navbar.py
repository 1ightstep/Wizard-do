import customtkinter as ctk

class navbar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.title_display = ctk.CTkLabel(self, text="Menu")
        self.link_dashboard_page = ctk.CTkButton(self, text="Dashboard")
        self.link_todo_page = ctk.CTkButton(self, text="Todo List")
        self.link_settings_page = ctk.CTkButton(self, text="Settings")
