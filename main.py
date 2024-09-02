import ttkbootstrap as ttk
from components import navbar
from pages.settings import settings
from pages.dashboard import dashboard
from pages.tasks import tasks
from public.window_themes import window_themes
from public.window_themes import window_themes_color

class Main(ttk.Window):
    def __init__(self):
        super().__init__()
        self.window_style = ttk.Style(theme="cosmo")
        for theme in window_themes:
            self.window_style.configure(
           f"{theme}.TButton",
                background=window_themes_color[theme],
            )
        self.title("Wizard-do")
        self.geometry("1000x600")
        self.current_page = "dashboard"
        self.resizable(True, True)

        self.navbar = (navbar.Navbar(self, self.page_display_logic).pack(side="left", fill="y"))
        self.dashboard_page = dashboard.Dashboard(self)
        self.tasks_page = tasks.Tasks(self)
        self.settings_page = settings.Settings(self, self.update_window_theme)

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
            )

if __name__ == "__main__":
    Main()
