import ttkbootstrap as ttk
from database.database import Database
from public.images.resources import img_to_number
from pages.settings.settings_account import AccountMenu


class Accounts(ttk.Frame):
    def __init__(self, master, dashboard_page, tasks_page):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.account = self.database.search("accounts",
                                            "username",
                                            f'{self.database.return_value("settings", "signed_in")}')
        self.title = ttk.Label(self, text="Account", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        self.frame = AccountMenu(self, dashboard_page, tasks_page)
        self.frame.pack(fill="both", expand=True)
        master.protocol("WM_DELETE_WINDOW", self.account_page_end_event)

    def account_page_end_event(self):
        self.frame.get_important_widgets()
        current_account_icon = self.database.return_value("icon",
                                                     f'{self.database.return_value("settings", "signed_in")}')
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
                                               'username': self.database.return_value("settings", "signed_in"),
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
