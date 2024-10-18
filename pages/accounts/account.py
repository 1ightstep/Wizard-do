import ttkbootstrap as ttk
from PIL import Image, ImageTk
from database.database import Database
from public.images.resources import img_to_number
from pages.accounts import account_image


class Accounts(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.title = ttk.Label(self, text="Account", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        self.container = ttk.LabelFrame(self, text="Accounts")
        self.container.pack(padx=5, pady=5, fill="both", expand=True)
        self.profile_frame = ttk.Frame(self.container, padding=5)
        self.profile_frame.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.pictures = img_to_number.pictures

        self.account = self.database.search("accounts", "username",
                                            f'{self.database.return_value("settings", "signed_in")}')
        if not self.account:
            self.account = {
                'username': 'Guest',
                'password': '',
                'icon': 17
            }

        self.icon_number = ttk.Button(self, text=f"{self.account['icon']}")
        self.icon_frame = ttk.Frame(self.container)
        self.icon_frame.pack(padx=5, pady=5, fill="both", expand=True, side="left")

        self.acc_img = account_image.AccountImage(self.icon_frame, self)
        if self.database.return_value("settings", "signed_in"):
            self.acc_img.pack(pady=20, fill="both", expand=True)

        if self.account['username'] == "Guest":
            picture = self.pictures[14]
        else:
            picture = self.pictures[self.database.return_value("accounts", "icon")]
        self.picture_file = ImageTk.PhotoImage(Image.open(picture).resize((75, 75)))
        self.profile_picture_frame = ttk.Label(self.profile_frame,
                                          image=self.picture_file,
                                          padding=15)
        self.profile_picture_frame.grid(row=0, column=0, rowspan=2)
        self.profile_username = ttk.Label(self.profile_frame,
                                     font=("Helvetica", 10),
                                     text="Username:\n" + self.account['username'],
                                     padding=10)
        self.profile_username.grid(row=0, column=1)
        self.pw_edited = "•" * len(self.account['password'])
        self.profile_password = ttk.Label(self.profile_frame,
                                     font=("Helvetica", 10),
                                     text="Password:\n" + self.pw_edited,
                                     padding=10)
        self.profile_password.grid(row=0, column=2)
        master.protocol("WM_DELETE_WINDOW", self.account_page_end_event)

    def update_ui(self, username, tasks_page):
        if self.profile_username:
            self.profile_username.configure(text="Username:\n" + username)
            if username == "Guest":
                self.database.replace_data("settings", "signed_in", "")
            else:
                self.database.replace_data("settings", "signed_in", username)
            tasks_page.load_tasks(username)
    def update_icon(self, icon, icon_set):
        self.profile_picture_frame.configure(
            image=icon
        )
        self.icon_number.config(text=str(icon_set))

    def account_page_end_event(self):
        new_account = {
            'username': self.account['username'],
            'password': self.account['password'],
            'icon': int(self.icon_number.cget("text"))
        }
        print(str(self.account) + "\n" + str(new_account))
        # self.database.replace_specific("accounts",
        #                                current_account,
        #
        #                                )