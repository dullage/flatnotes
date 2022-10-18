import os
import sys
from base64 import b32encode
from enum import Enum

from logger import logger


class AuthType(str, Enum):
    NONE = "none"
    PASSWORD = "password"
    TOTP = "totp"


class Config:
    def __init__(self) -> None:
        self.data_path = self.get_data_path()

        self.auth_type = self.get_auth_type()

        self.username = self.get_username()
        self.password = self.get_password()

        self.session_key = self.get_session_key()
        self.session_expiry_days = self.get_session_expiry_days()

        self.totp_key = self.get_totp_key()

    @classmethod
    def get_env(cls, key, mandatory=False, default=None, cast_int=False):
        """Get an environment variable."""
        value = os.environ.get(key)
        if mandatory and not value:
            logger.error(f"Environment variable {key} must be set.")
            sys.exit(1)
        if not mandatory and not value:
            return default
        if cast_int:
            try:
                value = int(value)
            except (TypeError, ValueError):
                logger.error(f"Invalid value '{value}' for {key}.")
                sys.exit(1)
        return value

    def get_data_path(self):
        return self.get_env("FLATNOTES_PATH", mandatory=True)

    def get_auth_type(self):
        key = "FLATNOTES_AUTH_TYPE"
        auth_type = self.get_env(
            key, mandatory=False, default=AuthType.PASSWORD.value
        )
        try:
            auth_type = AuthType(auth_type.lower())
        except ValueError:
            logger.error(
                f"Invalid value '{auth_type}' for {key}. "
                + "Must be one of: "
                + ", ".join([auth_type.value for auth_type in AuthType])
                + "."
            )
            sys.exit(1)
        return auth_type

    def get_username(self):
        return self.get_env(
            "FLATNOTES_USERNAME", mandatory=self.auth_type != AuthType.NONE
        )

    def get_password(self):
        return self.get_env(
            "FLATNOTES_PASSWORD", mandatory=self.auth_type != AuthType.NONE
        )

    def get_session_key(self):
        return self.get_env(
            "FLATNOTES_SECRET_KEY", mandatory=self.auth_type != AuthType.NONE
        )

    def get_session_expiry_days(self):
        return self.get_env(
            "FLATNOTES_SESSION_EXPIRY_DAYS",
            mandatory=False,
            default=30,
            cast_int=True,
        )

    def get_totp_key(self):
        totp_key = self.get_env(
            "FLATNOTES_TOTP_KEY", mandatory=self.auth_type == AuthType.TOTP
        )
        if totp_key:
            totp_key = b32encode(totp_key.encode("utf-8"))
        return totp_key


config = Config()
