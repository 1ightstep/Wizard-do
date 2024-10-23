import ttkbootstrap as ttk
from PIL import Image, ImageTk

from database.database import Database
from public.images.resources import img_to_number


class AccountImage(ttk.Toplevel):
    def __init__(self, master, account_page, dashboard_page, get_username):
        super().__init__(master)
        self.title("Account Profile Pictures")
        self.iconbitmap("public/images/Wizard-Do.ico")
        self.database = Database("/database/database")
        self.pictures = img_to_number.pictures
        self.account = self.database.search("accounts",
                                            "username",
                                            f'{get_username()}')
        self.create_icons(account_page, dashboard_page)

    def create_icons(self, account_page, dashboard_page):
        img = 1
        for row in range(5):
            for col in range(5):
                icon = ImageTk.PhotoImage(Image.open(self.pictures[img]).resize((75, 75)))
                image = ttk.Label(self, text="hello", image=icon)
                image.image = icon
                image.pack_propagate(False)
                image.grid(row=row, column=col, padx=5, pady=5)
                image.bind("<Button-1>", lambda e, icon_var=self.pictures[img]: account_page.update_icon(
                    icon_var,
                    ImageTk.PhotoImage(Image.open(icon_var).resize((125, 125))),
                    ImageTk.PhotoImage(Image.open(icon_var).resize((75, 75))),
                    dashboard_page
                ))

                img += 1
