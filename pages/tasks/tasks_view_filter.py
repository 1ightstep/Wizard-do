import ttkbootstrap as ttk
from components.placeholder_entry import PlaceholderEntry
import tkinter as tk

class SearchBarFrame(ttk.Frame):
    def __init__(self, master, command):
        super().__init__(master)
        self.search_bar = PlaceholderEntry(self, placeholder="Search bar")
        self.search_btn = ttk.Button(self, text="Search", command=lambda: command(self.search_bar.get_value()))
        self.search_bar.pack(side="left", fill="x", expand=True, padx=5)
        self.search_btn.pack(side="left", padx=5)


class ManualFilters(ttk.Frame):
    def __init__(self, master, name, command):
        super().__init__(master)
        self.check_var = tk.BooleanVar()
        self.check_var.set(False)
        self.checkbox = ttk.Checkbutton(self, variable=self.check_var, command=lambda: command(self.check_var.get()))
        self.checkbox.pack(side="left", padx=5)

        self.name = ttk.Label(self, text=name)
        self.name.pack(side="right", padx=5)


class ManualFiltersFrame(ttk.LabelFrame):
    def __init__(self, master, func_dict):
        super().__init__(master, text="Manual Filters")
        self.grid_columnconfigure(tuple(range(2)), weight=1, minsize=1)
        self.grid_rowconfigure(tuple(range(3)), weight=1, minsize=1)

        self.by_time = ManualFilters(self, "Filter by time", func_dict["by_time"])
        self.by_time.grid(row=0, column=0, stick="nsw", pady=1)

        self.by_tag = ManualFilters(self, "Filter by tag", func_dict["by_tag"])
        self.by_tag.grid(row=0, column=1, stick="nsw", pady=1)

        self.show_reverse = ManualFilters(self, "Show reverse", func_dict["show_reverse"])
        self.show_reverse.grid(row=1, column=0, stick="nsw", pady=1)

        self.remove_done = ManualFilters(self, "Remove checked tasks", func_dict["remove_done"])
        self.remove_done.grid(row=1, column=1, stick="nsw", pady=1)

        self.clear_filters_btn = ttk.Button(
            self,
            text="Clear filters",
            command=lambda: (
                func_dict["clear_filters"],
                self.uncheck_all()
            )
        )
        self.clear_filters_btn.grid(row=3, column=0, columnspan=2, stick="nsew", pady=5, padx=5)

    def uncheck_all(self):
        self.by_time.check_var.set(False)
        self.by_tag.check_var.set(False)
        self.show_reverse.check_var.set(False)
        self.remove_done.check_var.set(False)


class TasksViewFilter(ttk.LabelFrame):
    def __init__(self, master, func_dict):
        super().__init__(master, text="Task Filters")
        self.search_bar = SearchBarFrame(self, command=func_dict["search"])
        self.search_bar.pack(side="top", fill="x")

        self.filters_frame = ManualFiltersFrame(self, func_dict)
        self.filters_frame.pack(side="top", fill="x", padx=5)
