import customtkinter as ctk
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import uuid

from pages.tasks.task_form import TaskForm
from pages.tasks.task import Task
from pages.tasks.tasks_view import TasksView
from pages.tasks.tasks_view_filter import TasksViewFilter


class Tasks(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.task_list = []
        self.title = ttk.Label(self, text="Tasks", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        self.task_form = TaskForm(self, self.create_task)
        self.task_form.pack(fill="x", ipady=10, side="top")
        self.tasks_view_filter = TasksViewFilter(self)
        self.tasks_view_filter.pack(side="left", ipady=10, ipadx=5, fill="both", expand=True)
        self.tasks_view = TasksView(self)
        self.tasks_view.pack(side="left", fill="both", expand=True)

    def create_task(self, task_name="", task_tag="Blue", task_date="", task_time=""):
        task_id = uuid.uuid4()
        task_widget = Task(
            master=self.tasks_view.tasks_container,
            task_id=task_id,
            task_name=task_name,
            task_tag=task_tag,
            task_date=task_date,
            task_time=task_time,
            destroy_func=self.destroy_task,
            done_func=self.task_done
        )
        self.task_list.append({
            "task_id": task_id,
            "task_name": task_name,
            "task_tag": task_tag,
            "task_date": task_date,
            "task_time": task_time,
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
        print("YEAH")
        for task in self.task_list:
            if task["task_id"] == task_id:
                task["task_status"] = "done"