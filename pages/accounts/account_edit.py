import hashlib

import customtkinter as ctk

from database.database import Database


class AccountEdit(ctk.CTk):
    def __init__(self, get_username):
        super().__init__()
        self.database = Database("/database/database")
        self.title("Password Manager")
        self.geometry("500x400")
        self.iconbitmap("public/images/Wizard-Do.ico")
        self.resizable(False, False)
        self.header = ctk.CTkLabel(self,
                                   text="Change Password",
                                   font=("Helvetica", 20, "bold"))
        self.header.pack(fill="x", pady=(10, 0))
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.account = self.database.search("accounts",
                                            "username",
                                            f'{get_username()}')
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
                                    command=lambda: self.edit(
                                        self.entry1.get(),
                                        self.entry2.get(),
                                        self.entry3.get(),
                                        get_username
                                    ))
        self.entry1.bind("<Return>", lambda e: self.edit(
            self.entry1.get(),
            self.entry2.get(),
            self.entry3.get(),
            get_username
        ))
        self.entry2.bind("<Return>", lambda e: self.edit(
            self.entry1.get(),
            self.entry2.get(),
            self.entry3.get(),
            get_username
        ))
        self.entry3.bind("<Return>", lambda e: self.edit(
            self.entry1.get(),
            self.entry2.get(),
            self.entry3.get(),
            get_username
        ))
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

    def edit(self, old_password, new_password, new_password_2, get_username):
        for item in self.frame.winfo_children():
            if item == ctk.CTkButton:
                item.configure(border_color=['#979DA2', '#565B5E'])
                if not item.get():
                    item.configure(border_color="#dd0525")
                    return
        current_account = self.database.search("accounts", "username", f'{get_username()}')
        hashed = hashlib.md5()
        new_pw_edited = new_password.encode()
        hashed.update(new_pw_edited)
        hashed2 = hashlib.md5()
        old_pw_edited = old_password.encode()
        hashed2.update(old_pw_edited)
        # make sure the old password isn't the new password
        if hashed2.hexdigest() != current_account["password"]:
            self.entry1.configure(border_color="#dd0525")
            return
        # make sure confirm box matches new password
        elif new_password != new_password_2:
            self.entry2.configure(border_color="#dd0525")
            self.entry3.configure(border_color="#dd0525")
            return
        # if user "changes" the password, but it's the same as before
        elif old_password == new_password:
            self.entry1.configure(border_color="#dd0525")
            self.entry2.configure(border_color="#dd0525")
        # when it ACTUALLY changes the password
        else:
            self.database.replace_specific("accounts",
                                           self.account,
                                           {
                                               'username': self.account["username"],
                                               'password': hashed.hexdigest(),
                                               'email': self.account["email"]
                                           })
            self.protocol("WM_DELETE_WINDOW", self.withdraw())
