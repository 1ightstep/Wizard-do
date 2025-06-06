import ttkbootstrap as ttk
import tkinter as tk


class Task(ttk.LabelFrame):
    def __init__(self, master, task_id, task_tag, task_name, task_date, task_time, task_status, destroy_func, done_func):
        self.styles = {
            "Goal": {
                "TLabelframe": "primary",
                "TLabel": "primary.TLabel",
                "TButton": "primary.TButton",
                "TCheckbutton": "primary.TCheckbutton"
            },
            "Urgent": {
                "TLabelframe": "danger",
                "TLabel": "danger.TLabel",
                "TButton": "danger.TButton",
                "TCheckbutton": "danger.TCheckbutton"
            },
            "Important": {
                "TLabelframe": "warning",
                "TLabel": "warning.TLabel",
                "TButton": "warning.TButton",
                "TCheckbutton": "warning.TCheckbutton"
            },
            "Medium": {
                "TLabelframe": "info",
                "TLabel": "info.TLabel",
                "TButton": "info.TButton",
                "TCheckbutton": "info.TCheckbutton"
            },
            "Low": {
                "TLabelframe": "success",
                "TLabel": "success.TLabel",
                "TButton": "success.TButton",
                "TCheckbutton": "success.TCheckbutton"
            }
        }
        super().__init__(master=master, text=f"{task_date}, {task_time}", bootstyle=self.styles[task_tag]["TLabelframe"], padding=5)
        self.check_var = tk.BooleanVar()
        if task_status == "ongoing":
            self.check_var.set(False)
        else:
            self.check_var.set(True)
        self.done_btn = ttk.Checkbutton(
            self,
            style=self.styles[task_tag]["TCheckbutton"],
            command=lambda: done_func(task_id),
            variable=self.check_var
        )
        self.done_btn.pack(side="left")

        self.task_name = ttk.Label(self, text=task_name, style=self.styles[task_tag]["TLabel"])
        self.task_name.pack(side="left")

        self.destroy_btn = ttk.Button(self, text="Delete", style=self.styles[task_tag]["TButton"], command=lambda: destroy_func(task_id))
        self.destroy_btn.pack(side="right")