import ttkbootstrap as ttk
from PIL import Image, ImageTk
from database.database import Database
from public.images.resources import img_to_number
from pages.accounts import account_in, account_edit, account_create
from tkinter import messagebox
from random import randint


class Accounts(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.title = ttk.Label(self, text="Account", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        self.profile_frame = ttk.LabelFrame(self, text="Profile", padding=5)
        self.profile_frame.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.pictures = img_to_number.pictures

        username = self.database.return_value("settings", "signed_in")
        try:
            password = self.database.search("accounts", "username", username)["password"]
        except KeyError:
            username = "Guest"
            password = ""
        if username == "Guest":
            picture = self.pictures[14]
        else:
            picture = self.pictures[randint(1, 25)]
        self.guest = ImageTk.PhotoImage(Image.open(picture))
        self.profile_picture_frame = ttk.Label(self.profile_frame,
                                               image=self.guest,
                                               padding=15)
        self.profile_picture_frame.grid(row=0, column=0, rowspan=2)
        self.profile_username = ttk.Label(self.profile_frame,
                                          font=("Helvetica", 10),
                                          text="Username:\n" + username,
                                          padding=10)
        self.profile_username.grid(row=0, column=1)
        self.pw_edited = "•" * len(password)
        self.profile_password = ttk.Label(self.profile_frame,
                                          font=("Helvetica", 10),
                                          text="Password:\n" + self.pw_edited,
                                          padding=10)
        self.profile_password.grid(row=0, column=2)

    def update_ui(self, username, password):
        if self.profile_username and self.profile_password:
            self.profile_username.configure(text="Username:\n" + username)
            self.profile_password.configure(text="Password:\n" + len(password) * "•")
