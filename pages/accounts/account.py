import ttkbootstrap as ttk
from database.database import Database
from public.images.resources import img_to_number
from pages.settings.settings_account import AccountMenu


class Accounts(ttk.Frame):
    def __init__(self, master, dashboard_page, tasks_page):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.title = ttk.Label(self, text="Account", font=("Helvetica", 20, "bold"))
        self.title.pack(fill="x", ipady=10)
        self.frame = AccountMenu(self, dashboard_page, tasks_page)
        self.frame.pack(fill="both", expand=True)
        master.protocol("WM_DELETE_WINDOW", self.account_page_end_event)

    def account_page_end_event(self):
        current_account = self.database.return_value("icon",
                                                     f'{self.database.return_value("settings", "signed_in")}')
        if current_account:
            new_account = {
                f'{self.database.return_value("settings", "signed_in")}': current_account
                }
            print(str(current_account) + "\n" + str(new_account))
            # WORK ON THIS
            self.database.replace_specific("icon",
                                           self.database.search(
                                               self.database.return_value("settings", "signed_in"),
                                               current_account),
                                           new_account
                                           )
