import logging
import os
from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from flatnotes import Flatnotes, Note, NoteHit
from helpers import CamelCaseBaseModel, is_path_safe

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
    return RedirectResponse("/index.html")


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
    if not is_path_safe(filename):
        return JSONResponse(status_code=404)  # TODO: Different code
    note = Note(os.path.join(flatnotes.notes_dirpath, filename), new=True)
    note.content = content
    # TODO: Handle file exists
    return NoteModel.dump(note, include_content=True)


@app.get("/api/notes/{filename}", response_model=NoteModel)
async def get_note(filename: str, include_content: bool = True):
    """Get a specific note."""
    if not is_path_safe(filename):
        return JSONResponse(status_code=404)
    note = Note(os.path.join(flatnotes.notes_dirpath, filename))
    try:
        return NoteModel.dump(note, include_content=include_content)
    except FileNotFoundError:
        return JSONResponse(status_code=404)


@app.patch("/api/notes/{filename}", response_model=NoteModel)
async def patch_note(
    filename: str, new_filename: str = None, new_content: str = None
):
    if not is_path_safe(filename):
            return JSONResponse(status_code=404)
    note = Note(
        os.path.join(flatnotes.notes_dirpath, filename)
    )  # TODO: Stop repeating this
    if new_filename is not None:
        note.filename = new_filename
    if new_content is not None:
        note.content = new_content
    return NoteModel.dump(note, include_content=True)


@app.delete("/api/notes/{filename}")
async def delete_note(filename: str):
    if not is_path_safe(filename):
            return JSONResponse(status_code=404)
    note = Note(os.path.join(flatnotes.notes_dirpath, filename))
    note.delete()


@app.get("/api/search", response_model=List[NoteHitModel])
async def search(term: str):
    """Perform a full text search for a note."""
    return [NoteHitModel.dump(note_hit) for note_hit in flatnotes.search(term)]


app.mount("/", StaticFiles(directory="flatnotes/dist"), name="dist")
