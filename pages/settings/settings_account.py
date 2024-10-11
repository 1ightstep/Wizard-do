import ttkbootstrap as ttk
from tkinter import messagebox
from pages.accounts import account_in, account_edit, account_create, account
from database.database import Database


class AccountMenu(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master=master, text="Profile")
        self.database = Database("/database/databases")
        self.sign_up = ttk.Button(self,
                                  text="Sign Up",
                                  padding=5,
                                  width=45,
                                  command=account_create.AccountCreate)
        self.sign_in = ttk.Button(self,
                                  text="Sign In",
                                  padding=5,
                                  width=45,
                                  command=self.account_in)

        self.acc_change = ttk.Button(self,
                                     text="Change Password",
                                     padding=5,
                                     width=45,
                                     command=self.account_edit)
        self.sign_out = ttk.Button(self,
                                   text="Sign Out",
                                   padding=5,
                                   command=self.sign_out)
        self.sign_out.pack(padx=5, pady=5, fill="both", expand=True, side="bottom")
        self.sign_up.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.sign_in.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.acc_change.pack(padx=5, pady=5, fill="both", expand=True, side="left")

    def account_edit(self):
        if self.database.return_value("settings", "signed_in") == "":
            messagebox.showwarning("No options", "Cannot edit guest accounts!\nIf you just created an account, restart the app to change your password.")
        else:
            account_edit.AccountEdit()

    def account_in(self):
        try:
            if self.database.return_all("accounts"):
                account_in.AccountIn()
            else:
                messagebox.showerror("No accounts available", "There are currently no accounts available!")
        except Exception as e:
            messagebox.showerror("Unknown error", "An unknown error occurred, can't sign in right now.")

    def sign_out_cmd(self):
        if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
            self.database.replace_data("settings", "signed_in", "")
            self.account_page.update_ui("Guest", "")

    def sign_out(self):
        if self.database.return_value("settings", "signed_in"):
            if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
                self.database.replace_data("settings", "signed_in", "")
                # call update_ui to change to guest acc
        else:
            messagebox.showwarning("Can't sign out", "You are on a guest account, can't sign out now!")