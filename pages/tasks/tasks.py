import ttkbootstrap as ttk
import uuid
import datetime

from pages.tasks.task_form import TaskForm
from pages.tasks.task import Task
from pages.tasks.tasks_view import TasksView
from pages.tasks.tasks_view_filter import TasksViewFilter

from database.database import Database
from utils.ai import AI


class Tasks(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.database = Database("/database/database")
        self.tasks_done = 0
        self.main_task_list = []
        self.dynamic_task_list = []

        self.title = ttk.Label(self, text="Tasks", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)

        self.task_form = TaskForm(self, self.create_task)
        self.task_form.pack(fill="x", ipady=10, side="top")

        filter_func_dict = {
            "search": self.search_task,
            "by_time": self.filter_by_time,
            "by_tag": self.filter_by_tag,
            "show_reverse": self.show_reverse,
            "remove_done": self.remove_done,
            "clear_filters": self.clear_filters
        }
        self.tasks_view_filter = TasksViewFilter(self, filter_func_dict)
        self.tasks_view_filter.pack(side="left", ipady=10, ipadx=5, fill="both", expand=True)

        self.tasks_view = TasksView(self)
        self.tasks_view.pack(side="left", fill="both", expand=True)

        for task in self.database.return_all("tasks"):
            self.create_task(
                task_tag=task["task_tag"],
                task_name=task["task_name"],
                task_date=task["task_date"],
                task_time=task["task_time"],
                initial_load=True
            )
        master.protocol("WM_DELETE_WINDOW", self.task_page_end_event)

    def create_task(self, task_tag, task_name="", task_date="", task_time="", initial_load=False):
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
        if initial_load:
            self.dynamic_task_list.append(task_data_dict)
        self.tasks_view.add_task(task_widget)

    def destroy_task(self, task_id):
        for task in self.main_task_list:
            if task["task_id"] == task_id:
                task["task_widget"].destroy()
                self.main_task_list.remove(task)

    def task_done(self, task_id):
        for task in self.main_task_list:
            if task["task_id"] == task_id:
                if task["task_widget"].check_var.get():
                    task["task_status"] = "done"
                    self.tasks_done += 1
                else:
                    task["task_status"] = "ongoing"
                    self.tasks_done -= 1

    def search_task(self, val):
        self.dynamic_task_list = [
            task for task in self.main_task_list
            if any(val.lower() in str(t_vals).lower() for t_vals in list(task.values()))
        ]
        self.tasks_view.clear_view()
        self.tasks_view.add_all(self.dynamic_task_list)

    def filter_by_time(self, checked_val):
        if checked_val:
            self.dynamic_task_list = sorted(
                self.dynamic_task_list,
                key=lambda task: datetime.datetime.strptime(f"{task['task_date']} {task['task_time']}", '%m/%d/%Y %H:%M')
            )
            self.tasks_view.clear_view()
            self.tasks_view.add_all(self.dynamic_task_list)

    def filter_by_tag(self, checked_val):
        if checked_val:
            goal_list = [dict(task) for task in self.main_task_list if task["task_tag"] == "Goal"]
            urgent_list = [dict(task) for task in self.main_task_list if task["task_tag"] == "Urgent"]
            important_list = [dict(task) for task in self.main_task_list if task["task_tag"] == "Important"]
            medium_list = [dict(task) for task in self.main_task_list if task["task_tag"] == "Medium"]
            low_list = [dict(task) for task in self.main_task_list if task["task_tag"] == "Low"]
            self.dynamic_task_list = goal_list + urgent_list + important_list + medium_list + low_list
            self.tasks_view.clear_view()
            self.tasks_view.add_all(self.dynamic_task_list)

    def show_reverse(self, checked_val):
        if checked_val:
            self.dynamic_task_list = self.dynamic_task_list[::-1]
            self.tasks_view.clear_view()
            self.tasks_view.add_all(self.dynamic_task_list)

    def remove_done(self, checked_val):
        if checked_val:
            self.dynamic_task_list = [task for task in self.main_task_list if task["task_status"] == "ongoing"]
            self.tasks_view.clear_view()
            self.tasks_view.add_all(self.dynamic_task_list)

    def clear_filters(self):
        self.tasks_view.clear_view()
        self.tasks_view.add_all(self.main_task_list)

    def task_page_end_event(self):
        temp = self.main_task_list
        for i in range(len(temp)):
            temp[i]["task_id"] = ""
            temp[i]["task_widget"] = ""
        self.database.replace_category("tasks", temp)
        self.master.destroy()
