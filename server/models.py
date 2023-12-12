from typing import List, Optional

from pydantic import BaseModel, Field

from config import AuthType
from helpers import camel_case


class TokenModel(BaseModel):
    # Use of BaseModel instead of CustomBaseModel is intentional as OAuth
    # requires keys to be snake_case
    access_token: str
    token_type: str = Field("bearer")


class CustomBaseModel(BaseModel):
    class Config:
        alias_generator = camel_case
        populate_by_name = True
        from_attributes = True


class LoginModel(CustomBaseModel):
    username: str
    password: str


class NotePostModel(CustomBaseModel):
    title: str
    content: Optional[str] = Field(None)


class NoteResponseModel(CustomBaseModel):
    title: str
    last_modified: float


class NoteContentResponseModel(NoteResponseModel):
    content: Optional[str] = Field(None)


class NotePatchModel(CustomBaseModel):
    new_title: Optional[str] = Field(None)
    new_content: Optional[str] = Field(None)


class SearchResultModel(CustomBaseModel):
    score: Optional[float] = Field(None)
    title: str
    last_modified: float
    title_highlights: Optional[str] = Field(None)
    content_highlights: Optional[str] = Field(None)
    tag_matches: Optional[List[str]] = Field(None)


class ConfigModel(CustomBaseModel):
    auth_type: AuthType
