from typing import Dict, Optional

from helpers import CamelCaseBaseModel

from flatnotes import Note, NoteHit


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


class NoteHitModel(CamelCaseBaseModel):
    title: str
    last_modified: int
    title_highlights: Optional[str]
    content_highlights: Optional[str]

    @classmethod
    def dump(self, note_hit: NoteHit) -> Dict:
        return {
            "title": note_hit.title,
            "lastModified": note_hit.last_modified,
            "titleHighlights": note_hit.title_highlights,
            "contentHighlights": note_hit.content_highlights,
        }
