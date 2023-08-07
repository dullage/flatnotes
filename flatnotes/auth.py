from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import AuthType, config

JWT_ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry_datetime = datetime.utcnow() + timedelta(
        days=config.session_expiry_days
    )
    to_encode.update({"exp": expiry_datetime})
    encoded_jwt = jwt.encode(
        to_encode, config.session_key, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


def validate_token(token: str = Depends(oauth2_scheme)):
    if config.auth_type == AuthType.NONE:
        return
    try:
        payload = jwt.decode(
            token, config.session_key, algorithms=[JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None or username.lower() != config.username.lower():
            raise ValueError
        return
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def no_auth():
    return


def get_auth(for_edit: bool = True):
    if config.auth_type == AuthType.NONE:
        return no_auth
    elif (
        config.auth_type
        in [AuthType.PASSWORD_EDIT_ONLY, AuthType.TOTP_EDIT_ONLY]
        and for_edit is False
    ):
        return no_auth
    else:
        return validate_token
