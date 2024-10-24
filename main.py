import ttkbootstrap as ttk

from components import navbar
from database.database import Database
from pages.accounts import account
from pages.dashboard import dashboard
from pages.settings import settings
from pages.tasks import tasks
from public.window_themes import window_themes
from public.window_themes import window_themes_color


class Main(ttk.Window):
    def __init__(self):
        super().__init__()
        self.database = Database("/database/database")
        self.iconbitmap("public/images/Wizard-Do.ico")
        self.window_style = ttk.Style(theme="cosmo")
        self.title("Wizard-do")
        self.geometry("1000x600")
        self.current_page = "dashboard"
        self.resizable(True, True)
        self.username = "Guest"

        self.initial_setup()

        self.navbar = (navbar.Navbar(self,
                                     self.page_display_logic).pack(side="left", fill="y"))
        self.tasks_page = tasks.Tasks(self,
                                      "Guest"
                                      )
        self.dashboard_page = dashboard.Dashboard(
            self,
            self.username,
            self.tasks_page.main_task_list,
            self.get_username
        )
        self.settings_page = settings.Settings(self,
                                               self.update_window_theme)
        self.accounts_page = account.Accounts(self,
                                              self.get_username,
                                              self.update_username
                                              )
        self.dashboard_page.pack(fill="both", expand=True, padx=5)
        self.protocol("WM_DELETE_WINDOW", self.end_event)
        self.mainloop()

    def end_event(self):
        self.tasks_page.task_page_end_event()
        self.accounts_page.account_page_end_event(self.get_username())

    def page_display_logic(self, page):
        self.dashboard_page.forget()
        self.tasks_page.forget()
        self.settings_page.forget()
        self.accounts_page.forget()
        if page == "dashboard":
            self.dashboard_page.pack(fill="both", expand=True, padx=5)
            self.dashboard_page.refresh_ui(
                self.get_username(),
                self.tasks_page.main_task_list
            )
        elif page == "tasks":
            self.tasks_page.pack(fill="both", expand=True, padx=5)
            self.tasks_page.load_tasks(
                self.get_username()
            )
        elif page == "settings":
            self.settings_page.pack(fill="both", expand=True, padx=5)
        elif page == "accounts":
            self.accounts_page.pack(fill="both", expand=True, padx=5)

    def update_username(self, username):
        self.username = username
        self.tasks_page.load_tasks(username)
        self.accounts_page.frame.update_ui(username)
        self.dashboard_page.refresh_ui(
            username,
            self.tasks_page.main_task_list)

    def get_username(self):
        return self.username

    def update_window_theme(self, theme):
        self.window_style.theme_use(theme)
        for theme in window_themes:
            self.window_style.configure(
                f"{theme}.TButton",
                background=window_themes_color[theme],
                font=("Helvetic", 12),
                borderwidth=0,
                corner_radius=15
            )
        self.database.replace_data("settings", "window_theme", ttk.Style().theme_use())

    def initial_setup(self):
        if not self.database.category_exists("settings"):
            self.database.create_data_category("settings")
            self.database.replace_category(
                "settings",
                [
                    {"window_theme": "cosmo"},
                ]
            )
        categories = ["Guest", "accounts", "icon"]
        for category in categories:
            if not self.database.category_exists(category):
                self.database.create_data_category(category)

        self.update_window_theme(self.database.return_value("settings", "window_theme"))

if __name__ == "__main__":
    Main()
