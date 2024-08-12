import customtkinter as ctk


class Navbar(ctk.CTkFrame):
    def __init__(self, master, hover_color, page_display_function):
        super().__init__(master)
        self.configure(corner_radius=0, width=250, fg_color="#2B2B2B")
        self.link_dashboard_page = ctk.CTkButton(
            self,
            text="Dashboard",
            text_color="white",
            corner_radius=0,
            fg_color="#2B2B2B",
            hover_color=hover_color,
            font=('Helvetica', 15),
            anchor="w",
            command=lambda: page_display_function("dashboard"))
        self.link_dashboard_page.pack(fill="x")
        self.link_todo_page = ctk.CTkButton(
            self,
            text="Tasks",
            text_color="white",
            corner_radius=0,
            fg_color="#2B2B2B",
            hover_color=hover_color,
            font=('Helvetica', 15),
            anchor="w",
            command=lambda: page_display_function("tasks"))
        self.link_todo_page.pack(fill="x")
        self.link_settings_page = ctk.CTkButton(
            self,
            text="Settings",
            text_color="white",
            corner_radius=0,
            fg_color="#2B2B2B",
            hover_color=hover_color,
            font=('Helvetica', 15),
            anchor="w",
            command=lambda: page_display_function("settings"))
        self.link_settings_page.pack(fill="x")


