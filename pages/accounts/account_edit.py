import customtkinter as ctk
from tkinter import messagebox
from database.database import Database
from pages.accounts import account


class AccountEdit(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.database = Database("/database/databases")
        self.title("Password Manager")
        self.geometry("500x350")
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
        self.entry1.pack(pady=(40, 5), padx=10, side="top", anchor="n")
        self.entry2 = ctk.CTkEntry(self.frame, placeholder_text="New password", corner_radius=5, width=250, 
                                   height=50)
        self.entry2.configure(show="•")
        self.entry2.pack(pady=5, padx=10, side="top")
        self.entry3 = ctk.CTkEntry(self.frame, placeholder_text="Confirm password", corner_radius=5, width=250,
                                   height=50)
        self.entry3.configure(show="•")
        self.entry3.pack(pady=5, padx=10, side="top")
        self.checkbox = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                        command=self.show)
        self.checkbox.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0,
                                    command=lambda: self.edit(self.entry1.get(), self.entry2.get()))
        self.entry1.bind("<Return>", lambda e: self.login(self.entry2.get()))
        self.entry2.bind("<Return>", lambda e: self.login(self.entry2.get()))
        self.entry3.bind("<Return>", lambda e: self.login(self.entry2.get()))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()
        
    def edit():
        return

    def show(self):
        if self.checkbox.get() == 1:
            self.entry2.configure(show="")
        else:
            self.entry2.configure(show="•")
    
    def edit(self, password):
        accounts = self.database.return_all("accounts")
        if self.entry2.get() != self.entry3.get():
            messagebox.showwarning("Password does not match!", "Passwords do not match, please try again")
            return
        