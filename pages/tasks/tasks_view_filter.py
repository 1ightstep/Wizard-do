import ttkbootstrap as ttk
from components.placeholder_entry import PlaceholderEntry

class SearchBarFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.search_bar = PlaceholderEntry(self, placeholder="Search bar")
        self.search_btn = ttk.Button(self, text="Search")
        self.search_bar.pack(side="left", fill="x", expand=True)
        self.search_btn.pack(side="left")
class TasksViewFilter(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Task Filters")
        self.search_bar = SearchBarFrame(self)
        self.search_bar.pack(fill="x", expand=True, side="top")
        self.filter_done_btn = ttk.Button(self, text="Filter out done")
        self.filter_done_btn.pack(fill="x", expand=True)
        self.filter_ongoing_btn = ttk.Button(self, text="Filter out ongoing")
        self.filter_ongoing_btn.pack(fill="x", expand=True)
        self.filter_by_difficulty_btn = ttk.Button(self, text="Filter by difficulty")
        self.filter_by_difficulty_btn.pack(fill="x", expand=True)
        self.filter_by_status_btn = ttk.Button(self, text="Filter by status")
        self.filter_by_status_btn.pack(fill="x", expand=True)