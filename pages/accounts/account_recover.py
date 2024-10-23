import hashlib

import customtkinter as ctk

from database.database import Database


class AccountRecover(ctk.CTkFrame):
    def __init__(self, master, confirm_number, username):
        super().__init__(master=master)
        self.database = Database("/database/database")
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.username = username
        self.entry1 = ctk.CTkEntry(self.frame, placeholder_text="Confirmation Number", corner_radius=5, width=250,
                                   height=50)
        self.entry1.pack(pady=(40, 5), padx=10, side="top", anchor="n")
        self.entry2 = ctk.CTkEntry(self.frame, placeholder_text="New Password", corner_radius=5, width=250,
                                   height=50)
        self.entry2.configure(show="•")
        self.entry2.pack(pady=5, padx=10, side="top", anchor="n")
        self.entry3 = ctk.CTkEntry(self.frame, placeholder_text="Confirm password", corner_radius=5, width=250,
                                   height=50)
        self.entry3.configure(show="•")
        self.entry3.pack(pady=5, padx=10, side="top")
        self.checkbox1 = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                         command=self.show)
        self.checkbox1.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0,
                                    command=lambda: self.edit(confirm_number,
                                                              self.entry1.get(),
                                                              self.entry2.get(),
                                                              self.entry3.get()))
        self.entry2.bind("<Return>", lambda e: self.edit(confirm_number,
                                                         self.entry1.get(),
                                                         self.entry2.get(),
                                                         self.entry3.get()))
        self.entry3.bind("<Return>", lambda e: self.edit(confirm_number,
                                                         self.entry1.get(),
                                                         self.entry2.get(),
                                                         self.entry3.get()))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")

    def show(self):
        if self.checkbox1.get() == 1:
            self.entry3.configure(show="")
            self.entry2.configure(show="")
        else:
            self.entry3.configure(show="•")
            self.entry2.configure(show="•")

    def edit(self, confirm_number, number, new_password, new_password_2):
        for item in self.frame.winfo_children():
            if item == ctk.CTkButton:
                item.configure(border_color=['#979DA2', '#565B5E'])
                if not item.get():
                    item.configure(border_color="#dd0525")
                    return
        if str(number) != str(confirm_number):
            self.entry1.configure(border_color="#dd0525")
            return
        hashed = hashlib.md5()
        new_pw_edited = new_password.encode()
        hashed.update(new_pw_edited)
        # make sure confirm box matches new password
        if new_password != new_password_2:
            self.entry3.configure(border_color="#dd0525")
            return
        # when it ACTUALLY changes the password
        else:
            self.database.replace_specific(
                "accounts",
                {
                    'username': self.username,
                    'password': self.database.search("accounts", "username", self.username)["password"],
                    'email': self.database.search("accounts", "username", self.username)["email"]
                },
                {
                    'username': self.username,
                    'password': hashed.hexdigest(),
                    'email': self.database.search("accounts", "username", self.username)["email"]
                }
            )
            return
