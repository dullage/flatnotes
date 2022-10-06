import os

from logger import logger


class Config:
    def __init__(self) -> None:
        self.data_path = self.get_data_path()

        self.username = self.get_username()
        self.password = self.get_password()

        self.session_key = self.get_session_key()
        self.session_expiry_days = self.get_session_expiry_days()

    @classmethod
    def get_env(cls, key, mandatory=False, default=None, cast_int=False):
        value = os.environ.get(key)
        if mandatory and not value:
            logger.error(f"Environment variable {key} must be set.")
            exit(1)
        if not mandatory and not value:
            return default
        if cast_int:
            try:
                value = int(value)
            except (TypeError, ValueError):
                logger.error(f"Invalid value '{value}' for {key}.")
                exit(1)
        return value

    def get_data_path(self):
        return self.get_env("FLATNOTES_PATH", mandatory=True)

    def get_username(self):
        return self.get_env("FLATNOTES_USERNAME", mandatory=True)

    def get_password(self):
        return self.get_env("FLATNOTES_PASSWORD", mandatory=True)

    def get_session_key(self):
        return self.get_env("FLATNOTES_SECRET_KEY", mandatory=True)

    def get_session_expiry_days(self):
        return self.get_env(
            "FLATNOTES_SESSION_EXPIRY_DAYS",
            mandatory=False,
            default=30,
            cast_int=True,
        )


config = Config()
