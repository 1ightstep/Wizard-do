import ttkbootstrap as ttk
import tkinter as tk


class PlaceholderEntry(ttk.Entry):
    def __init__(self, master, placeholder="placeholder", style="TEntry", **kwargs):
        super().__init__(master, style=style, **kwargs)
        self.focus_status = "out"
        self.placeholder = placeholder
        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)
        self.add_placeholder()

    def get_value(self):
        if self.focus_status == "out" and self.get() == self.placeholder:
            return ""
        else:
            return self.get()

    def add_placeholder(self, event=None):
        self.focus_status = "out"
        if not self.get():
            self.insert(0, self.placeholder)

    def clear_placeholder(self, event=None):
        self.focus_status = "in"
        if self.get() == self.placeholder:
            self.delete(0, tk.END)