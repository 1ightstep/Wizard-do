import customtkinter as ctk
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import uuid

from pages.tasks.task_form import TaskForm
from pages.tasks.task import Task
from pages.tasks.tasks_view import TasksView
from pages.tasks.tasks_view_filter import TasksViewFilter

from database.database import Database


class Tasks(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.database = Database("/database/database")
        self.main_task_list = []
        self.dynamic_task_list = []

        self.title = ttk.Label(self, text="Tasks", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)

        self.task_form = TaskForm(self, self.create_task)
        self.task_form.pack(fill="x", ipady=10, side="top")

        self.tasks_view_filter = TasksViewFilter(self, self.search_task)
        self.tasks_view_filter.pack(side="left", ipady=10, ipadx=5, fill="both", expand=True)

        self.tasks_view = TasksView(self)
        self.tasks_view.pack(side="left", fill="both", expand=True)

        for task in self.database.return_all("tasks"):
            self.create_task(
                task_tag=task["task_tag"],
                task_name=task["task_name"],
                task_date=task["task_date"],
                task_time=task["task_time"],
            )

        master.protocol("WM_DELETE_WINDOW", self.task_page_end_event)

    def create_task(self, task_tag, task_name="", task_date="", task_time=""):
        task_id = uuid.uuid4()
        task_widget = Task(
            master=self.tasks_view.tasks_container,
            task_id=task_id,
            task_tag=task_tag,
            task_name=task_name,
            task_date=task_date,
            task_time=task_time,
            destroy_func=self.destroy_task,
            done_func=self.task_done
        )
        task_data_dict = {
            "task_id": task_id,
            "task_name": task_name,
            "task_tag": task_tag,
            "task_date": task_date,
            "task_time": task_time,
            "task_widget": task_widget,
            "task_status": "ongoing"
        }
        self.main_task_list.append(task_data_dict)
        self.tasks_view.add_task(task_widget)

    def destroy_task(self, task_id):
        for task in self.main_task_list:
            if task["task_id"] == task_id:
                task["task_widget"].destroy()
                self.main_task_list.remove(task)

    def task_done(self, task_id):
        for task in self.main_task_list:
            if task["task_id"] == task_id:
                task["task_status"] = "done"

    def search_task(self, val):
        self.dynamic_task_list = [
            task for task in self.main_task_list
            if any(val.lower() in str(t_vals).lower() for t_vals in list(task.values()))
        ]
        self.tasks_view.remove_all(self.main_task_list)
        self.tasks_view.add_all(self.dynamic_task_list)

    def task_page_end_event(self):
        temp = self.main_task_list
        for i in range(len(temp)):
            temp[i]["task_id"] = ""
            temp[i]["task_widget"] = ""
        self.database.replace_category("tasks", temp)
        self.master.destroy()
