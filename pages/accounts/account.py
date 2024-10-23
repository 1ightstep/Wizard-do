import ttkbootstrap as ttk

from database.database import Database
from pages.settings.settings_account import AccountMenu


class Accounts(ttk.Frame):
    def __init__(self, master, dashboard_page, get_username, update_username):
        super().__init__(master)
        self.database = Database("/database/database")
        self.account = get_username()
        self.title = ttk.Label(self, text="Account", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        self.frame = AccountMenu(self, dashboard_page, get_username, update_username)
        self.frame.pack(fill="both", expand=True)
        master.protocol("WM_DELETE_WINDOW", lambda: self.account_page_end_event(get_username()))

    def account_page_end_event(self, get_username):
        self.frame.get_important_widgets()
        current_account_icon = self.database.return_value("icon",
                                                          f'{get_username}')
        current_account = self.database.search("accounts",
                                               'username',
                                               f'{self.frame.get_important_widgets()[0].cget("text")}',
                                               )
        if current_account:
            new_account = {
                'username': f'{self.frame.get_important_widgets()[0].cget("text")}',
                'password': current_account["password"],
                'email': f'{current_account["email"]}'
            }
            new_account_icon = {
                f'{current_account["username"]}': f'{self.frame.get_important_widgets()[1].cget("text")}'
            }
            # WORK ON THIS
            self.database.replace_specific("accounts",
                                           {
                                               'username': get_username,
                                               'password': current_account["password"],
                                               'email': current_account["email"]
                                           },
                                           new_account
                                           )
            self.database.replace_specific("icon",
                                           {
                                               f'{current_account["username"]}':
                                                   f'{current_account_icon}'
                                           },
                                           new_account_icon
                                           )
