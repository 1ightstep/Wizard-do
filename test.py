import tkinter as tk
from tkinter import ttk
from ttkbootstrap import DateEntry
from datetime import datetime


class TimeSelector(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.hour = tk.StringVar(value="00")
        self.minute = tk.StringVar(value="00")

        self.hour_spinbox = ttk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hour, width=2)
        self.colon_label = ttk.Label(self, text=":")
        self.minute_spinbox = ttk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minute, width=2)

        self.hour_spinbox.pack(side=tk.LEFT)
        self.colon_label.pack(side=tk.LEFT)
        self.minute_spinbox.pack(side=tk.LEFT)

    def get_time(self):
        return f"{self.hour.get():02d}:{self.minute.get():02d}"


class DateAndTimeSelector(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.date_entry = DateEntry(self.master, width=10)
        self.time_selector = TimeSelector(self.master)

        self.button = ttk.Button(self, text="Select", command=self.open_selector)
        self.button.pack(side=tk.RIGHT)

        self.pack_forget()
        self.date_entry.pack_forget()
        self.time_selector.pack_forget()

    def open_selector(self):
        self.top = tk.Toplevel(self.master)
        self.top.title("Select Date and Time")

        self.date_label = ttk.Label(self.top, text="Date:")
        self.date_label.pack()

        self.date_entry.pack()

        self.time_label = ttk.Label(self.top, text="Time:")
        self.time_label.pack()

        self.time_selector.pack()

        self.ok_button = ttk.Button(self.top, text="OK", command=self.update_value)
        self.ok_button.pack()

    def update_value(self):
        selected_date = self.date_entry.get_date().strftime("%Y-%m-%d")
        selected_time = self.time_selector.get_time()

        self.delete(0, tk.END)
        self.insert(tk.END, f"{selected_date} {selected_time}")

        self.top.destroy()


# Create the main window
root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')

# Create the selector
selector = DateAndTimeSelector(root)
selector.pack(padx=10, pady=10)


# Example usage
def print_selected():
    print(selector.get())


ttk.Button(root, text="Print Selected", command=print_selected).pack(pady=10)

root.mainloop()