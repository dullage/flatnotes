import logging
import os
from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from error_responses import (
    file_exists_response,
    file_not_found_response,
    filename_contains_path_response,
)
from flatnotes import FilenameContainsPathError, Flatnotes, Note, NoteHit
from helpers import CamelCaseBaseModel

logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO").upper())

app = FastAPI()

flatnotes = Flatnotes(os.environ["FLATNOTES_PATH"])


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


@app.get("/")
async def root():
    with open("flatnotes/dist/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.get("/api/notes", response_model=List[NoteModel])
async def get_notes(include_content: bool = False):
    """Get all notes."""
    return [
        NoteModel.dump(note, include_content=include_content)
        for note in flatnotes.get_notes()
    ]


@app.post("/api/notes", response_model=NoteModel)
async def post_note(filename: str, content: str):
    """Create a new note."""
    try:
        note = Note(flatnotes, filename, new=True)
        note.content = content
        return NoteModel.dump(note, include_content=True)
    except FilenameContainsPathError:
        return filename_contains_path_response
    except FileExistsError:
        return file_exists_response


@app.get("/api/notes/{filename}", response_model=NoteModel)
async def get_note(filename: str, include_content: bool = True):
    """Get a specific note."""
    try:
        note = Note(flatnotes, filename)
        return NoteModel.dump(note, include_content=include_content)
    except FilenameContainsPathError:
        return filename_contains_path_response
    except FileNotFoundError:
        return file_not_found_response


@app.patch("/api/notes/{filename}", response_model=NoteModel)
async def patch_note(filename: str, new_data: NotePatchModel):
    try:
        note = Note(flatnotes, filename)
        if new_data.new_filename is not None:
            note.filename = new_data.new_filename
        if new_data.new_content is not None:
            note.content = new_data.new_content
        return NoteModel.dump(note, include_content=True)
    except FilenameContainsPathError:
        return filename_contains_path_response
    except FileNotFoundError:
        return file_not_found_response


@app.delete("/api/notes/{filename}")
async def delete_note(filename: str):
    try:
        note = Note(flatnotes, filename)
        note.delete()
    except FilenameContainsPathError:
        return filename_contains_path_response
    except FileNotFoundError:
        return file_not_found_response


@app.get("/api/search", response_model=List[NoteHitModel])
async def search(term: str):
    """Perform a full text search for a note."""
    return [NoteHitModel.dump(note_hit) for note_hit in flatnotes.search(term)]


app.mount("/", StaticFiles(directory="flatnotes/dist"), name="dist")
