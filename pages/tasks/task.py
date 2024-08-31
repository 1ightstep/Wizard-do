import ttkbootstrap as ttk


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