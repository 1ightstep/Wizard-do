import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame


class TasksView(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Tasks View")
        self.task_widget_list = []
        self.tasks_container = ScrolledFrame(self)
        self.tasks_container.pack(fill="both", expand=True)

    def remove_all(self, task_list):
        for task in task_list:
            task["task_widget"].forget()

    def add_all(self, task_list):
        for task in task_list:
            task["task_widget"].pack(side="top", padx=10, fill="both", expand=True)

    def add_task(self, task_widget):
        self.task_widget_list.append(task_widget)
        task_widget.pack(side="top", padx=10, fill="both", expand=True)

