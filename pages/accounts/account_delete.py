import ttkbootstrap as ttk
import customtkinter as ctk
from tkinter import messagebox
from components import placeholder_entry
from database.database import Database
from pages.accounts import account


class AccountCreate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Delete Account")
        self.database = Database("/database/databases")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap("public/images/acc.ico")
        self.header = ctk.CTkLabel(self,
                                   text="Delete Account",
                                   font=("Helvetica", 20, "bold"))
        self.header.pack(fill="x", pady=(10, 0))
        self.account_make = account.Accounts
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.entry1 = ctk.CTkEntry(self.frame, placeholder_text="Password", corner_radius=5, width=250, height=50)
        self.entry1.configure(show="•")
        self.entry1.pack(pady=5, padx=10, side="top")
        self.entry2 = ctk.CTkEntry(self.frame, placeholder_text="Confirm Password", corner_radius=5, width=250,
                                   height=50)
        self.entry2.configure(show="•")
        self.entry2.pack(pady=5, padx=10, side="top")
        self.checkbox = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                        command=self.show)
        self.checkbox.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0,
                                    command=lambda: self.delete(self.entry1.get(), self.entry2.get()))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.entry1.bind("<Return>", lambda e: self.delete(self.entry1.get(), self.entry2.get()))
        self.entry2.bind("<Return>", lambda e: self.delete(self.entry1.get(), self.entry2.get()))
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()

    def show(self):
        if self.checkbox.get() == 1:
            self.entry1.configure(show="")
            self.entry2.configure(show="")
        else:
            self.entry1.configure(show="•")
            self.entry2.configure(show="•")

    def delete(self, password, confirm_password):
        account_del = self.database.return_value("settings", "signed_in")
        if self.entry1.get() != self.entry2.get():
            messagebox.showwarning("Passwords do not match!", "Passwords do not match, please try again")
            return
        if not account_del:
            messagebox.showinfo("Account Deletion Successful", "Your account has been successfully deleted!")
            self.account_make.update_ui(self, "Guest", "")
            self.database.delete_data("accounts", "username", f"{self.database.return_value("settings", "signed_in")}")
            self.database.create_data_category(password)
            self.withdraw()
            return
        if not password or not confirm_password:
            messagebox.showwarning("Empty Box!", "You forgot to fill in one of the boxes, try again")
            return