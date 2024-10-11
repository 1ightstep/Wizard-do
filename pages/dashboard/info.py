import ttkbootstrap as ttk
from database.database import Database
from PIL import Image, ImageTk
from public.images.resources import img_to_number


class Info(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.database = Database("/database/databases")
        self.frame_names = iter(["TotalLeftFrame", "CompletedTodayFrame", "DifficultyFrame", "AverageFrame"])
        self.holder = iter(["TLF", "CTF", "AC", "AF"])

        self.labels = {}

        for x in range(4):
            self.create_frames(next(self.frame_names), next(self.holder))

        self.create_labels("Account", "Account", "", self.AC)
        self.create_labels("Total Left", "Total Tasks", "50      ", self.TLF)
        self.create_labels("Completed Today", "Completed Today", "50          ", self.CTF)
        self.create_labels("Average", "Average Time", "50 minutes", self.AF)

        self.create_labels("Account", "Account", f"{self.database.return_value("settings", "signed_in")}", self.AC)
        username = self.database.return_value("settings", "signed_in")
        try:
            password = self.database.search("accounts", "username", username)["password"]
        except KeyError:
            username = "Guest"
            password = ""
        if username == "Guest":
            self.picture = img_to_number.pictures[17]
        else:
            self.picture = img_to_number.pictures[self.database.return_value("accounts", "icon")]
        self.icon = ImageTk.PhotoImage(Image.open(self.picture))
        self.profile_picture_frame = ttk.Label(self.AC,
                                               image=self.icon,
                                               padding=15)
        self.profile_picture_frame.pack(padx=(0, 8), side=ttk.LEFT, fill=ttk.BOTH, expand=True)

    def create_frames(self, name1, name2):
        frame = ttk.LabelFrame(self, width=200, height=100)
        frame.pack_propagate(False)
        frame.pack(padx=(0, 8), side=ttk.LEFT, fill=ttk.BOTH, expand=True)

        holderframe = ttk.Frame(frame)
        holderframe.pack(side=ttk.LEFT, anchor=ttk.W, fill=ttk.BOTH, expand=True)
        setattr(self, f"{name1}", frame)
        setattr(self, f"{name2}", holderframe)

    def create_labels(self, name1, text1, text2, frame):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        max_size = min(width // 10, height // 15)
        base_font_size = max(8, min(max_size, 12))

        label1_font_size = int(base_font_size * (min(width, height) / 800))
        label2_font_size = int(label1_font_size * 2)

        label1 = ttk.Label(frame, text=text1, font=("Helvetica", label1_font_size))
        label1.pack(pady=5, padx=10, side=ttk.TOP, anchor=ttk.W)

        label2 = ttk.Label(frame, text=text2, font=("Helvetica", label2_font_size, "bold"))
        label2.pack(pady=15, padx=10, side=ttk.LEFT, anchor=ttk.W)

        self.labels[name1] = {"small": label1, "large": label2}

    def update_labels(self):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        max_size = min(width // 10, height // 15)

        base_font_size = max(8, min(max_size, 12))
        yes = int(base_font_size * (min(width, height) / 700))

        for label_set in self.labels.values():
            if isinstance(label_set["small"], ttk.Label):
                label_set["small"].config(font=("Helvetica", yes))
            if isinstance(label_set["large"], ttk.Label):
                label_set["large"].config(font=("Helvetica", int(yes * 1.5), "bold"))
