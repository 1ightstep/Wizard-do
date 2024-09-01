import ttkbootstrap as ttk
import tkinter as tk
from components import placeholder_entry


class TimeSelector(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.hour = tk.StringVar(value="00")
        self.minute = tk.StringVar(value="00")

        self.hour_spinbox = ttk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hour, width=2)
        self.colon_label = ttk.Label(self, text=":")
        self.minute_spinbox = ttk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minute, width=2)

        self.hour_spinbox.pack(side=tk.LEFT)
        self.colon_label.pack(side=tk.LEFT)
        self.minute_spinbox.pack(side=tk.LEFT)

    def get_time(self):
        return f"{self.hour.get():02d}:{self.minute.get():02d}"

class TaskForm(ttk.LabelFrame):
    def __init__(self, master, submit_func):
        super().__init__(master, text="Task Creation")
        self.submit_func = submit_func

        self.color_tag_mb = ttk.Menubutton(self, text="Tag", style="Outline.TMenubutton")
        self.color_tag_mb.pack(padx=5, side="left", fill="x", expand=True)
        self.color_tag_menu = tk.Menu(self.color_tag_mb)
        self.color_tag_mb["menu"] = self.color_tag_menu

        self.color_tag_var = tk.StringVar()
        self.color_tags = ["Red", "Orange", "Blue", "Green"]
        for color_tag in self.color_tags:
            self.color_tag_menu.add_radiobutton(
                label=color_tag,
                value=color_tag,
                variable=self.color_tag_var,
                command=lambda ct=color_tag: self.update_mb_style(ct)
            )

        self.task_name_input = placeholder_entry.PlaceholderEntry(self, placeholder="Task", style="primary.TEntry")
        self.task_name_input.pack(padx=5, side="left", fill="x", expand=True)

        self.calender = ttk.DateEntry(self)
        self.calender.pack(padx=5, side="left", fill="x", expand=True)

        self.submit_btn = ttk.Button(self, text="Create", command=self.create_task)
        self.submit_btn.pack(padx=5, side="left", fill="x", expand=True)

    def create_task(self):
        self.submit_func(
            self.task_name_input.get(),
            self.color_tag_var.get() if self.color_tag_var.get() else "Blue",
            self.calender.entry.get()
        )

    def update_mb_style(self, color_tag):
        style_dict = {
            "Red": "danger.TMenubutton",
            "Orange": "warning.TMenubutton",
            "Blue": "info.TMenubutton",
            "Green": "success.TMenubutton"
        }
        self.color_tag_mb.configure(style=style_dict[color_tag])