import customtkinter as ctk
from tkinter import messagebox
from database.database import Database
from pages.accounts import account


class AccountEdit(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.database = Database("/database/databases")
        self.title("Password Manager")
        self.geometry("500x400")
        self.resizable(False, False)
        self.header = ctk.CTkLabel(self,
                                   text="Change Password",
                                   font=("Helvetica", 20, "bold"))
        self.header.pack(fill="x", pady=(10, 0))
        self.account_set = account.Accounts
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.entry1 = ctk.CTkEntry(self.frame, placeholder_text="Original password", corner_radius=5, width=250, 
                                   height=50)
        self.entry1.configure(show="•")
        self.entry1.pack(pady=(40, 5), padx=10, side="top", anchor="n")
        self.checkbox1 = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                         command=lambda: self.show(1))
        self.checkbox1.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.entry2 = ctk.CTkEntry(self.frame, placeholder_text="New password", corner_radius=5, width=250, 
                                   height=50)
        self.entry2.configure(show="•")
        self.entry2.pack(pady=5, padx=10, side="top")
        self.entry3 = ctk.CTkEntry(self.frame, placeholder_text="Confirm password", corner_radius=5, width=250,
                                   height=50)
        self.entry3.configure(show="•")
        self.entry3.pack(pady=5, padx=10, side="top")
        self.checkbox2 = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                         command=lambda: self.show(2))
        self.checkbox2.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0,
                                    command=lambda: self.edit(self.entry1.get(), self.entry2.get(), self.entry3.get()))
        self.entry1.bind("<Return>", lambda e: self.edit(self.entry1.get(), self.entry2.get(), self.entry3.get()))
        self.entry2.bind("<Return>", lambda e: self.edit(self.entry1.get(), self.entry2.get(), self.entry3.get()))
        self.entry3.bind("<Return>", lambda e: self.edit(self.entry1.get(), self.entry2.get(), self.entry3.get()))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()

    def show(self, value):
        if value == 2:
            if self.checkbox2.get() == 1:
                self.entry2.configure(show="")
                self.entry3.configure(show="")
            else:
                self.entry2.configure(show="•")
                self.entry3.configure(show="•")
        else:
            if self.checkbox1.get() == 1:
                self.entry1.configure(show="")
            else:
                self.entry1.configure(show="•")
    
    def edit(self, old_password, new_password, new_password_2):
        current_account = self.database.search("accounts", "username", f'{self.database.return_value("settings", "signed_in")}')
        # make sure the old password isn't the new password
        if old_password != current_account["password"]:
            messagebox.showerror("Incorrect password!", "The old password doesn't match, try again")
            return
        # make sure confirm box matches new password
        elif new_password != new_password_2:
            messagebox.showwarning("Password does not match!", "Password and confirm password do not match, please try again")
            return
        # if user "changes" the password, but it's the same as before
        elif old_password == new_password:
            messagebox.showinfo("Nothing changed", "You set the password the same as before, nothing changed!")
        # when it ACTUALLY changes the password
        else:
            # fix this so it doesn't change all passwords, instead just one password
            new_account = {
                'username': self.database.return_value("settings", "signed_in"),
                'password': new_password
            }
            self.database.replace_specific("accounts", 'current_account', 'new_account')
            messagebox.showinfo("Success!", "Your password has been successfully changed!")
            self.protocol("WM_DELETE_WINDOW", self.withdraw())