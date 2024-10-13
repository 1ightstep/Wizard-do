import ttkbootstrap as ttk
from database.database import Database
from pages.accounts import account
from PIL import Image, ImageTk
from public.images.resources import img_to_number


class AccountImage(ttk.LabelFrame):
    def __init__(self, master, account_page):
        super().__init__(master=master, text="Profile Picture")
        self.database = Database("/database/databases")

        self.pictures = img_to_number.pictures
        self.account_make = account.Accounts
        self.ico = ImageTk.PhotoImage(
            Image.open(self.pictures[self.database.return_value("accounts", "icon")]).resize(
                (200, 200)))
        self.display = ttk.Label(self, image=self.ico)
        self.display.image = self.ico
        self.display.pack(padx=50, pady=50, side="left")

        self.frame = ttk.Frame(self)
        self.frame.pack(padx=20, side="right")
        self.create_icons(account_page)

    def create_icons(self, page1):
        img = 1
        for row in range(5):
            for col in range(5):
                icon = ImageTk.PhotoImage(Image.open(self.pictures[img]).resize((75, 75)))
                self.image = ttk.Label(self.frame, text="hello", image=icon)
                self.image.image = icon
                self.image.pack_propagate(False)
                self.image.grid(row=row, column=col, padx=2, pady=2)
                self.image.bind("<Button-1>", lambda _, icon_var=self.pictures[img]: self.update_icon(page1, icon_var))

                img += 1

    def update_icon(self, page, icon):
        hlr = ImageTk.PhotoImage(Image.open(icon).resize((200, 200)))
        self.display.config(image=hlr)
        self.display.image = hlr
        # make this shorter
        self.database.replace_specific("accounts",
                                       {'username': f'{self.database.return_value("settings", "signed_in")}',
                                        'password': f'{self.database.return_value(self.database.return_value("settings", "signed_in"), "password")}',
                                        'icon': f'{self.database.return_value(self.database.return_value("settings", "signed_in"), "icon")}'
                                        },
                                       {'username': f'{self.database.return_value("settings", "signed_in")}',
                                        'password': f'{self.database.return_value(self.database.return_value("settings", "signed_in"), "password")}',
                                        'icon': icon}
                                       ,)
        page.update_icon(hlrhlr = ImageTk.PhotoImage(Image.open(icon)))

