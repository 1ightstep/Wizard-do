import ttkbootstrap as ttk

from database.database import Database
from pages.settings.settings_account import AccountMenu


class Accounts(ttk.Frame):
    def __init__(self, master, get_username, update_username):
        super().__init__(master)
        self.database = Database("/database/database")
        self.account = get_username()
        self.title = ttk.Label(self, text="Account", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        self.frame = AccountMenu(self, get_username, update_username)
        self.frame.pack(fill="both", expand=True)

    def account_page_end_event(self, get_username):
        current_account_icon = self.database.return_value(
            "icon",
            get_username
        )
        current_account = self.database.search(
            "accounts",
            'username',
            get_username,
        )
        if current_account:
            new_account = {
                'username': get_username,
                'password': current_account["password"],
                'email': f'{current_account["email"]}'
            }
            new_account_icon = {
                f'{current_account["username"]}': f'{self.frame.selected_pfp}'
            }
            self.database.replace_specific(
                "accounts",
                {
                    'username': get_username,
                    'password': current_account["password"],
                    'email': current_account["email"]
                },
                new_account
            )
            self.database.replace_specific(
                "icon",
                {
                    f'{current_account["username"]}':
                    f'{current_account_icon}'
                },
                new_account_icon
            )
