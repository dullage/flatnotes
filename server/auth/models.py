from pydantic import BaseModel, Field

from helpers import CustomBaseModel


class Login(CustomBaseModel):
    username: str
    password: str


class Token(BaseModel):
    # Note: OAuth requires keys to be snake_case so we use the standard
    # BaseModel here
    access_token: str
    token_type: str = Field("bearer")
