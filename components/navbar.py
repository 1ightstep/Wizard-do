import ttkbootstrap as ttk
import tkinter as tk
class Navbar(ttk.Frame):
    def __init__(self, master, page_display_function):
        super().__init__(master)
        super().configure(style="primary.TFrame")
        self.link_dashboard_page = tk.Button(
            self,
            anchor="w",
            font=("Helvetica", 15),
            text="Dashboard",
            command=lambda: page_display_function("dashboard"))
        self.link_dashboard_page.pack(fill="x", ipadx=30)
        self.link_todo_page = tk.Button(
            self,
            anchor="w",
            font=("Helvetica", 15),
            text="Tasks",
            command=lambda: page_display_function("tasks")
        )
        self.link_todo_page.pack(fill="x", ipadx=30)
        self.link_settings_page = tk.Button(
            self,
            anchor="w",
            font=("Helvetica", 15),
            text="Settings",
            command=lambda: page_display_function("settings"),
        )
        self.link_settings_page.pack(fill="x", ipadx=30)


