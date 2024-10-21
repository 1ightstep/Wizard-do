import datetime
import random
import time

import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import Image, ImageTk
from database.database import Database
Image.CUBIC = Image.BICUBIC


class QuoteWidget(ttk.LabelFrame):
    def __init__(self, master, title, content):
        super().__init__(master)
        self.content_label = ttk.Label(self, text=f"{title}", style="primary.TLabel", font=("Helvetica", 20, "bold"))
        self.content_label.pack(side="top", fill="x", anchor="w", padx=15, pady=15)
        self.content_v_label = ttk.Label(self, text=f"{content}", font=("Helvetica", 15, "bold"), wraplength=535)
        self.content_v_label.pack(side="top", fill="x", anchor="w", padx=15, pady=25)


class InfoWidget(ttk.LabelFrame):
    def __init__(self, master, title, a_used, a_total, subtext):
        super().__init__(master)
        self.title = ttk.Label(self, text=f"{title}", style="primary.TLabel", font=("Helvetica", 10, "bold"))
        self.title.pack(side="top", padx=10, pady=5, anchor="w")

        self.content = ttk.Meter(
            self,
            metersize=200,
            amounttotal=a_total,
            amountused=a_used,
            textleft=None,
            textright=None,
            subtext=subtext
        )
        self.content.pack()

    def refresh_ui_info(self, a_used, a_total, subtext):
        self.content.configure(amountused=a_used, amounttotal=a_total, subtext=subtext)


class InfoFrame(ttk.Frame):
    def __init__(self, master, task_list):
        super().__init__(master)
        self.task_list = task_list

        self.grid_rowconfigure((0, 1), weight=1, minsize=100)
        self.grid_columnconfigure((0, 1), weight=1, minsize=100)

        self.quote = QuoteWidget(self, "Quote of the day", self.get_quote())
        self.quote.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=1)

        self.total_tasks = InfoWidget(self,"Total Tasks", len(self.task_list), 1, "Total Tasks")
        self.total_tasks.grid(row=1, column=0, sticky="nsew", padx=5, pady=1)
        if len(self.task_list) < 1:
            self.tasks_completed = InfoWidget(self,"Tasks Completed", self.get_completed_tasks(), 1, "Tasks Completed")
        else:
            self.tasks_completed = InfoWidget(self, "Tasks Completed", self.get_completed_tasks(), len(task_list), "Tasks Completed")
        self.tasks_completed.grid(row=1, column=1, sticky="nsew", padx=5, pady=1)

    def get_completed_tasks(self):
        return len(list(task for task in self.task_list if task["task_status"] == "done"))

    def get_quote(self):
        with open("public/quotes.txt", "r") as f:
            quotes = [quote for quote in f.readlines() if quote != "\n"]
        return random.choice(quotes)

    def refresh_info(self):
        if len(self.task_list) < 1:
            self.tasks_completed.refresh_ui_info(self.get_completed_tasks(), 1, "Tasks Completed")
        else:
            self.tasks_completed.refresh_ui_info(self.get_completed_tasks(), len(self.task_list), "Tasks Completed")
        self.total_tasks.refresh_ui_info(len(self.task_list), 1, "Total Tasks")


class TaskWidget(ttk.Frame):
    def __init__(self, master, name, date):
        super().__init__(master)
        self.name_label = ttk.Label(self, text=name, wraplength=110)
        self.name_label.pack(side="left", padx=10, pady=5)

        self.date_label = ttk.Label(self, text=date)
        self.date_label.pack(side="right", padx=15, pady=5)


class TasksFrame(ttk.LabelFrame):
    def __init__(self, master, task_list):
        super().__init__(master, text="Upcoming Tasks")
        self.task_list = task_list
        self.scrolled_frame = ScrolledFrame(self)
        self.scrolled_frame.pack(fill="both", expand=True)

        self.task_widgets = []
        self.refresh_list(1)

    def refresh_list(self, username):
        filtered_list = list(task for task in self.task_list if task["task_status"] == "ongoing")
        filtered_list = sorted(
            filtered_list,
            key=lambda task: datetime.datetime.strptime(f"{task['task_date']} {task['task_time']}", '%m/%d/%Y %H:%M')
        )
        for widget in self.task_widgets:
            widget.destroy()
        for task in filtered_list:
            n_task_w = TaskWidget(self.scrolled_frame, task["task_name"], task["task_date"])
            n_task_w.pack(fill="x")
            self.task_widgets.append(n_task_w)


class Dashboard(ttk.Frame):
    def __init__(self, master, username, task_list):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.task_list = task_list
        self.title = ttk.Label(self, text=f"Hello, {username}", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        if not self.database.return_value("settings", "signed_in"):
            picture = "public/images/meh.png"
        else:
            picture = self.database.return_value("icon", f"{self.database.return_value("settings", "signed_in")}")
        month_to_name = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        date = time.strftime(f"%A, {month_to_name[time.localtime(time.time()).tm_mon]} %d, %Y ", time.localtime(time.time()))
        self.date = ttk.Label(self, text=f"Today is {date}")
        self.date.pack(fill="x")

        self.picture_file = ImageTk.PhotoImage(Image.open(picture).resize((75, 75)))
        self.label = ttk.Label(self,
                               image=self.picture_file,
                               )
        self.label.image = picture
        self.label.pack_propagate(False)
        self.label.place(relx=0.98, rely=0.02, anchor="ne")

        self.info_frame = InfoFrame(self, self.task_list)
        self.info_frame.place(relx=0, rely=0.15, relwidth=0.7, relheight=0.8)

        self.tasks_frame = TasksFrame(self, self.task_list)
        self.tasks_frame.place(relx=0.7, rely=0.15, relwidth=0.3, relheight=0.8)

    def refresh_ui(self, username):
        self.info_frame.refresh_info()
        if username:
            self.title.configure(text=f"Hello, {username}")
        else:
            self.title.configure(text="Hello, Guest")
