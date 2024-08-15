import customtkinter as ctk
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.scrolled import ScrolledFrame
from components import placeholderEntry as phE
import uuid


class TaskForm(ttk.LabelFrame):
    def __init__(self, master, submit_func):
        super().__init__(master, text="Task Creation")
        self.submit_func = submit_func

        self.color_tag_mb = ttk.Menubutton(self, text="Tag", style="Outline.TMenubutton")
        self.color_tag_mb.pack(padx=5, side="left")
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

        self.task_name_input = phE.PlaceholderEntry(self, placeholder="Task", style="primary.TEntry")
        self.task_name_input.pack(padx=5, side="left")

        self.calender = ttk.DateEntry(self)
        self.calender.pack(padx=5, side="left")

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


class Task(ttk.LabelFrame):
    def __init__(self, master, task_id, task_name, task_tag, task_date, destroy_func, done_func):
        self.styles = {
            "Red": {
                "TLabelframe": "danger",
                "TLabel": "danger.TLabel",
                "TButton": "danger.TButton",
                "TCheckbutton": "danger.TCheckbutton"
            },
            "Orange": {
                "TLabelframe": "warning",
                "TLabel": "warning.TLabel",
                "TButton": "warning.TButton",
                "TCheckbutton": "warning.TCheckbutton"
            },
            "Blue": {
                "TLabelframe": "info",
                "TLabel": "info.TLabel",
                "TButton": "info.TButton",
                "TCheckbutton": "info.TCheckbutton"
            },
            "Green": {
                "TLabelframe": "success",
                "TLabel": "success.TLabel",
                "TButton": "success.TButton",
                "TCheckbutton": "success.TCheckbutton"
            }
        }

        super().__init__(master=master, text=task_date, bootstyle=self.styles[task_tag]["TLabelframe"], padding=5)
        self.done_btn = ttk.Checkbutton(self, style=self.styles[task_tag]["TCheckbutton"], command=lambda: done_func(task_id))
        self.done_btn.pack(side="left")
        self.task_name = ttk.Label(self, text=task_name, style=self.styles[task_tag]["TLabel"])
        self.task_name.pack(side="left")

        self.destroy_btn = ttk.Button(self, text="Destroy", style=self.styles[task_tag]["TButton"], command=lambda: destroy_func(task_id))
        self.destroy_btn.pack(side="right")


class TasksView(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Tasks View")
        self.tasks_container = ScrolledFrame(self)
        self.tasks_container.pack(fill="both", expand=True)

    def add_task(self, task_widget):
        task_widget.pack(side="top", padx=10, fill="both", expand=True)


class TasksViewFilter(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Task Filters")


class Tasks(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.task_list = []
        self.title = ttk.Label(self, text="Tasks", font=("Helvetica", 20, "bold"), foreground="black")
        self.title.pack(fill="x")
        self.task_form = TaskForm(self, self.create_task)
        self.task_form.pack(fill="x", ipady=10)
        self.tasks_view_filter = TasksViewFilter(self)
        self.tasks_view_filter.pack(side="left", fill="both", expand=True)
        self.tasks_view = TasksView(self)
        self.tasks_view.pack(side="left", fill="both", expand=True)

    def create_task(self, task_name="", task_tag="Blue", task_date=""):
        task_id = uuid.uuid4()
        task_widget = Task(
            master=self.tasks_view.tasks_container,
            task_id=task_id,
            task_name=task_name,
            task_tag=task_tag,
            task_date=task_date,
            destroy_func=self.destroy_task,
            done_func=self.task_done
        )
        self.task_list.append({
            "task_id": task_id,
            "task_name": task_name,
            "task_tag": task_tag,
            "task_date": task_date,
            "task_widget": task_widget,
            "task_status": "ongoing"
        })
        self.tasks_view.add_task(task_widget)

    def destroy_task(self, task_id):
        for task in self.task_list:
            if task["task_id"] == task_id:
                task["task_widget"].destroy()
                self.task_list.remove(task)

    def task_done(self, task_id):
        for task in self.task_list:
            if task["task_id"] == task_id:
                task["task_status"] = "done"