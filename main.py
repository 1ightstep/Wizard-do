import customtkinter as ctk
import tkinter as tk
from components import navbar
from pages import dashboard, settings, todo
class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wizard-do")
        self.geometry("600x400")
        self.current_page = "dashboard"
        self.resizable(False, False)

        self.navbar = (navbar.Navbar(self, self.page_display_logic).pack(side="left", fill="y"))
        self.dashboard_page = dashboard.Dashboard(self)
        self.todo_page = todo.Todo(self)
        self.settings_page = settings.Settings(self)

        self.mainloop()
    def page_display_logic(self, page):
        self.dashboard_page.forget()
        self.todo_page.forget()
        self.settings_page.forget()
        if page == "dashboard":
            self.dashboard_page.pack()
        elif page == "todo":
            self.todo_page.pack()
        elif page == "settings":
            self.settings_page.pack()


if __name__ == "__main__":
    Main()
