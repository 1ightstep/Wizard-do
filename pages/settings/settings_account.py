import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import messagebox

from PIL import Image, ImageTk

from pages.accounts import account_in, account_edit, account_create, account_delete, account_image
from database.database import Database


class AccountMenu(ttk.LabelFrame):
    def __init__(self, master, dashboard_page, tasks_page):
        super().__init__(master=master, text="Profile")
        self.database = Database("/database/databases")

        self.account_view = ttk.Frame(self)
        self.account_view.pack(padx=5, pady=(0, 5), expand=True, side="left")
        self.profile_username = ttk.Label(self.account_view,
                                          font=("Helvetica", 16, "bold")
                                          )
        if not self.database.return_value("settings", "signed_in"):
            picture = "public/images/meh.png"
            self.profile_username.config(text="Guest")
        else:
            picture = self.database.return_value("icon", f"{self.database.return_value("settings", "signed_in")}")
            self.profile_username.config(text=self.database.return_value("settings", "signed_in"))
        self.picture_file = ImageTk.PhotoImage(Image.open(picture).resize((125, 125)))
        self.picture_edit_file = ImageTk.PhotoImage(Image.open("public/images/edit.png").resize((40, 40)))
        self.profile_picture_frame = ttk.Frame(self.account_view)
        self.profile_picture_frame.pack(padx=20, pady=(0, 10), expand=True)
        self.profile_picture_frame.columnconfigure((0, 0), weight=1, minsize=100)
        self.profile_picture_frame.rowconfigure((0, 0), weight=1, minsize=100)
        self.profile_picture = ttk.Label(self.profile_picture_frame,
                                         text=picture,
                                         image=self.picture_file
                                         )

        self.profile_picture.grid(row=0, column=0, rowspan=2, columnspan=2)
        self.profile_picture_edit_btn = ttk.Button(self.profile_picture_frame,
                                                   image=self.picture_edit_file,
                                                   padding=0,
                                                   command=lambda: account_image.AccountImage(self, self, dashboard_page)
                                                   )
        if self.database.return_value("settings", "signed_in"):
            self.profile_picture_edit_btn.grid(row=1, column=1, sticky="se")
        self.profile_username.pack(padx=40, pady=(3, 20), expand=True)
        self.sign_out = ttk.Button(self.account_view,
                                   text="Sign Out",
                                   padding=5,
                                   command=lambda: self.sign_out_cmd(self, dashboard_page, tasks_page))
        self.sign_out.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.account_change = ttk.Button(self.account_view,
                                         text="Change Password",
                                         padding=5,
                                         command=lambda: self.account_edit(self))
        self.account_change.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.del_account = ttk.Button(self.account_view,
                                      text="Delete Account",
                                      padding=5,
                                      command=lambda: self.delete_account(self, dashboard_page, tasks_page))
        if self.profile_username.cget("text") == "Guest":
            self.del_account.config(state="disabled")
            self.account_change.configure(state="disabled")
            self.sign_out.configure(state="disabled")
        self.del_account.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        self.account_view2 = ttk.Frame(self)

        self.account_list = ScrolledFrame(self)
        self.account_list.pack(padx=5, pady=5, fill="both", expand=True, side="top")
        if self.database.return_all("accounts"):
            for account in self.database.return_all("accounts"):
                account_button = ttk.Button(self.account_list,
                                            text=account["username"] + "     ---->",
                                            width=40,
                                            command=lambda: account_in.AccountIn(account["username"],
                                                                                 self,
                                                                                 dashboard_page,
                                                                                 tasks_page
                                                                                 ))
                account_button.pack(padx=5, pady=5, fill="x", expand=True, side="top")
        else:
            account_button = ttk.Label(self.account_list,
                                       text="No accounts at the moment!\nClick sign up to make your first account."
                                       )
            account_button.pack(padx=5, pady=5, fill="x", expand=True, side="top")
        self.sign_up = ttk.Button(self.account_view2,
                                  text="Create Account",
                                  padding=5,
                                  width=42,
                                  command=lambda: account_create.AccountCreate(self, dashboard_page, tasks_page))
        self.sign_up.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.account_view2.pack(padx=5, pady=5, expand=True, side="right")

    def account_edit(self, account_page):
        if self.database.return_value("settings", "signed_in") == "":
            messagebox.showwarning("No options", "Cannot edit guest accounts!\nIf you just created an account, restart the app to change your password.")
        else:
            account_edit.AccountEdit()

    # function named sign_out_cmd to not mix up with button sign_out
    def sign_out_cmd(self, account_page, dashboard_page, tasks_page):
        if self.profile_username.cget("text") != "Guest":
            if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
                self.database.replace_data("settings", "signed_in", "")
                account_page.update_ui("Guest", tasks_page, dashboard_page)
                dashboard_page.refresh_ui("Guest")
                guest_photo = ImageTk.PhotoImage(Image.open("public/images/meh.png"))
                dashboard_page.refresh_icon(guest_photo)
        else:
            messagebox.showwarning("Can't sign out", "You are on a guest account, can't sign out now!")

    def delete_account(self, account_page, dashboard_page, tasks_page):
        if self.database.return_value("settings", "signed_in"):
            account_delete.AccountDelete(account_page, dashboard_page, tasks_page)
            account_page.update_ui("Guest", tasks_page, dashboard_page)
            dashboard_page.refresh_ui("Guest")
        else:
            messagebox.showwarning("Can't sign out", "You are on a guest account!")

    def update_icon(self, icon_var, icon_size_1, icon_size_2, dashboard_page):
        dashboard_page.refresh_icon(icon_size_2)
        self.profile_picture.configure(
            text=icon_var,
            image=icon_size_1
        )
        self.profile_picture.image = icon_size_1

    def update_ui(self, username, tasks_page, dashboard_page):
        self.profile_username.config(text=username)
        tasks_page.load_tasks(username)
        dashboard_page.refresh_ui(username)
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

    def get_important_widgets(self):
        return [self.profile_username, self.profile_picture]

    def get_username(self):
        return self.profile_username.cget("text")
