import os


class Config:
    def __init__(self) -> None:
        self.data_path = self.load_data_path()

        self.username = self.load_username()
        self.password = self.load_password()

        self.session_key = self.load_session_key()
        self.session_expiry_days = self.load_session_expiry_days()

    def load_data_path(self):
        return os.environ["FLATNOTES_PATH"]

    def load_username(self):
        return os.environ["FLATNOTES_USERNAME"]

    def load_password(self):
        return os.environ["FLATNOTES_PASSWORD"]

    def load_session_key(self):
        return os.environ["FLATNOTES_SECRET_KEY"]

    def load_session_expiry_days(self):
        return int(os.environ.get("FLATNOTES_SESSION_EXPIRY_DAYS", 30))


config = Config()
