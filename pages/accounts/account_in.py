import hashlib
import customtkinter as ctk
from tkinter import messagebox
from database.database import Database


class AccountIn(ctk.CTk):
    def __init__(self, username, account_page, dashboard_page, tasks_page):
        super().__init__()
        self.title("Sign In")
        self.database = Database("/database/databases")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap("public/images/acc.ico")
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
                                             border_color="#dd0525")
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0, command=lambda: self.login(
            username,
            self.entry.get(),
            account_page,
            dashboard_page,
            tasks_page
        ))
        self.entry.bind("<Return>", lambda e: self.login(
            username,
            self.entry.get(),
            account_page,
            dashboard_page,
            tasks_page
        ))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.error_message = ctk.CTkLabel(self.frame, text_color="#dd0525", text="Couldn't sign you in")
        self.total_attempts = 0
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()

    def show(self):
        if self.checkbox1.get() == 1:
            self.entry.configure(show="")
        else:
            self.entry.configure(show="•")

    def login(self, username, password, account_page, dashboard_page, tasks_page):
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
                self.log_check(True, username, account_page, dashboard_page, tasks_page)
                return
        self.log_check(False, None, None, None, None)

    def log_check(self, value, username, account_page, dashboard_page, tasks_page):
        if value:
            self.submit.configure(bg_color="#4ddd05")
            account_page.update_ui(username, tasks_page, dashboard_page)
            dashboard_page.refresh_ui(username)
            self.protocol("WM_DELETE_WINDOW", self.withdraw())
        else:
            self.error_message.pack(pady=(0, 25), padx=10, side="right", anchor="se")
            self.total_attempts += 1
            if self.total_attempts >= 3:
                self.error_message.pack_forget()
                self.forgot_password.pack(pady=(0, 25), padx=10, side="right", anchor="se")
