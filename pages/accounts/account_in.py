import customtkinter as ctk
from tkinter import messagebox
from database.database import Database


class AccountIn(ctk.CTk):
    def __init__(self, account_page, dashboard_page, tasks_page):
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
        self.entry1 = ctk.CTkEntry(self.frame, placeholder_text="Username", corner_radius=5, width=250, height=50)
        self.entry1.pack(pady=(40, 5), padx=10, side="top", anchor="n")
        self.entry2 = ctk.CTkEntry(self.frame, placeholder_text="Password", corner_radius=5, width=250, height=50)
        self.entry2.configure(show="•")
        self.entry2.pack(pady=5, padx=10, side="top")
        self.checkbox = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                        command=self.show)
        self.checkbox.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0, command=lambda: self.login(
            self.entry1.get(), self.entry2.get(), account_page, dashboard_page, tasks_page))
        self.entry1.bind("<Return>", lambda e: self.login(self.entry1.get(), self.entry2.get(), account_page, dashboard_page, tasks_page))
        self.entry2.bind("<Return>", lambda e: self.login(self.entry1.get(), self.entry2.get(), account_page, dashboard_page, tasks_page))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()

    def show(self):
        if self.checkbox.get() == 1:
            self.entry2.configure(show="")
        else:
            self.entry2.configure(show="•")

    def login(self, username, password, account_page, dashboard_page, tasks_page):
        # return ALL accounts, sift thru each one for matching account
        accounts = self.database.return_all("accounts")
        if username == "" or password == "":
            messagebox.showerror("Text Box is Empty!", "At least one of the entry boxes is empty, please try again!")
            return
        for instance in accounts:
            if instance["username"] == username and instance["password"] == password:
                self.log_check(True, username, account_page, dashboard_page, tasks_page)
                return
        self.log_check(False, None, None, None, None)

    def log_check(self, value, username, account_page, dashboard_page, tasks_page):
        if value:
            messagebox.showinfo("Login Successful", "Welcome!")
            account_page.update_ui(username, tasks_page)
            dashboard_page.refresh_name(username)
            self.protocol("WM_DELETE_WINDOW", self.withdraw())
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")