import customtkinter as ctk
from PIL import Image, ImageTk

from database.database import Database


class AccountDelete(ctk.CTk):
    def __init__(self, account_page, dashboard_page, get_username, update_username):
        super().__init__()
        self.title("Delete Account")
        self.database = Database("/database/database")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap("public/images/Wizard-Do.ico")
        self.header = ctk.CTkLabel(self,
                                   text="Delete Account",
                                   font=("Helvetica", 20, "bold"))
        self.header.pack(fill="x", pady=(10, 0))
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.entry1 = ctk.CTkEntry(self.frame, placeholder_text="Password", corner_radius=5, width=250, height=50)
        self.entry1.configure(show="•")
        self.entry1.pack(pady=(40, 5), padx=10, side="top")
        self.entry2 = ctk.CTkEntry(self.frame, placeholder_text="Confirm Password", corner_radius=5, width=250,
                                   height=50)
        self.entry2.configure(show="•")
        self.entry2.pack(pady=5, padx=10, side="top")
        self.checkbox = ctk.CTkCheckBox(self.frame, width=25, height=25, text="Show Password", corner_radius=0,
                                        command=self.show)
        self.checkbox.pack(pady=5, padx=125, side="top", anchor=ctk.W)
        self.submit = ctk.CTkButton(self.frame, text="Enter", corner_radius=0,
                                    command=lambda: self.delete(
                                        self.entry1.get(),
                                        self.entry2.get(),
                                        dashboard_page,
                                        get_username,
                                        update_username
                                    ))
        self.submit.pack(pady=(0, 25), padx=10, side="right", anchor="se")
        self.entry1.bind("<Return>", lambda e: self.delete(
            self.entry1.get(),
            self.entry2.get(),
            dashboard_page,
            get_username,
            update_username
        ))
        self.entry2.bind("<Return>", lambda e: self.delete(
            self.entry1.get(),
            self.entry2.get(),
            dashboard_page,
            get_username,
            update_username
        ))
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.mainloop()

    def show(self):
        if self.checkbox.get() == 1:
            self.entry1.configure(show="")
            self.entry2.configure(show="")
        else:
            self.entry1.configure(show="•")
            self.entry2.configure(show="•")

    def delete(self, password, confirm_password, dashboard_page, get_username, update_username):
        account_del = get_username
        if self.entry1.get() != self.entry2.get():
            self.entry1.configure(border_color="#dd0525")
            self.entry2.configure(border_color="#dd0525")
            return
        if not password:
            self.entry1.configure(border_color="#dd0525")
            return
        if not confirm_password:
            self.entry2.configure(border_color="#dd0525")
            return
        if account_del:
            update_username("Guest")
            guest_photo = ImageTk.PhotoImage(Image.open("public/images/meh.png"))
            dashboard_page.refresh_icon(guest_photo)
            self.database.delete_data("accounts", "username", f"{get_username()}")
            self.database.delete_data("icon", f"{get_username()}", "")
            self.withdraw()
            return
