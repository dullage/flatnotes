from typing import Dict, List, Optional

from config import Config
from flatnotes import Note, SearchResult
from helpers import CamelCaseBaseModel
from auth_type import AuthType


class LoginModel(CamelCaseBaseModel):
    username: str
    password: str


class NoteModel(CamelCaseBaseModel):
    title: str
    last_modified: Optional[int]
    content: Optional[str]

    @classmethod
    def dump(cls, note: Note, include_content: bool = True) -> Dict:
        return {
            "title": note.title,
            "lastModified": note.last_modified,
            "content": note.content if include_content else None,
        }


class NotePatchModel(CamelCaseBaseModel):
    new_title: Optional[str]
    new_content: Optional[str]


class SearchResultModel(CamelCaseBaseModel):
    score: Optional[float]
    title: str
    last_modified: int
    title_highlights: Optional[str]
    content_highlights: Optional[str]
    tag_matches: Optional[List[str]]

    @classmethod
    def dump(self, search_result: SearchResult) -> Dict:
        return {
            "score": search_result.score,
            "title": search_result.title,
            "lastModified": search_result.last_modified,
            "titleHighlights": search_result.title_highlights,
            "contentHighlights": search_result.content_highlights,
            "tagMatches": search_result.tag_matches,
        }


class ConfigModel(CamelCaseBaseModel):
    auth_type: AuthType

    @classmethod
    def dump(self, config: Config) -> Dict:
        return {
            "authType": config.auth_type.value,
        }
