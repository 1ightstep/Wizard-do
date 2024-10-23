import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.scrolled import ScrolledFrame

from database.database import Database
from pages.accounts import account_in, account_edit, account_create, account_delete, account_image


class AccountMenu(ttk.LabelFrame):
    def __init__(self, master, get_username, update_username):
        super().__init__(master=master, text="Profile")
        self.master = master
        self.database = Database("/database/database")
        self.get_username = get_username
        self.update_username = update_username
        self.account_view = ttk.Frame(self)
        self.account_view.pack(padx=5, pady=(0, 5), expand=True, side="left")
        self.profile_username = ttk.Label(
            self.account_view,
            font=("Helvetica", 16, "bold")
        )
        self.account_list_widgets = []
        self.selected_pfp = "public/images/meh.png"
        if get_username() == "Guest":
            picture = "public/images/meh.png"
            self.profile_username.config(text="Guest")
        else:
            picture = self.database.return_value("icon", f"{get_username()}")
            self.profile_username.config(text=get_username())
        self.picture_file = ImageTk.PhotoImage(Image.open(picture).resize((125, 125)))
        self.picture_edit_file = ImageTk.PhotoImage(Image.open("public/images/edit.png").resize((40, 40)))
        self.profile_picture_frame = ttk.Frame(self.account_view)
        self.profile_picture_frame.pack(padx=20, pady=(0, 10), expand=True)
        self.profile_picture_frame.columnconfigure((0, 0), weight=1, minsize=100)
        self.profile_picture_frame.rowconfigure((0, 0), weight=1, minsize=100)
        self.profile_picture = ttk.Label(
            self.profile_picture_frame,
            text=picture,
            image=self.picture_file
        )

        self.profile_picture.grid(row=0, column=0, rowspan=2, columnspan=2)
        self.profile_picture_edit_btn = ttk.Button(
            self.profile_picture_frame,
            image=self.picture_edit_file,
            padding=0,
            command=lambda: account_image.AccountImage(
                self,
                self,
                get_username
                )
            )
        self.profile_username.pack(padx=40, pady=(3, 20), expand=True)
        self.sign_out = ttk.Button(
            self.account_view,
            text="Sign Out",
            padding=5,
            command=lambda: self.sign_out_cmd(
                update_username
            )
        )
        self.sign_out.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.account_change = ttk.Button(
            self.account_view,
            text="Change Password",
            padding=5,
            command=lambda: account_edit.AccountEdit(
                get_username
            )
        )
        self.account_change.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.account_view2 = ttk.Frame(self)
        self.del_account = ttk.Button(
            self.account_view2,
            text="Delete Account",
            padding=5,
            width=42,
            command=lambda: account_delete.AccountDelete(
                get_username,
                update_username
            )
        )

        if self.profile_username.cget("text") == "Guest":
            self.del_account.config(state="disabled")
            self.account_change.configure(state="disabled")
            self.sign_out.configure(state="disabled")
        self.account_list_frame = ttk.LabelFrame(
            self.account_view2,
            text="All Accounts"
        )
        self.account_list_frame.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.account_list = ScrolledFrame(self.account_list_frame)
        self.account_list.pack(fill="both", expand=True)
        self.account_list_load()
        self.sign_up = ttk.Button(
            self.account_view2,
            text="Create Account",
            padding=5,
            width=42,
            command=lambda: account_create.AccountCreate(self)
        )
        self.del_account.pack(padx=5, pady=5, fill="x", side="bottom")
        self.sign_up.pack(padx=5, pady=5, fill="x", side="bottom")
        self.account_view2.pack(padx=5, pady=5, fill="both", expand=True, side="right")

    def account_list_load(self):
        for widgets in self.account_list_widgets:
            widgets.forget()
        self.account_list_widgets = []
        if self.database.return_all("accounts"):
            for account in self.database.return_all("accounts"):
                account_frame = AccountWidget(
                    self.account_list,
                    account["username"],
                    lambda e: account_in.AccountIn(
                        account["username"],
                        self,
                        self.get_username(),
                        self.update_username
                    )
                )
                self.account_list_widgets.append(account_frame)
                account_frame.pack(padx=(5, 15), pady=5, fill="x", expand=True, side="top")
        else:
            account_frame = ttk.Label(
                self.account_list,
                text="No accounts at the moment!\n",
                font=("Helvetica", 15)
            )
            self.account_list_widgets.append(account_frame)
            account_frame.pack(padx=5, pady=5, fill="x", expand=True, side="top")

    # function named sign_out_cmd to not mix up with button sign_out
    def sign_out_cmd(self, update_username):
        update_username("Guest")
        guest_photo = ImageTk.PhotoImage(Image.open("public/images/meh.png").resize((125, 125)))
        self.update_icon("public/images/meh.png", guest_photo)

    def update_icon(self, icon_var, icon_size_1):
        self.selected_pfp = icon_var
        self.profile_picture.configure(
            text=icon_var,
            image=icon_size_1
        )
        self.profile_picture.image = icon_size_1
        print(self.get_username())
        self.master.account_page_end_event(self.get_username())
        self.account_list_load()

    def update_ui(self, username):
        self.profile_username.config(text=username)
        if username and self.profile_username.cget("text") != "Guest":
            self.profile_picture_edit_btn.grid(row=1, column=1, sticky="se")
        else:
            self.profile_picture_edit_btn.grid_forget()
        if self.profile_username.cget("text") == "Guest":
            self.del_account.config(state="disabled")
            self.account_change.configure(state="disabled")
            self.sign_out.configure(state="disabled")
        else:
            self.del_account.config(state="normal")
            self.account_change.configure(state="normal")
            self.sign_out.configure(state="normal")
        self.account_list_load()


class AccountWidget(ttk.LabelFrame):
    def __init__(self, master, username, command):
        super().__init__(master=master)
        self.database = Database("/database/database")
        icon = ImageTk.PhotoImage(Image.open(f"{self.database.return_value("icon", username)}").resize((50, 50)))
        self.image = ttk.Label(
            self,
            image=icon
        )
        self.image.image = icon
        self.image.bind("<Button-1>", command)
        self.image.pack(side="left", pady=(0, 5), padx=(5, 0))
        self.button = ttk.Label(
            self,
            text=username,
            font=("Helvetica", 24)
        )
        self.button.bind("<Button-1>", command)
        self.button.pack(padx=(15, 0), fill="both", expand=True, side="left", pady=(0, 5))