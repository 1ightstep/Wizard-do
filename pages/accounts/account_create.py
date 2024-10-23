import hashlib
import smtplib
from random import randint
from tkinter import messagebox

import customtkinter as ctk

from database.database import Database


class AccountCreate(ctk.CTk):
    def __init__(self, account_page):
        super().__init__()
        self.title("Create Account")
        self.database = Database("/database/database")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap("public/images/Wizard-Do.ico")

        self.header = ctk.CTkLabel(self,
                                   text="Sign Up",
                                   font=("Helvetica", 20, "bold"))
        self.header.pack(fill="x", pady=(10, 0))

        self.step_frame = ctk.CTkFrame(self)
        self.step_frame.pack(fill="both", expand=True)

        self.current_step = AccountCreate1(self.step_frame, account_page)

        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()


class AccountCreate1(ctk.CTkFrame):
    def __init__(self, master, account_page):
        super().__init__(master)
        self.database = Database("/database/database")
        self.frame1 = ctk.CTkFrame(master)
        self.frame1.pack(fill="both", expand=True)
        self.entry1 = ctk.CTkEntry(self.frame1, placeholder_text="Username", corner_radius=5, width=250, height=50)
        self.entry1.pack(pady=(40, 5), padx=10, side="top", anchor="n")
        self.entry2 = ctk.CTkEntry(self.frame1, placeholder_text="Email", corner_radius=5, width=250, height=50)
        self.entry2.pack(pady=5, padx=10, side="top", anchor="n")
        self.entry3 = ctk.CTkEntry(self.frame1, placeholder_text="Password", corner_radius=5, width=250, height=50)
        self.entry3.configure(show="•")
        self.entry3.pack(pady=5, padx=10, side="top")
        self.entry4 = ctk.CTkEntry(self.frame1, placeholder_text="Confirm", corner_radius=5, width=250,
                                   height=50)
        self.entry4.configure(show="•")
        self.entry4.pack(pady=5, padx=10, side="top")
        self.checkbox = ctk.CTkCheckBox(self.frame1, width=25, height=25, text="Show Password", corner_radius=0,
                                        command=self.show)
        self.checkbox.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit1 = ctk.CTkButton(self.frame1, text="Sign Up", corner_radius=0, command=self.sign_up_step_1)
        self.submit1.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.entry1.bind("<Return>", lambda e: self.sign_up_step_1())
        self.entry2.bind("<Return>", lambda e: self.sign_up_step_1())
        self.entry3.bind("<Return>", lambda e: self.sign_up_step_1())
        self.entry4.bind("<Return>", lambda e: self.sign_up_step_1())

        # Page 2
        self.confirm_number = 0
        self.frame2 = ctk.CTkFrame(master)
        self.prompt = ctk.CTkLabel(self.frame2,
                                   text="A 6 digit code was sent to the provided email address.\nEnter it here "
                                        "to proceed with account creation.",
                                   font=("Helvetica", 18, "bold"))
        self.prompt.pack(pady=(40, 5), padx=10, side="top", anchor="n")
        self.message = ctk.CTkEntry(self.frame2, placeholder_text="Enter Verification Code Here (check email for code)")
        self.message.pack(fill="x", expand=True, pady=5, padx=10, side="top", anchor="center")
        self.back_button = ctk.CTkButton(self.frame2, text="Back", command=self.back)
        self.submit2 = ctk.CTkButton(self.frame2, text="Submit", command=lambda: self.sign_up_step_3(
            [
                self.entry1.get(),
                self.entry2.get(),
                self.entry3.get()
            ],
            self.confirm_number,
            self.message.get(),
            account_page
        ))
        self.submit2.pack(fill="x", expand=True, pady=5, padx=10, side="bottom", anchor="n")

    def show(self):
        if self.checkbox.get() == 1:
            self.entry3.configure(show="")
            self.entry4.configure(show="")
        else:
            self.entry3.configure(show="•")
            self.entry4.configure(show="•")

    def next(self):
        self.frame1.pack_forget()
        self.frame2.pack(fill="both", expand=True)

    def back(self):
        self.frame2.pack_forget()
        self.frame1.pack(fill="both", expand=True)

    def sign_up_step_1(self):
        accounts = self.database.return_all("accounts")
        for item in self.frame1.winfo_children():
            if item == ctk.CTkButton:
                item.configure(border_color=['#979DA2', '#565B5E'])
                if not item.get():
                    item.configure(border_color="#dd0525")
                    return
        if self.entry3.get() != self.entry4.get():
            self.entry3.configure(border_color="#dd0525")
            self.entry4.configure(border_color="#dd0525")
            return
        if not accounts:
            self.sign_up_step_2(self.entry2.get())
            return
        for instance in accounts:
            if instance["username"] == self.entry1.get():
                messagebox.showerror("Username Taken!",
                                     "Username is already taken by someone else, please use a different one.")
                return
        self.sign_up_step_2(self.entry2.get())

    def sign_up_step_2(self, email):
        try:
            self.smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.smtpserver.ehlo()
            self.smtpserver.login('wizarddoauthteam@gmail.com', 'dolm zzwc bppk uasa')
            self.confirm_number = randint(100000, 999999)
            self.smtpserver.sendmail(
                "wizarddoauthteam@gmail.com",
                f"{email}",
                f"""\n
                Hello new user!\n\n
                Your verification code is {str(self.confirm_number)}.
                \nIf you got this email by mistake, ignore it.
                \n\nFrom,\nThe Wizard-Do Authentication Team
                """
            )
        except smtplib.SMTPRecipientsRefused:
            self.entry2.configure(border_color="#dd0525")
            self.smtpserver.close()
            return
        self.smtpserver.close()
        for item in self.frame1.winfo_children():
            item.pack_forget()
        self.next()
        self.destroy()
        self.frame2.pack()

    def sign_up_step_3(self, new_account, confirm_number, number, account_page):
        if str(confirm_number) == number:
            self.sign_up_step_4(new_account, account_page)
        else:
            self.message.configure(
                border_color="#dd0525"
            )

    def sign_up_step_4(self, new_account, account_page):
        self.database = Database("/database/database")
        account_page.update_ui(new_account[0])
        hashed = hashlib.md5()
        message = new_account[2].encode()
        hashed.update(message)
        print(new_account)
        self.database.add_data("accounts",
                               {'username': new_account[0],
                                'password': str(hashed.hexdigest()),
                                'email': new_account[1]
                                })
        self.database.add_data("icon", {f"{new_account[0]}": "public/images/meh.png"})
        self.database.create_data_category(new_account[0])
        messagebox.showinfo("Notice!", "Reopen the app to start using your account.")
        exit()
