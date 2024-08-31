import ttkbootstrap as ttk


class TasksViewFilter(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Task Filters")
        self.filter_done_btn = ttk.Button(self, text="Filter out done")
        self.filter_done_btn.pack(fill="x", expand=True)
        self.filter_ongoing_btn = ttk.Button(self, text="Filter out ongoing")
        self.filter_ongoing_btn.pack(fill="x", expand=True)
        self.filter_by_difficulty_btn = ttk.Button(self, text="Filter by difficulty")
        self.filter_by_difficulty_btn.pack(fill="x", expand=True)
        self.filter_by_status_btn = ttk.Button(self, text="Filter by status")
        self.filter_by_status_btn.pack(fill="x", expand=True)