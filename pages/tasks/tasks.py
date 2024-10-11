import time

import ttkbootstrap as ttk
import uuid
import datetime
import threading

from pages.tasks.task_form import TaskForm
from pages.tasks.task import Task
from pages.tasks.tasks_view import TasksView
from pages.tasks.tasks_view_filter import TasksViewFilter

from database.database import Database
from utils.ai import AI


class Tasks(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.ai = AI()
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
            "clear_filters": self.clear_filters,
            "ai_filter": self.ai_filter
        }
        self.tasks_view_filter = TasksViewFilter(self, filter_func_dict)
        self.tasks_view_filter.pack(side="left", ipady=10, ipadx=5, fill="both", expand=True)

        self.tasks_view = TasksView(self)
        self.tasks_view.pack(side="left", fill="both", expand=True)
        
        # FIX on startup loading the wrong tasks
        if self.database.return_value("settings", "signed_in"):
            for task in self.database.return_all(self.database.return_value("settings", "signed_in")):
                self.create_task(
                    task_tag=task["task_tag"],
                    task_name=task["task_name"],
                    task_date=task["task_date"],
                    task_time=task["task_time"],
                    initial_load=True
                )
        else:
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
        month, day, year = task_date.split("/")
        if len(year) != 4:
            year = "20" + year
        try:
            datetime.datetime.strptime(f"{task_date} {task_time}", '%m/%d/%Y %H:%M')
        except ValueError as e:
            print(e)
            task_date = f"{time.localtime().tm_mon}/{time.localtime().tm_day}/{time.localtime().tm_year}"

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
        return task_data_dict

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

    def ai_filter(self, prompt):
        self.tasks_view_filter.ai_filter_frame.message_box.input.config(state="disabled")
        self.tasks_view_filter.ai_filter_frame.message_box.submit_btn.config(state="disabled")
        self.task_form.submit_btn.config(state="disabled")
        self.tasks_view_filter.ai_filter_frame.log_box.add_log("Please wait... Generations can take up to 5 minutes.", "primary")

        def thread_work():
            response = self.ai.filter_list(prompt, self.dynamic_task_list)
            if response["status"] == "success":
                self.dynamic_task_list = []
                for r_task in response["list"]:
                    if not r_task["to_create"]:
                        find_task = next((
                            m_task
                            for m_task in self.main_task_list
                            if r_task["task_name"] == m_task["task_name"] and r_task["task_date"] == m_task["task_date"] and r_task["task_time"] == m_task["task_time"]
                        ), None)
                        if find_task:
                            self.dynamic_task_list.append(find_task)
                    else:
                        new_task = self.create_task(r_task["task_tag"], r_task["task_name"], r_task["task_date"], r_task["task_time"])
                        self.dynamic_task_list.append(new_task)
                self.tasks_view.clear_view()
                self.tasks_view.add_all(self.dynamic_task_list)
                self.tasks_view_filter.ai_filter_frame.log_box.add_log("Success", "success")
            else:
                self.tasks_view_filter.ai_filter_frame.log_box.add_log("An error has occurred.", "danger")
            self.tasks_view_filter.ai_filter_frame.message_box.input.config(state="active")
            self.tasks_view_filter.ai_filter_frame.message_box.submit_btn.config(state="active")
            self.task_form.submit_btn.config(state="active")
        try:
            threading.Thread(target=thread_work).start()
        except Exception as e:
            print(e)
            self.tasks_view_filter.ai_filter_frame.log_box.add_log("An error has occurred.", "danger")
            self.tasks_view_filter.ai_filter_frame.message_box.input.config(state="active")
            self.tasks_view_filter.ai_filter_frame.message_box.submit_btn.config(state="active")
            self.task_form.submit_btn.config(state="active")

    def task_page_end_event(self):
        self.dynamic_task_list = self.main_task_list
        for task in self.dynamic_task_list:
            task["task_id"] = ""
            task["task_widget"] = ""
        if self.database.return_value("settings", "signed_in") == "":
            self.database.replace_category("tasks", self.dynamic_task_list)
        else:
            self.database.replace_category(f"{self.database.return_value("settings", "signed_in")}", self.dynamic_task_list)
        self.master.destroy()
