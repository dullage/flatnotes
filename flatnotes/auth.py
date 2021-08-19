import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

FLATNOTES_USERNAME = os.environ["FLATNOTES_USERNAME"]
FLATNOTES_PASSWORD = os.environ["FLATNOTES_PASSWORD"]

JWT_SECRET_KEY = os.environ["FLATNOTES_SECRET_KEY"]
JWT_EXPIRE_DAYS = int(os.environ.get("FLATNOTES_SESSION_EXPIRY_DAYS", 30))
JWT_ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry_datetime = datetime.utcnow() + timedelta(days=JWT_EXPIRE_DAYS)
    to_encode.update({"exp": expiry_datetime})
    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None or username.lower() != FLATNOTES_USERNAME.lower():
            raise ValueError
        return FLATNOTES_USERNAME
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
