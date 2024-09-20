import ttkbootstrap as ttk

from pages.dashboard.info import info
from pages.dashboard.dashboard_task_view import dashboard_tasks_view


class DashboardData:
    def __init__(self):
        pass


class Dashboard(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.title = ttk.Label(self, text="Dashboard", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)

        self.info = info(self)
        self.info.pack(side="top", fill="both", expand=True, padx=(6, 0))
        self.frame = ttk.Frame(self)
        self.frame.pack(side="bottom", fill="both", expand=True, pady=(0, 8))
        self.dashboard_tasks_view = dashboard_tasks_view(self.frame)
        self.dashboard_tasks_view.pack(side="left", fill="both", expand=True, padx=(6, 8))

        master.bind('<Configure>', lambda event: self.update())

    def update(self, event=None):
        self.master.update_idletasks()
        self.info.update_labels()
