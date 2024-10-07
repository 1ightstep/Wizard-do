import ttkbootstrap as ttk
from database.database import Database
from pages.accounts import account
from PIL import Image, ImageTk
from public.images.resources import img_to_number


class AccountImage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.pictures = img_to_number.pictures
        self.account_make = account.Accounts
        self.ico = ImageTk.PhotoImage(Image.open("images/balanced.png").resize((200, 200)))
        self.display = ttk.Label(self, image=self.ico)
        self.display.image = self.ico
        self.display.pack(padx=50, pady=50, side="left")

        self.frame = ttk.Frame(self)
        self.frame.pack(padx=20, side="right")
        self.createicons()

    def createicons(self):
        img = 1
        for row in range(5):
            for col in range(5):
                icon = ImageTk.PhotoImage(Image.open(self.pictures[img]).resize((75, 75)))
                self.image = ttk.Label(self.frame, text="hello", image=icon)
                self.image.image = icon
                self.image.pack_propagate(False)
                self.image.grid(row=row, column=col, padx=2, pady=2)
                self.image.bind("<Button-1>", lambda _, icon_var=self.pictures[img]: self.update_icon(icon_var))

                img += 1

    def update_icon(self, icon):
        hlr = ImageTk.PhotoImage(Image.open(icon).resize((200, 200)))
        self.display.config(image=hlr)
        self.display.image = hlr
        self.account_make.update_icon(account, icon)