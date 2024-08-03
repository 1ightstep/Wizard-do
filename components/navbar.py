import customtkinter as ctk


class Navbar(ctk.CTkFrame):
    def __init__(self, master, page_display_function):
        super().__init__(master)
        self.configure(corner_radius=0, width=250)
        self.link_dashboard_page = ctk.CTkButton(
            self,
            text="  📊Dashboard",
            corner_radius=0,
            fg_color="#2B2B2B",
            anchor="w",
            command=lambda: page_display_function("dashboard"))
        self.link_dashboard_page.pack(fill="x")
        self.link_todo_page = ctk.CTkButton(
            self,
            text="  ✅Todo List",
            corner_radius=0,
            fg_color="#2B2B2B",
            anchor="w",
            command=lambda: page_display_function("todo"))
        self.link_todo_page.pack(fill="x")
        self.link_settings_page = ctk.CTkButton(
            self,
            text="  ⚙️Settings",
            corner_radius=0,
            fg_color="#2B2B2B",
            anchor="w",
            command=lambda: page_display_function("settings"))
        self.link_settings_page.pack(fill="x")


