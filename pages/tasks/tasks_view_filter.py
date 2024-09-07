import ttkbootstrap as ttk
from components.placeholder_entry import PlaceholderEntry


class SearchBarFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.search_bar = PlaceholderEntry(self, placeholder="Search bar")
        self.search_btn = ttk.Button(self, text="Search")
        self.search_bar.pack(side="left", fill="x", expand=True, padx=5)
        self.search_btn.pack(side="left", padx=5)


class TasksViewFilter(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Task Filters")
        self.search_bar = SearchBarFrame(self)
        self.search_bar.pack(side="top", fill="x")