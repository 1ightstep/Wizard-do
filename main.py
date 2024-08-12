import ttkbootstrap as ttk
from ttkbootstrap import Style
from components import navbar
from pages import dashboard, settings, tasks
class Main(ttk.Window):
    def __init__(self):
        super().__init__(themename="yeti")
        self.title("Wizard-do")
        self.geometry("700x500")
        self.current_page = "dashboard"
        self.resizable(False, False)

        self.navbar = (navbar.Navbar(self, "gray", self.page_display_logic).pack(side="left", fill="y"))
        self.dashboard_page = dashboard.Dashboard(self)
        self.tasks_page = tasks.Tasks(self)
        self.settings_page = settings.Settings(self)

        self.mainloop()
    def page_display_logic(self, page):
        self.dashboard_page.forget()
        self.tasks_page.forget()
        self.settings_page.forget()
        if page == "dashboard":
            self.dashboard_page.pack(fill="both", expand=True, padx=5)
        elif page == "tasks":
            self.tasks_page.pack(fill="both", expand=True, padx=5)
        elif page == "settings":
            self.settings_page.pack(fill="both", expand=True, padx=5)


if __name__ == "__main__":
    Main()
