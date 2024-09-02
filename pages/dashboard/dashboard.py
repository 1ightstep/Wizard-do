import customtkinter as ctk
import ttkbootstrap as ttk
class DashboardData:
    def __init__(self):
        pass
class Dashboard(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.title = ttk.Label(self, text="Dashboard", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x")


