import ttkbootstrap as ttk
from database.database import Database
from PIL import Image, ImageTk
from public.images.resources import img_to_number


class AccountImage(ttk.Toplevel):
    def __init__(self, master, account_page):
        super().__init__(master)
        self.title("Account Profile Pictures")
        self.database = Database("/database/databases")
        self.pictures = img_to_number.pictures
        self.account = self.database.search("accounts", "username",
                                            f'{self.database.return_value("settings", "signed_in")}')
        if not self.account:
            self.account = {'username': 'Guest'}
        else:
            self.create_icons(account_page)
        self.mainloop()

    def create_icons(self, account_page):
        img = 1
        for row in range(5):
            for col in range(5):
                icon = ImageTk.PhotoImage(Image.open(self.pictures[img]).resize((75, 75)))
                image = ttk.Label(self, image=icon)
                image.image = icon
                image.pack_propagate(False)
                image.grid(row=row, column=col, padx=2, pady=2)
                image.bind("<Button-1>",
                           lambda _, icon_var=icon: account_page.update_icon(icon_var,
                                                                             self.database.return_value(
                                                                                 "icon",
                                                                                 f"{self.account["username"]}"
                                                                             )))

                img += 1
