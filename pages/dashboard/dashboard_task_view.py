import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame


class DashboardTasksView(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(text="Tasks To-Do")

        self.ListFrame = ScrolledFrame(self, autohide=True, height=380)
        self.ListFrame.pack(fill="both", expand=True)

        self.frame1 = ttk.Frame(self.ListFrame)
        self.frame1.pack(side="left", fill="both")
        self.frame2 = ttk.Frame(self.ListFrame)
        self.frame2.pack(pady=10, side="right", fill="both")

        tasks = [
            "task1", "task2", "task3"]

        tasks_date = ("9/18/24", "9/19/24", "9/20/24")

        for task, date in zip(tasks, tasks_date):
            self.add_task(task, date)

    def add_task(self, task_text, tasks_date):

        task_label = ttk.Label(self.frame1, text=task_text, wraplength=300, font=("Helvetica", 12))
        task_label.pack(padx=10, pady=10, fill="x")

        label_height = task_label.winfo_reqheight()

        line_height = 18
        lines = int(label_height / line_height) + 1
        if lines > 2:
            padding = 14 + (0.09*lines)
        else:
            padding = 10.2
        print(lines)

        tasks_date = ttk.Label(self.frame2, text=tasks_date, font=("helvetica", 12))
        tasks_date.pack(padx=10, pady=(0, padding*lines))
