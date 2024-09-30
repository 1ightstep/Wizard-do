import ttkbootstrap as ttk

from database.database import Database
from components import navbar

from pages.settings import settings
from pages.dashboard import dashboard
from pages.tasks import tasks

from public.window_themes import window_themes
from public.window_themes import window_themes_color


class Main(ttk.Window):
    def __init__(self):
        super().__init__()
        self.database = Database("/database/database")
        self.window_style = ttk.Style(theme="cosmo")
        self.title("Wizard-do")
        self.geometry("1000x600")
        self.current_page = "dashboard"
        self.resizable(True, True)

        self.settings_setup()

        self.navbar = (navbar.Navbar(self, self.page_display_logic).pack(side="left", fill="y"))
        self.dashboard_page = dashboard.Dashboard(self)
        self.tasks_page = tasks.Tasks(self)
        self.settings_page = settings.Settings(self, self.update_window_theme)

        self.dashboard_page.pack(fill="both", expand=True, padx=5)

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
