import ttkbootstrap as ttk
from tkinter import messagebox
from pages.accounts import account_in, account_edit, account_create, account_delete
from database.database import Database


class AccountMenu(ttk.LabelFrame):
    def __init__(self, master, account_page, dashboard_page):
        super().__init__(master=master, text="Profile")
        self.database = Database("/database/databases")

        # Five functions will use account_page because they update the ui: sign_up, sign_in, account_change, sign_out,
        # del_account
        # Only function that doesn't need to run through function first is account creation; nothing to check initially
        self.sign_up = ttk.Button(self,
                                  text="Sign Up",
                                  padding=5,
                                  command=lambda: account_create.AccountCreate(account_page, dashboard_page))
        self.sign_in = ttk.Button(self,
                                  text="Sign In",
                                  padding=5,
                                  command=lambda: self.account_in(account_page, dashboard_page))
        self.account_change = ttk.Button(self,
                                         text="Change Password",
                                         padding=5,
                                         command=lambda: self.account_edit(account_page))
        self.sign_out = ttk.Button(self,
                                   text="Sign Out",
                                   padding=5,
                                   width=45,
                                   command=lambda: self.sign_out_cmd(account_page, dashboard_page))
        self.del_account = ttk.Button(self,
                                      text="Delete Account",
                                      padding=5,
                                      width=45,
                                      command=lambda: self.delete_account(account_page, dashboard_page))
        self.sign_up.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.sign_in.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.account_change.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.sign_out.pack(padx=5, pady=5, fill="both", expand=True, side="bottom")
        self.del_account.pack(padx=5, pady=5, fill="both", expand=True, side="bottom")

    def account_edit(self, account_page):
        if self.database.return_value("settings", "signed_in") == "":
            messagebox.showwarning("No options", "Cannot edit guest accounts!\nIf you just created an account, restart the app to change your password.")
        else:
            account_edit.AccountEdit(account_page)

    def account_in(self, account_page, dashboard_page):
        try:
            if self.database.return_all("accounts"):
                account_in.AccountIn(account_page, dashboard_page)
            else:
                messagebox.showerror("No accounts available", "There are currently no accounts available!")
        except Exception as e:
            messagebox.showerror("Unknown error", "An unknown error occurred, can't sign in right now.")
            print(e)

    # function named sign_out_cmd to not mix up with button sign_out
    def sign_out_cmd(self, account_page, dashboard_page):
        if self.database.return_value("settings", "signed_in"):
            if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
                self.database.replace_data("settings", "signed_in", "")
                account_page.update_ui("Guest")
                dashboard_page.refresh_name("Guest")
        else:
            messagebox.showwarning("Can't sign out", "You are on a guest account, can't sign out now!")

    def delete_account(self, account_page, dashboard_page):
        if self.database.return_value("settings", "signed_in"):
            account_delete.AccountDelete(account_page, dashboard_page)
            account_page.update_ui("Guest")
            dashboard_page.refresh_name("Guest")
        else:
            messagebox.showwarning("Can't sign out", "You are on a guest account!")