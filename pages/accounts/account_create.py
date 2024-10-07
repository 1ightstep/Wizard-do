import ttkbootstrap as ttk
import customtkinter as ctk
from tkinter import messagebox
from components import placeholder_entry
from database.database import Database
from pages.accounts import account


class AccountCreate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Create Account")
        self.database = Database("/database/databases")
        self.geometry("500x350")
        self.resizable(False, False)
        self.iconbitmap("public/images/acc.ico")
        self.header = ctk.CTkLabel(self,
                                   text="Sign Up",
                                   font=("Helvetica", 20, "bold"))
        self.header.pack(fill="x", pady=(10, 0))
        self.account_make = account.Accounts
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.entry1 = ctk.CTkEntry(self.frame, placeholder_text="Username", corner_radius=5, width=250, height=50)
        self.entry1.pack(pady=(40, 5), padx=10, side="top", anchor="n")
        self.entry2 = ctk.CTkEntry(self.frame, placeholder_text="Password", corner_radius=5, width=250, height=50)
        self.entry2.configure(show="•")
        self.entry2.pack(pady=5, padx=10, side="top")
        self.entry3 = ctk.CTkEntry(self.frame, placeholder_text="Confirm Password", corner_radius=5, width=250, 
                                   height=50)
        self.entry3.configure(show="•")
        self.entry3.pack(pady=5, padx=10, side="top")
        self.checkbox = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                        command=self.show)
        self.checkbox.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0,
                                    command=lambda: self.sign_up(self.entry1.get(), self.entry2.get()))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.entry1.bind("<Return>", lambda e: self.login(self.entry1.get(), self.entry2.get()))
        self.entry2.bind("<Return>", lambda e: self.login(self.entry1.get(), self.entry2.get()))
        self.entry3.bind("<Return>", lambda e: self.login(self.entry1.get(), self.entry2.get()))
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()

    def show(self):
        if self.checkbox.get() == 1:
            self.entry2.configure(show="")
            self.entry3.configure(show="")
        else:
            self.entry2.configure(show="•")
            self.entry3.configure(show="•")

    def sign_up(self, username, password):
        accounts = self.database.return_all("accounts")
        if self.entry2.get() != self.entry3.get():
            messagebox.showwarning("Password does not match!", "Passwords do not match, please try again")
            return
        if accounts == []:
            messagebox.showinfo("Sign Up Successful", "Your account has been successfully created!")
            self.account_make.update_ui(self, username, password)
            self.database.add_data("accounts", {'username': username, 'password': password})
            self.database.create_data_category(username)
            self.withdraw()
            return
        for account in accounts:
            if account["username"] == username:
                messagebox.showerror("Username Taken!",
                                     "Username is already taken by someone else, please use a different one.")
                return
            messagebox.showinfo("Sign Up Successful", "Your account has been successfully created!")
            self.account_make.update_ui(self, username, password)
            self.database.add_data("accounts", {'username': username, 'password': password})
            self.database.create_data_category(username)
            self.withdraw()
            return