import ttkbootstrap as ttk
from public.window_themes import window_themes as themes
from public.window_themes import window_themes_color as themes_dict
from math import *
import customtkinter as ctk
import tkinter as tk

class Settings(ttk.Frame):
    def __init__(self, master, update_win_theme_func):
        super().__init__(master)
        self.title = ttk.Label(self, text="Settings", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x")

        self.theme_frame_cols = int(sqrt(len(themes))) + 1
        self.theme_frame_rows = ceil(len(themes)/self.theme_frame_cols)
        self.theme_option_frame = ttk.LabelFrame(self, text='Themes', padding=5)
        self.theme_option_frame.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.theme_option_frame.grid_rowconfigure(tuple(range(self.theme_frame_rows)), weight=1)
        self.theme_option_frame.grid_columnconfigure(tuple(range(self.theme_frame_cols)), weight=1)

        for index, theme in enumerate(themes):
            col = index % self.theme_frame_cols
            row = floor(index / self.theme_frame_cols)
            theme_btn = ttk.Button(
                self.theme_option_frame,
                text=theme,
                style=f"{theme}.TButton",
                command=lambda theme_name=theme: update_win_theme_func(theme_name)
            )
            theme_btn.grid(row=row, column=col, sticky="nsew")

