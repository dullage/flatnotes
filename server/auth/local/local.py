import secrets
from base64 import b32encode
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pyotp import TOTP
from pyotp.utils import build_uri
from qrcode import QRCode

from global_config import AuthType, GlobalConfig
from helpers import get_env

from ..base import BaseAuth
from ..models import Login, Token

global_config = GlobalConfig()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token", auto_error=False)


class LocalAuth(BaseAuth):
    JWT_ALGORITHM = "HS256"

    def __init__(self) -> None:
        self.username = get_env("FLATNOTES_USERNAME", mandatory=True).lower()
        self.password = get_env("FLATNOTES_PASSWORD", mandatory=True)
        self.secret_key = get_env("FLATNOTES_SECRET_KEY", mandatory=True)
        self.session_expiry_days = get_env(
            "FLATNOTES_SESSION_EXPIRY_DAYS", default=30, cast_int=True
        )

        # TOTP
        self.is_totp_enabled = False
        if global_config.auth_type == AuthType.TOTP:
            self.is_totp_enabled = True
            self.totp_key = get_env("FLATNOTES_TOTP_KEY", mandatory=True)
            self.totp_key = b32encode(self.totp_key.encode("utf-8"))
            self.totp = TOTP(self.totp_key)
            self.last_used_totp = None
            self._display_totp_enrolment()

    def login(self, data: Login) -> Token:
        # Check Username
        username_correct = secrets.compare_digest(
            self.username.lower(), data.username.lower()
        )

        # Check Password & TOTP
        expected_password = self.password
        if self.is_totp_enabled:
            current_totp = self.totp.now()
            expected_password += current_totp
        password_correct = secrets.compare_digest(
            expected_password, data.password
        )

        # Raise error if incorrect
        if not (
            username_correct
            and password_correct
            # Prevent TOTP from being reused
            and (
                self.is_totp_enabled is False
                or current_totp != self.last_used_totp
            )
        ):
            raise ValueError("Incorrect login credentials.")
        if self.is_totp_enabled:
            self.last_used_totp = current_totp

        # Create Token
        access_token = self._create_access_token(data={"sub": self.username})
        return Token(access_token=access_token)

    def authenticate(
        self, request: Request, token: str = Depends(oauth2_scheme)
    ):
        # If no token is found in the header, check the cookies
        if token is None:
            token = request.cookies.get("token")
        # Validate the token
        try:
            self._validate_token(token)
        except (JWTError, ValueError):
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def _validate_token(self, token: str) -> bool:
        if token is None:
            raise ValueError
        payload = jwt.decode(
            token, self.secret_key, algorithms=[self.JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None or username.lower() != self.username:
            raise ValueError

    def _create_access_token(self, data: dict):
        to_encode = data.copy()
        expiry_datetime = datetime.utcnow() + timedelta(
            days=self.session_expiry_days
        )
        to_encode.update({"exp": expiry_datetime})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.JWT_ALGORITHM
        )
        return encoded_jwt

    def _display_totp_enrolment(self):
        # Fix for #237. Remove padding as per spec:
        # https://github.com/google/google-authenticator/wiki/Key-Uri-Format#secret
        unpadded_secret = self.totp_key.rstrip(b"=")
        uri = build_uri(unpadded_secret, self.username, issuer="flatnotes")
        qr = QRCode()
        qr.add_data(uri)
        print(
            "\nScan this QR code with your TOTP app of choice",
            "e.g. Authy or Google Authenticator:",
        )
        qr.print_ascii()
        print(
            f"Or manually enter this key: {self.totp.secret.decode('utf-8')}\n"
        )
