from typing import Dict, List, Optional

from helpers import CamelCaseBaseModel

from flatnotes import Note, SearchResult


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
    rank: int
    title: str
    last_modified: int
    title_highlights: Optional[str]
    content_highlights: Optional[str]
    tag_matches: Optional[List[str]]

    @classmethod
    def dump(self, search_result: SearchResult) -> Dict:
        return {
            "rank": search_result.rank,
            "title": search_result.title,
            "lastModified": search_result.last_modified,
            "titleHighlights": search_result.title_highlights,
            "contentHighlights": search_result.content_highlights,
            "tagMatches": search_result.tag_matches,
        }
