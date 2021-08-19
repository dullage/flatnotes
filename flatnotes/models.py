from typing import Dict, Optional

from helpers import CamelCaseBaseModel

from flatnotes import Note, NoteHit


class LoginModel(CamelCaseBaseModel):
    username: str
    password: str


class NoteModel(CamelCaseBaseModel):
    filename: str
    last_modified: int
    content: Optional[str]

    @classmethod
    def dump(cls, note: Note, include_content: bool = True) -> Dict:
        return {
            "filename": note.filename,
            "lastModified": note.last_modified,
            "content": note.content if include_content else None,
        }


class NotePatchModel(CamelCaseBaseModel):
    new_filename: Optional[str]
    new_content: Optional[str]


class NoteHitModel(CamelCaseBaseModel):
    filename: str
    last_modified: int
    title_highlights: Optional[str]
    content_highlights: Optional[str]

    @classmethod
    def dump(self, note_hit: NoteHit) -> Dict:
        return {
            "filename": note_hit.filename,
            "lastModified": note_hit.last_modified,
            "titleHighlights": note_hit.title_highlights,
            "contentHighlights": note_hit.content_highlights,
        }
