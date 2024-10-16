import ttkbootstrap as ttk
from database.database import Database
from pages.accounts import account
from PIL import Image, ImageTk
from public.images.resources import img_to_number


class AccountImage(ttk.Frame):
    def __init__(self, master, account_page):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.pictures = img_to_number.pictures

        self.createicons(account_page)


    def createicons(self, account_page):
        img = 1
        for row in range(5):
            for col in range(5):
                icon = ImageTk.PhotoImage(Image.open(self.pictures[img]).resize((75, 75)))
                self.image = ttk.Label(self, text="hello", image=icon)
                self.image.image = icon
                self.image.pack_propagate(False)
                self.image.grid(row=row, column=col, padx=2, pady=2)
                self.image.bind("<Button-1>", lambda _, icon_var=icon: account_page.update_icon(icon_var))

                img += 1
