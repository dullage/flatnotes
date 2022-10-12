from enum import Enum


class AuthType(str, Enum):
    NONE = "none"
    PASSWORD = "password"
    # TOTP = "totp"  # Not yet implemented
