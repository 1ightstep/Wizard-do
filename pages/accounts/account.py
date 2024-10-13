import ttkbootstrap as ttk
from PIL import Image, ImageTk
from database.database import Database
from public.images.resources import img_to_number
from public.images.resources.img_to_number import pictures


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
        if username == "Guest":
            picture = self.pictures[17]
        else:
            picture = self.pictures[self.database.return_value("accounts", "icon")]
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

    def update_ui(self, username):
        if self.profile_username:
            self.profile_username.configure(text="Username:\n" + username)
            if username == "Guest":
                self.database.replace_data("settings", "signed_in", "")
            else:
                self.database.replace_data("settings", "signed_in", username)

    def update_icon(self, icon):
        self.profile_picture_frame.configure(
            image=icon
        )
