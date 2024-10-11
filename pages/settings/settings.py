import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from database.database import Database
from pages.settings import settings_account, settings_profile_pictures
from public.window_themes import window_themes as themes
from math import *


class Settings(ttk.Frame):
    def __init__(self, master, update_win_theme_func, account_page):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.title = ttk.Label(self, text="Settings", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)

        self.container = ScrolledFrame(self)
        self.container.pack(fill="both", expand=True)
        self.theme_frame_cols = int(sqrt(len(themes))) + 1
        self.theme_frame_rows = ceil(len(themes)/self.theme_frame_cols)
        self.theme_option_frame = ttk.LabelFrame(self.container, text='Themes', padding=5)
        self.theme_option_frame.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.theme_option_frame.grid_rowconfigure(tuple(range(self.theme_frame_rows)), weight=1, minsize=100)
        self.theme_option_frame.grid_columnconfigure(tuple(range(self.theme_frame_cols)), weight=1, minsize=100)

        self.account_dir = settings_account.AccountMenu(self.container)
        self.account_dir.pack(padx=5, pady=5, fill="both", expand=True, side="top")

        self.account_img = settings_profile_pictures.AccountImage(self.container)
        if self.database.return_value("settings", "signed_in"):
            self.account_img.pack(padx=5, pady=5, fill="both", expand=True, side="top")

        for index, theme in enumerate(themes):
            col = index % self.theme_frame_cols
            row = floor(index / self.theme_frame_cols)
            theme_btn = ttk.Button(
                self.theme_option_frame,
                text=theme,
                style=f"{theme}.TButton",
                command=lambda theme_name=theme: update_win_theme_func(theme_name)
            )
            theme_btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)