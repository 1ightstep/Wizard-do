import hashlib
import smtplib
from random import randint
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image, ImageTk

from database.database import Database
from pages.accounts import account_recover


class AccountIn(ctk.CTk):
    def __init__(self, username, account_page, get_username, update_username):
        super().__init__()
        self.username = username
        self.title("Sign In")
        self.database = Database("/database/database")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap("public/images/Wizard-Do.ico")
        self.header = ctk.CTkLabel(self,
                                   text="Sign In",
                                   font=("Helvetica", 20, "bold"))
        self.header.pack(fill="x", pady=(10, 0))
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="Password", corner_radius=5, width=250, height=50)
        self.entry.configure(show="•")
        self.entry.pack(pady=(50, 5), padx=10, side="top")
        self.checkbox1 = ctk.CTkCheckBox(self.frame,
                                         width=25,
                                         height=25,
                                         text="Show Password",
                                         corner_radius=0,
                                         command=self.show)
        self.checkbox1.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.forgot_password = ctk.CTkButton(self.frame,
                                             width=25,
                                             height=25,
                                             text="Forgot Password?",
                                             border_width=0,
                                             border_color="#dd0525",
                                             command=lambda: self.save_account(username, get_username)
                                             )
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0, command=lambda: self.login(
            username,
            self.entry.get(),
            account_page,
            update_username
        ))
        self.entry.bind("<Return>", lambda e: self.login(
            username,
            self.entry.get(),
            account_page,
            update_username
        ))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.forgot_password.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()

    def show(self):
        if self.checkbox1.get() == 1:
            self.entry.configure(show="")
        else:
            self.entry.configure(show="•")

    def login(self, username, password, account_page, update_username):
        # return ALL accounts, sift through each one for matching account
        accounts = self.database.return_all("accounts")
        if username == "" or password == "":
            messagebox.showerror("Text Box is Empty!", "At least one of the entry boxes is empty, please try again!")
            return
        for instance in accounts:
            hashed = hashlib.md5()
            message = password.encode()
            hashed.update(message)
            if instance["username"] == username and str(hashed.hexdigest()) == instance["password"]:
                self.log_check(True, username, account_page, update_username)
                return
        self.log_check(False, None, None, None, None)

    def log_check(self, value, username, account_page, update_username):
        if value:
            update_username(username)

            account_page.update_ui(username)
            if username == "Guest":
                image = ImageTk.PhotoImage(Image.open("public/images/meh.png").resize((125, 125)))
            else:
                image = ImageTk.PhotoImage(Image.open(self.database.return_value("icon", username)).resize((125, 125)))
            account_page.update_icon(
                self.database.return_value("icon", username),
                image
            )
            self.protocol("WM_DELETE_WINDOW", self.withdraw())

    def save_account(self, username, get_username):
        try:
            self.smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.smtpserver.ehlo()
            self.smtpserver.login('wizarddoauthteam@gmail.com', 'dolm zzwc bppk uasa')
            self.confirm_number = randint(100000, 999999)
            self.smtpserver.sendmail(
                "wizarddoauthteam@gmail.com",
                f"{self.database.search("accounts", "username", f"{username}")["email"]}",
                f"""\n
                Hello user!\n\n
                Your verification code is {str(self.confirm_number)}.
                \nIf you got this email by mistake, ignore it.
                \n\nFrom,\nThe Wizard-Do Authentication Team
                """
            )
        except:
            # APOCALYPSE scenario, hope NO user EVER has to go through this
            self.forgot_password.configure(border_color="#dd0525",
                                           text="Sorry, we're unable to contact the provided email address."
                                           )
            self.smtpserver.close()
            return
        self.smtpserver.close()
        self.frame.pack_forget()
        self.frame = account_recover.AccountRecover(self, self.confirm_number, self.username)
        self.frame.pack(fill="both", expand=True)
