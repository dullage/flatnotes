from datetime import datetime, timedelta

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from helpers import get_env

from ..base import BaseAuth
from ..models import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token", auto_error=False)


class OIDCAuth(BaseAuth):
    JWT_ALGORITHM = "HS256"

    def __init__(self) -> None:
        self.provider_url = get_env("FLATNOTES_OIDC_PROVIDER_URL", mandatory=True)
        self.client_id = get_env("FLATNOTES_OIDC_CLIENT_ID", mandatory=True)
        self.client_secret = get_env("FLATNOTES_OIDC_CLIENT_SECRET", mandatory=True)
        self.secret_key = get_env("FLATNOTES_SECRET_KEY", mandatory=True)

        self.redirect_uri = get_env("FLATNOTES_OIDC_REDIRECT_URI", mandatory=False)
        self.scopes = get_env(
            "FLATNOTES_OIDC_SCOPES", mandatory=False, default="openid email profile"
        )
        self.session_expiry_days = get_env(
            "FLATNOTES_SESSION_EXPIRY_DAYS", default=30, cast_int=True
        )

        allowed_users_str = get_env(
            "FLATNOTES_OIDC_ALLOWED_USERS", mandatory=False, default=""
        )
        self.allowed_users = [
            u.strip().lower() for u in allowed_users_str.split(",") if u.strip()
        ]

        self.provider_name = get_env(
            "FLATNOTES_OIDC_PROVIDER_NAME", mandatory=False, default="OIDC"
        )
        self.auto_redirect = get_env(
            "FLATNOTES_OIDC_AUTO_REDIRECT", mandatory=False, default=False, cast_bool=True
        )

        self.oauth = OAuth()
        self.oauth.register(
            name="oidc",
            client_id=self.client_id,
            client_secret=self.client_secret,
            server_metadata_url=f"{self.provider_url.rstrip('/')}/.well-known/openid-configuration",
            client_kwargs={"scope": self.scopes},
        )

    def login(self, data):
        raise NotImplementedError("OIDC uses redirect-based authentication")

    async def handle_callback(self, request: Request) -> Token:
        token_data = await self.oauth.oidc.authorize_access_token(request)

        user_info = token_data.get("userinfo")
        if not user_info:
            user_info = await self.oauth.oidc.parse_id_token(token_data, nonce=None)

        email = user_info.get("email", "").lower()
        if not email:
            raise HTTPException(status_code=401, detail="Email not provided by OIDC provider")

        if self.allowed_users and email not in self.allowed_users:
            raise HTTPException(status_code=403, detail="User not authorized")

        access_token = self._create_access_token({
            "sub": email,
            "name": user_info.get("name", email)
        })
        return Token(access_token=access_token)

    def authenticate(self, request: Request, token: str = Depends(oauth2_scheme)):
        if token is None:
            token = request.cookies.get("token")
        try:
            self._validate_token(token)
        except (JWTError, ValueError):
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def _validate_token(self, token: str) -> dict:
        if token is None:
            raise ValueError("No token provided")
        payload = jwt.decode(token, self.secret_key, algorithms=[self.JWT_ALGORITHM])
        if payload.get("sub") is None:
            raise ValueError("Invalid token payload")
        return payload

    def _create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expiry = datetime.utcnow() + timedelta(days=self.session_expiry_days)
        to_encode.update({"exp": expiry})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.JWT_ALGORITHM)
