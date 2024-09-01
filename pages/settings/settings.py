import ttkbootstrap as ttk

class Settings(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.title = ttk.Label(self, text="Settings").pack(fill="x")