import customtkinter as ctk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import numpy as np
import matplotlib.pyplot

import public.window_themes

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image

Image.CUBIC = Image.BICUBIC


class DashboardData:
    def __init__(self):
        pass


class Dashboard(ttk.Frame):
    def __init__(self, master, hexclr, drkthm):
        super().__init__(master)
        self.hex = hexclr
        self.theme = drkthm

        self.title = ttk.Label(self, text="Dashboard", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)

    def add_task(self, task_text):
        task_label = ttk.Label(self.ListFrame, text=task_text, wraplength=275, font=("Helvetica", 12))
        task_label.pack(padx=5, pady=5, fill="x")

    def construct(self):
        tasks = ["task1", "task2", "task3"]

        self.TopFrame = ttk.Frame(self)
        self.TopFrame.pack(anchor=ttk.N, fill="both", expand=True)

        self.EndFrame = ttk.Frame(self)
        self.EndFrame.pack(anchor=ttk.SW, fill="both", expand=True)

        self.Frame1 = ttk.Frame(self.TopFrame)
        self.Frame1.pack(side=ttk.LEFT, anchor=ttk.N, fill="both", expand=True)

        self.Frame2 = ttk.Frame(self.TopFrame)
        self.Frame2.pack(side=ttk.LEFT, anchor=ttk.N, fill="both", expand=True)

        self.Frame3 = ttk.Frame(self.TopFrame)
        self.Frame3.pack(side=ttk.LEFT, anchor=ttk.N, fill="both", expand=True)

        self.Frame4 = ttk.Frame(self.TopFrame)
        self.Frame4.pack(side=ttk.LEFT, anchor=ttk.N, fill="both", expand=True)

        self.Frame5 = ttk.Frame(self.EndFrame)
        self.Frame5.pack(pady=2, padx=5, side=ttk.LEFT, anchor=ttk.W, fill="both", expand=True)

        self.Frame6 = ttk.Frame(self.EndFrame)
        self.Frame6.pack(pady=2, padx=2, side=ttk.LEFT, anchor=ttk.E, fill="both", expand=True)

        self.TotalLeftFrame = ttk.LabelFrame(self.Frame1, width=200, height=100)
        self.TotalLeftFrame.pack_propagate(False)
        self.TotalLeftFrame.pack(padx=5, fill="both", expand=True)

        self.TLFrame = ttk.Frame(self.TotalLeftFrame)
        self.TLFrame.pack(side=ttk.LEFT, anchor=ttk.W)

        self.TotalLeft = ttk.Label(self.TLFrame, text="Total Tasks", font=("Helvetica", 10))
        self.TotalLeft.pack(pady=2, padx=2)

        self.TL = ttk.Label(self.TLFrame, text="50      ", font=("Helvetica", 18, "bold"))
        self.TL.pack(pady=15)

        self.CompletedTodayFrame = ttk.LabelFrame(self.Frame2, width=200, height=100)
        self.CompletedTodayFrame.pack_propagate(False)
        self.CompletedTodayFrame.pack(padx=5, fill="both", expand=True)

        self.CTFrame = ttk.Frame(self.CompletedTodayFrame)
        self.CTFrame.pack(side=ttk.LEFT, anchor=ttk.W)

        self.CompletedToday = ttk.Label(self.CTFrame, text="Completed Today",
                                        font=("Helvetica", 10))
        self.CompletedToday.pack(pady=2, padx=2)

        self.CT = ttk.Label(self.CTFrame, text="50          ", font=("Helvetica", 18, "bold"))
        self.CT.pack(pady=15)

        self.DifficultyFrame = ttk.LabelFrame(self.Frame3, width=200, height=100)
        self.DifficultyFrame.pack_propagate(False)
        self.DifficultyFrame.pack(padx=5, fill="both", expand=True)

        self.DFrame = ttk.Frame(self.DifficultyFrame)
        self.DFrame.pack(side=ttk.LEFT, anchor=ttk.W)

        self.Difficulty = ttk.Label(self.DFrame, text="Difficulty", font=("Helvetica", 10))
        self.Difficulty.pack(pady=2, padx=2)

        self.D = ttk.Label(self.DFrame, text="Medium", font=("Helvetica", 12, "bold"))
        self.D.pack(pady=15)

        self.AverageFrame = ttk.LabelFrame(self.Frame4, width=200, height=100)
        self.AverageFrame.pack_propagate(False)
        self.AverageFrame.pack(padx=5, fill="both", expand=True)

        self.AFFrame = ttk.Frame(self.AverageFrame)
        self.AFFrame.pack(side=ttk.LEFT, anchor=ttk.W)

        self.Average = ttk.Label(self.AFFrame, text="Average Time", font=("Helvetica", 10))
        self.Average.pack(pady=2, padx=2)

        self.AF = ttk.Label(self.AFFrame, text="50 minutes", font=("Helvetica", 12, "bold"))
        self.AF.pack(pady=15)

        self.LF = ttk.LabelFrame(self.Frame6, text="Tasks To-Do", width=457, height=397)
        self.LF.pack_propagate(False)
        self.LF.pack(padx=5, fill="both", expand=True)

        self.ListFrame = ScrolledFrame(self.LF, autohide=True)
        self.ListFrame.pack(fill="both", expand=True)

        for task in tasks:
            self.add_task(task)

        self.TotalCompleted = ttk.LabelFrame(self.Frame5, text="Total Tasks Completed")
        self.TotalCompleted.pack(fill="both", expand=True)

        fig, ax = plt.subplots(figsize=(4, 3))

        x = [1, 2, 3, 4, 5, 6]
        y = [1, 2, 3, 4, 5, 6]

        plt.title("Tasks Completed Over A Lifetime", color=self.hex, fontsize=10)
        plt.xlabel("Weeks", color=self.hex, fontsize=10)
        plt.ylabel("Tasks", color=self.hex, fontsize=10)
        ax.plot(x, y, color=self.hex, linewidth=2, linestyle="solid")
        ax.tick_params(axis='x', colors=self.hex)
        ax.tick_params(axis='y', colors=self.hex)

        plt.tight_layout()

        fig.patch.set_facecolor(self.theme)

        self.canvas = FigureCanvasTkAgg(fig, master=self.TotalCompleted)
        self.canvas.draw()

        self.canvas.get_tk_widget().config(width=500, height=380)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
