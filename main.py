import ttkbootstrap as ttk

from database.database import Database
from components import navbar

from pages.accounts import account
from pages.settings import settings, settings_account, settings_profile_pictures
from pages.dashboard import dashboard
from pages.tasks import tasks

from public.window_themes import window_themes
from public.window_themes import window_themes_color


class Main(ttk.Window):
    def __init__(self):
        super().__init__()
        self.database = Database("/database/databases")
        self.window_style = ttk.Style(theme="cosmo")
        self.title("Wizard-do")
        self.geometry("1000x600")
        self.current_page = "dashboard"
        self.resizable(True, True)
        self.settings_setup()

        self.navbar = (navbar.Navbar(self, self.page_display_logic).pack(side="left", fill="y"))
        self.accounts_page = account.Accounts(self)
        self.dashboard_page = dashboard.Dashboard(self)
        self.tasks_page = tasks.Tasks(self)
        self.settings_page = settings.Settings(self, self.update_window_theme, self.accounts_page)

        self.dashboard_page.pack(fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", lambda: exit())
        self.mainloop()

    def page_display_logic(self, page):
        self.dashboard_page.forget()
        self.tasks_page.forget()
        self.settings_page.forget()
        self.accounts_page.forget()
        if page == "dashboard":
            self.dashboard_page.pack(fill="both", expand=True)
        elif page == "tasks":
            self.tasks_page.pack(fill="both", expand=True)
            tasks.Tasks(self)
        elif page == "settings":
            self.settings_page.pack(fill="both", expand=True)
        elif page == "accounts":
            self.accounts_page.pack(fill="both", expand=True)

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

    def settings_setup(self):
        if not self.database.category_exists("settings"):
            self.database.create_data_category("settings")
            self.database.replace_category(
                "settings",
                [
                    {"window_theme": "cosmo"},
                ]
            )
        self.update_window_theme(self.database.return_value("settings", "window_theme"))


if __name__ == "__main__":
    Main()