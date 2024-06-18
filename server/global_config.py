import sys
from enum import Enum

from helpers import CustomBaseModel, get_env
from logger import logger


class GlobalConfig:
    def __init__(self) -> None:
        logger.debug("Loading global config...")
        self.auth_type: AuthType = self._load_auth_type()
        self.hide_recently_modified: bool = self._load_hide_recently_modified()
        self.path_prefix: str = self._load_path_prefix()

    def load_auth(self):
        if self.auth_type in (AuthType.NONE, AuthType.READ_ONLY):
            return None
        elif self.auth_type in (AuthType.PASSWORD, AuthType.TOTP):
            from auth.local import LocalAuth

            return LocalAuth()

    def load_note_storage(self):
        from notes.file_system import FileSystemNotes

        return FileSystemNotes()

    def load_attachment_storage(self):
        from attachments.file_system import FileSystemAttachments

        return FileSystemAttachments()

    def _load_auth_type(self):
        key = "FLATNOTES_AUTH_TYPE"
        auth_type = get_env(
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

    def _load_hide_recently_modified(self):
        key = "FLATNOTES_HIDE_RECENTLY_MODIFIED"
        return get_env(key, mandatory=False, default=False, cast_bool=True)

    def _load_path_prefix(self):
        key = "FLATNOTES_PATH_PREFIX"
        value = get_env(key, mandatory=False, default="")
        if value and (not value.startswith("/") or value.endswith("/")):
            logger.error(
                f"Invalid value '{value}' for {key}. "
                + "Must start with '/' and not end with '/'."
            )
            sys.exit(1)
        return value


class AuthType(str, Enum):
    NONE = "none"
    READ_ONLY = "read_only"
    PASSWORD = "password"
    TOTP = "totp"


class GlobalConfigResponseModel(CustomBaseModel):
    auth_type: AuthType
    hide_recently_modified: bool
